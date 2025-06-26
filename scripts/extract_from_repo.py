import os
import ast
import json
import yaml
import pandas as pd

def load_config(config_path='config.yaml'):
    """Loads the YAML configuration file."""
    with open(config_path, 'r') as file:
        return yaml.safe_load(file)

def extract_file_context_and_functions(file_path):
    """
    Performs a two-pass analysis on a file.
    1. First pass gathers all top-level imports and global constants.
    2. Second pass streams function definitions and prepends the context.
    """
    with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
        content = f.read()

    # --- Pass 1: Gather Context ---
    context_nodes = []
    try:
        tree = ast.parse(content)
        for node in tree.body:
            # We'll grab imports and simple global variable assignments
            if isinstance(node, (ast.Import, ast.ImportFrom, ast.Assign)):
                context_nodes.append(node)
    except (SyntaxError, IndexError):
        # If the file is not valid python, we can't get context.
        context_nodes = []
    
    context_header = ast.unparse(context_nodes) if context_nodes else ""

    # --- Pass 2: Stream and Extract Functions ---
    for code_chunk in stream_and_parse_definitions(content.splitlines(True)):
        try:
            tree = ast.parse(code_chunk)
            for node in ast.walk(tree):
                if isinstance(node, ast.FunctionDef):
                    docstring = ast.get_docstring(node)
                    if docstring:
                        function_source = ast.unparse(node)
                        # Prepend the context header to the function source
                        full_completion = context_header + "\\n\\n" + function_source
                        yield {
                            "prompt": docstring.strip(),
                            "completion": full_completion
                        }
        except (SyntaxError, IndexError):
            continue

def stream_and_parse_definitions(lines):
    """
    A generator that takes a list of lines and yields chunks of text
    that are likely to be top-level class or function definitions.
    """
    chunk_buffer = []
    for line in lines:
        if (line.startswith('def ') or line.startswith('class ') or line.startswith('@')) and not line.startswith(' '):
            if chunk_buffer:
                yield "".join(chunk_buffer)
            chunk_buffer = [line]
        elif chunk_buffer:
            chunk_buffer.append(line)
    
    if chunk_buffer:
        yield "".join(chunk_buffer)

def main():
    """Main function to extract data from the raw code repository."""
    config = load_config()
    repo_path = config['data']['raw_repo_path']
    output_path = config['data']['extracted_path']

    print(f"Starting context-aware extraction from: {repo_path}")
    
    all_functions = []
    for root, _, files in os.walk(repo_path):
        for file in files:
            if file.endswith('.py'):
                file_path = os.path.join(root, file)
                print(f"Processing {file_path} for context and functions...")
                try:
                    # The new context-aware generator is called here
                    extracted_generator = extract_file_context_and_functions(file_path)
                    all_functions.extend(list(extracted_generator))
                except Exception as e:
                    print(f"Error processing {file_path}: {e}")
    
    print(f"Extracted {len(all_functions)} functions with docstrings and context.")
    
    # Ensure the output directory exists
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    
    # Use pandas to save to JSONL for better handling of newlines
    df = pd.DataFrame(all_functions)
    df.to_json(output_path, orient='records', lines=True)
            
    print(f"Saved extracted data to {output_path}")

if __name__ == '__main__':
    main() 
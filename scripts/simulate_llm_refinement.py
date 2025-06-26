import yaml
import json
import pandas as pd
import time
import os
import openai

# --- Configuration Switch ---
# Set this to True to use the real OpenAI API (requires an API key)
# Set to False to use the local simulation (default)
USE_REAL_LLM = False

# --- API Key Configuration ---
# For security, the API key is loaded from an environment variable.
# To use the real API, run: export OPENAI_API_KEY='your_key_here'
if USE_REAL_LLM:
    openai.api_key = os.getenv("OPENAI_API_KEY")
    if not openai.api_key:
        raise ValueError("OPENAI_API_KEY environment variable not set. Please set it to use the real LLM.")

def load_config(config_path='config.yaml'):
    """Loads the YAML configuration file."""
    with open(config_path, 'r') as file:
        return yaml.safe_load(file)

def call_llm_judge_api_simulation(docstring, code):
    """
    Simulates calling an LLM API to judge docstring quality.
    This is a placeholder and does not make a real API call.
    """
    print(f"  [JUDGE SIM] Evaluating docstring: '{docstring[:40]}...'")
    time.sleep(0.1) # Simulate network latency

    # --- Simulation Logic ---
    # To make this interesting, we'll pretend the 'is_prime' docstring is bad.
    if "is_prime" in code:
        print("  [JUDGE SIM] Verdict: Low quality.")
        return {"score": 2, "reason": "Docstring is too brief and lacks detail."}
    
    print("  [JUDGE SIM] Verdict: High quality.")
    return {"score": 5, "reason": "The docstring is clear and accurate."}

def call_llm_judge_api_real(docstring, code):
    """
    Calls the real OpenAI API to judge docstring quality.
    NOTE: This will incur costs.
    """
    print(f"  [JUDGE API] Evaluating docstring: '{docstring[:40]}...'")
    
    prompt = f"""
You are an expert Python code reviewer. Your task is to evaluate if the given docstring accurately and sufficiently describes the provided Python function.

Respond ONLY with a JSON object with two keys:
1. "score": A rating from 1 to 5, where 1 is "completely irrelevant" and 5 is "a perfect, comprehensive description".
2. "reason": A brief, one-sentence explanation for your score.

Here is the function:
```python
{code}
```

Here is the docstring to evaluate:
```
{docstring}
```
"""
    
    response = openai.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.1,
    )
    
    try:
        result = json.loads(response.choices[0].message.content)
        print(f"  [JUDGE API] Verdict: Score {result.get('score', 'N/A')}")
        return result
    except (json.JSONDecodeError, KeyError):
        print("  [JUDGE API] Error: Could not parse LLM response.")
        return {"score": 3, "reason": "Could not parse API response."}

def call_llm_generator_api_simulation(code):
    """
    Simulates calling an LLM API to generate a new docstring.
    This is a placeholder and does not make a real API call.
    """
    print(f"  [GENERATOR SIM] Generating new docstring for function...")
    time.sleep(0.2) # Simulate network latency

    # --- Simulation Logic ---
    # Generate a new, high-quality docstring.
    new_docstring = f"""This function takes a code snippet and generates a high-quality docstring.
    
    It analyzes the function's parameters and return values to create
    a comprehensive explanation of its purpose.

    Args:
        (Extracted from code): The arguments the function accepts.
    
    Returns:
        (Extracted from code): The value the function returns.
    """
    print("  [GENERATOR SIM] New docstring created.")
    return new_docstring.strip()

def call_llm_generator_api_real(code):
    """
    Calls the real OpenAI API to generate a new docstring.
    NOTE: This will incur costs.
    """
    print(f"  [GENERATOR API] Generating new docstring for function...")

    prompt = f"""
You are an expert Python programmer tasked with writing high-quality, professional documentation.

Analyze the following Python function and write a clear, concise, and accurate docstring for it. The docstring should explain what the function does, its arguments, and what it returns.

Do not write any other text or explanation. Output ONLY the docstring itself.

Here is the function:
```python
{code}
```
"""

    response = openai.chat.completions.create(
        model="gpt-4-turbo",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.3,
    )
    
    new_docstring = response.choices[0].message.content
    print("  [GENERATOR API] New docstring created.")
    return new_docstring.strip()

def main():
    """Main function to refine the data using a simulated LLM."""
    config = load_config()
    input_path = config['data']['extracted_path']
    output_path = config['data']['llm_refined_path']
    
    print(f"Starting LLM refinement process on {input_path}...")
    
    df = pd.read_json(input_path, lines=True)
    refined_records = []
    
    for index, row in df.iterrows():
        print(f"\nProcessing record {index+1}/{len(df)}...")
        code = row['completion']
        docstring = row['prompt']
        
        # --- Dynamic Dispatch: Use real API or simulation based on the flag ---
        if USE_REAL_LLM:
            judgement = call_llm_judge_api_real(docstring, code)
        else:
            judgement = call_llm_judge_api_simulation(docstring, code)
        
        # If score is low, generate a new one
        if judgement.get('score', 0) <= 2:
            print("  -> Low score detected. Generating a new docstring.")
            if USE_REAL_LLM:
                new_docstring = call_llm_generator_api_real(code)
            else:
                new_docstring = call_llm_generator_api_simulation(code)
            final_docstring = new_docstring
        else:
            print("  -> High score. Keeping original docstring.")
            final_docstring = docstring
            
        refined_records.append({
            "prompt": final_docstring,
            "completion": code
        })

    print("\nLLM refinement process finished.")
    
    # Ensure the output directory exists before saving
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    
    # Save the refined data
    refined_df = pd.DataFrame(refined_records)
    refined_df.to_json(output_path, orient='records', lines=True)
            
    print(f"Saved LLM-refined data to {output_path}")

if __name__ == '__main__':
    main() 
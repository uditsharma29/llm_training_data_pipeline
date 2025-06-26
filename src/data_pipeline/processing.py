import pandas as pd
from typing import List, Dict
import ast

def load_data(file_path: str) -> pd.DataFrame:
    """Loads data from a JSONL file."""
    return pd.read_json(file_path, lines=True)

def is_valid_python_code(code: str) -> bool:
    """Checks if a string is valid Python code."""
    try:
        ast.parse(code)
        return True
    except SyntaxError:
        return False

def validate_code(df: pd.DataFrame) -> pd.DataFrame:
    """Filters out rows with invalid Python code in the 'completion' column."""
    initial_count = len(df)
    df['is_valid'] = df['completion'].apply(is_valid_python_code)
    valid_df = df[df['is_valid']].drop(columns=['is_valid'])
    dropped_count = initial_count - len(valid_df)
    if dropped_count > 0:
        print(f"Validated data: Dropped {dropped_count} records with invalid code.")
    return valid_df

def transform_to_alpaca_format(df: pd.DataFrame) -> List[Dict[str, str]]:
    """Transforms a DataFrame with 'prompt' and 'completion' columns to Alpaca format."""
    processed_data = []
    for _, row in df.iterrows():
        processed_data.append({
            "instruction": row["prompt"],
            "input": "",
            "output": row["completion"]
        })
    return processed_data

def save_processed_data(data: List[Dict[str, str]], output_path: str):
    """Saves the processed data to a JSONL file."""
    df = pd.DataFrame(data)
    df.to_json(output_path, orient='records', lines=True) 
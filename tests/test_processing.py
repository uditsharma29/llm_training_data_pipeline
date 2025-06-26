import pytest
import pandas as pd
import sys
import os

# Add the src directory to the Python path to allow for package imports
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'src')))

from data_pipeline.processing import (
    is_valid_python_code,
    validate_code,
    transform_to_alpaca_format
)

@pytest.fixture
def sample_dataframe():
    """Returns a sample DataFrame for testing."""
    data = {
        'prompt': [
            'Create a function to add two numbers.',
            'Create a broken function.'
        ],
        'completion': [
            """
def add(a, b):
    return a + b
""",
            """
def broken(a, b)
    return a + b
"""
        ]
    }
    return pd.DataFrame(data)

def test_is_valid_python_code_valid():
    """Tests that a valid Python code string returns True."""
    valid_code = """
def my_function():
    return 42
"""
    assert is_valid_python_code(valid_code) is True

def test_is_valid_python_code_invalid():
    """Tests that an invalid Python code string returns False."""
    invalid_code = """
def my_function()
    return 42
"""
    assert is_valid_python_code(invalid_code) is False

def test_validate_code(sample_dataframe):
    """Tests that the validate_code function correctly filters out invalid code."""
    validated_df = validate_code(sample_dataframe)
    assert len(validated_df) == 1
    assert validated_df.iloc[0]['prompt'] == 'Create a function to add two numbers.'

def test_transform_to_alpaca_format(sample_dataframe):
    """Tests that the data is correctly transformed to the Alpaca format."""
    # First, filter to only valid code since the transform runs after validation
    valid_df = validate_code(sample_dataframe)
    transformed_data = transform_to_alpaca_format(valid_df)
    
    assert len(transformed_data) == 1
    expected_record = {
        'instruction': 'Create a function to add two numbers.',
        'input': '',
        'output': valid_df.iloc[0]['completion']
    }
    assert transformed_data[0] == expected_record 
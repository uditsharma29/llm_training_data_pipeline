import os
import sys
import yaml

# Add the src directory to the Python path
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'src'))

from data_pipeline.processing import load_data, validate_code, transform_to_alpaca_format, save_processed_data

def load_config(config_path='config.yaml'):
    """Loads the YAML configuration file."""
    with open(config_path, 'r') as file:
        return yaml.safe_load(file)

def main():
    """Main function to run the data processing pipeline."""
    # Load configuration
    config = load_config()
    input_data_path = config['data']['llm_refined_path']
    final_alpaca_path = config['data']['final_alpaca_path']
    
    print("Starting data processing pipeline...")
    
    # Load raw data
    raw_df = load_data(input_data_path)
    print(f"Loaded {len(raw_df)} records from {input_data_path}")

    # Validate data
    validated_df = validate_code(raw_df)
    
    # Transform data
    processed_data = transform_to_alpaca_format(validated_df)
    print("Transformed data to Alpaca format.")
    
    # Save processed data
    save_processed_data(processed_data, final_alpaca_path)
    print(f"Saved processed data to {final_alpaca_path}")
    
    print("Data processing pipeline finished successfully.")

if __name__ == '__main__':
    main() 
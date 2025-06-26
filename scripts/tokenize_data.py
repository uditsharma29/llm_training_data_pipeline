import yaml
from datasets import load_dataset
from transformers import AutoTokenizer
import os

def load_config(config_path='config.yaml'):
    """Loads the YAML configuration file."""
    with open(config_path, 'r') as file:
        return yaml.safe_load(file)

def main():
    """Main function to tokenize the data."""
    # Load configuration
    config = load_config()
    processed_path = config['data']['final_alpaca_path']
    tokenized_path = config['data']['tokenized_path']
    model_name = "codellama/CodeLlama-7b-hf"

    print(f"Loading processed data from {processed_path}...")
    dataset = load_dataset('json', data_files=processed_path, split='train')

    print(f"Loading tokenizer for '{model_name}'...")
    tokenizer = AutoTokenizer.from_pretrained(model_name)
    
    # Set a padding token if one doesn't exist
    if tokenizer.pad_token is None:
        tokenizer.pad_token = tokenizer.eos_token

    def format_and_tokenize(example):
        """Formats the prompt and tokenizes it."""
        # The prompt template is crucial for instruction-tuned models
        prompt = f"### Instruction:\\n{example['instruction']}\\n\\n### Response:\\n{example['output']}"
        
        # Tokenize the formatted prompt
        tokenized_example = tokenizer(
            prompt,
            truncation=True,
            max_length=512, # A standard max_length
            padding="max_length"
        )
        return tokenized_example

    print("Formatting and tokenizing the dataset...")
    tokenized_dataset = dataset.map(format_and_tokenize)

    print(f"Saving tokenized dataset to {tokenized_path}...")
    # Ensure the output directory exists
    os.makedirs(tokenized_path, exist_ok=True)
    tokenized_dataset.save_to_disk(tokenized_path)

    print("Tokenization step finished successfully.")
    print(f"Data is ready for training in: {tokenized_path}")

if __name__ == '__main__':
    main() 
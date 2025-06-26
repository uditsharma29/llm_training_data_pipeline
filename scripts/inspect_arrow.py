from datasets import load_from_disk
import yaml

def load_config(config_path='config.yaml'):
    """Loads the YAML configuration file."""
    with open(config_path, 'r') as file:
        return yaml.safe_load(file)

def main():
    """Loads and inspects the final Arrow dataset."""
    config = load_config()
    tokenized_path = config['data']['tokenized_path']

    print(f"Loading tokenized dataset from: {tokenized_path}")
    
    # Load the dataset from disk
    tokenized_dataset = load_from_disk(tokenized_path)

    print("\\n--- Dataset Info ---")
    print(tokenized_dataset)

    print("\\n\\n--- Inspecting the First Record ---")
    first_record = tokenized_dataset[0]
    print(first_record)
    
    print("\\n\\n--- Breakdown of the First Record ---")
    print(f"Instruction: {first_record['instruction']}")
    # The 'input_ids' are the actual numbers the model will see.
    print(f"Number of Input IDs (Tokens): {len(first_record['input_ids'])}")
    print(f"Sample Input IDs: {first_record['input_ids'][:20]}...")

    # The 'attention_mask' tells the model which tokens to pay attention to.
    print(f"Number of Attention Mask Tokens: {len(first_record['attention_mask'])}")
    print(f"Sample Attention Mask: {first_record['attention_mask'][:20]}...")


if __name__ == '__main__':
    main() 
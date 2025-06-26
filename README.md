# Code Generation LLM - Fine-Tuning Data Pipeline

This project demonstrates how to build a realistic, multi-stage data pipeline to prepare data for fine-tuning a code generation Large Language Model (LLM).

## Pipeline Stages

The pipeline is divided into four main, automated stages:

1.  **Extraction (`scripts/extract_from_repo.py`)**:
    -   Simulates processing a raw source, in this case a repository of Python code (`data/raw_code_repo/`).
    -   It uses a **context-aware, two-pass static analysis** to create self-contained, runnable code snippets. The first pass gathers all file-level imports and global constants.
    -   The second pass uses a memory-efficient streaming parser to extract individual functions, then prepends the file-level context to each one.
    -   The output is a structured `.jsonl` file of `{prompt, completion}` pairs, where the docstring is the prompt and the full, context-aware code snippet is the completion.

2.  **LLM-Powered Refinement (Simulation) (`scripts/simulate_llm_refinement.py`)**:
    -   Demonstrates a state-of-the-art technique for data cleaning and augmentation.
    -   It simulates using a powerful "teacher" LLM to judge the quality of existing docstrings.
    -   If a docstring is missing or judged to be low-quality, the script simulates a call to a generator LLM to create a new, high-quality docstring from the source code.

3.  **Processing & Validation (`scripts/run_pipeline.py`)**:
    -   Takes the refined data and validates it, ensuring the code is syntactically correct.
    -   Transforms the data into the Alpaca instruction-following format, which is ideal for fine-tuning.

4.  **Tokenization (`scripts/tokenize_data.py`)**:
    -   Loads the processed data and tokenizes it using a model-specific tokenizer (e.g., from CodeLlama).
    -   Saves the final, model-ready dataset in the efficient Apache Arrow format, ready for a training job.

This project serves as a practical example for the following MLOps concepts:
- Building multi-stage, chained data pipelines.
- Processing truly raw data sources (like code repositories) with context-aware static analysis.
- Ensuring data quality through validation and LLM-based refinement (simulated).
- Creating reusable, config-driven pipeline components.
- Preparing data for LLM fine-tuning from start to finish.

## Using a Real LLM for Data Refinement

The LLM-powered refinement stage (`scripts/simulate_llm_refinement.py`) defaults to running in **simulation mode**. It does *not* make real API calls, which allows you to run the entire pipeline without needing an API key or incurring costs.

To connect the pipeline to a real LLM (e.g., GPT-3.5/4), follow these steps:

### 1. Install the OpenAI Library
First, ensure you have the necessary client library installed:
```bash
pip install -r requirements.txt
```

### 2. Set Your API Key
For security, the script reads the API key from an environment variable. Set it in your terminal before running the script.

**On macOS/Linux:**
```bash
export OPENAI_API_KEY='your_secret_key_here'
```

**On Windows:**
```powershell
$env:OPENAI_API_KEY='your_secret_key_here'
```

### 3. Activate the Real API Calls
Open the script `scripts/simulate_llm_refinement.py` in your editor. At the top of the file, change the configuration flag from `False` to `True`:

```python
# Before
USE_REAL_LLM = False

# After
USE_REAL_LLM = True
```

Now, when you run the pipeline, the refinement script will make real API calls to judge and generate docstrings. Be aware that this will use tokens from your OpenAI account and will incur costs.

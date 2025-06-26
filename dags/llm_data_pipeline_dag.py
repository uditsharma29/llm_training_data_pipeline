from airflow.models.dag import DAG
from airflow.operators.bash import BashOperator
from datetime import datetime

# --- IMPORTANT ---
# This is the absolute path to the project directory on the user's machine.
# In a real production environment, this path would be configured to point to
# where the repository is checked out on the Airflow worker machines.
PROJECT_HOME = '/Users/uditsharma/code/llm_fine_tune_data_gen'


with DAG(
    dag_id='llm_data_pipeline',
    start_date=datetime(2024, 1, 1),
    description='A DAG to run the full LLM data preparation pipeline.',
    schedule_interval='@weekly',  # You can use cron expressions like '0 2 * * 0'
    catchup=False,
    tags=['llm', 'data-pipeline'],
) as dag:

    # Task 1: Extract data from the raw code repository
    task_extract = BashOperator(
        task_id='extract_from_repo',
        bash_command=f"python3 {PROJECT_HOME}/scripts/extract_from_repo.py"
    )

    # Task 2: Refine the data using the simulated LLM
    task_refine = BashOperator(
        task_id='simulate_llm_refinement',
        bash_command=f"python3 {PROJECT_HOME}/scripts/simulate_llm_refinement.py"
    )

    # Task 3: Process and validate the refined data
    task_process = BashOperator(
        task_id='run_processing_pipeline',
        bash_command=f"python3 {PROJECT_HOME}/scripts/run_pipeline.py"
    )

    # Task 4: Tokenize the final dataset
    task_tokenize = BashOperator(
        task_id='tokenize_data',
        bash_command=f"python3 {PROJECT_HOME}/scripts/tokenize_data.py"
    )

    # Define the execution order (the dependency graph)
    task_extract >> task_refine >> task_process >> task_tokenize 
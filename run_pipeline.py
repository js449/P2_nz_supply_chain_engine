import subprocess
import sys
import os

def run_command(command, stage_name, cwd=None):
    """Executes a terminal command and stops the pipeline on failure."""
    print(f"--- [STARTING] {stage_name} ---")
    
    # We use subprocess to run the command just like you do in the terminal
    result = subprocess.run(command, shell=True, cwd=cwd)
    
    if result.returncode != 0:
        print(f"\n!!! [ERROR] {stage_name} FAILED. Stopping pipeline to protect Gold reports. !!!")
        sys.exit(1)
    
    print(f"--- [SUCCESS] {stage_name} Completed ---\n")

# --- Step 1: Ingest Data (Python/Pydantic) ---
# This populates the Bronze layer
run_command("python ingestor/main.py", "Data Ingestion (Bronze Layer)")

# --- Step 2: dbt Build (Transformations & Tests) ---
# This runs Silver, Gold, and all Quality Tests in order
# We run this from the dbt_project directory
dbt_path = os.path.join(os.getcwd(), "dbt_project")
run_command("dbt build --profiles-dir .", "dbt Medallion Pipeline (Silver/Gold)", cwd=dbt_path)

print("==========================================")
print("NZ SUPPLY CHAIN ENGINE: PIPELINE SUCCESSFUL")
print("==========================================")
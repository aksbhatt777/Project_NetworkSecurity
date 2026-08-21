"""
Test DagsHub MLflow connection using dagshub.init()
Uses your saved local credentials - no environment variables needed!
"""
#if dagshub not initialised it wont work

import dagshub
import mlflow

# Your repository details
REPO_OWNER = "aksbhatt777"
REPO_NAME = "Project_NetworkSecurity"

print("Testing DagsHub MLflow connection")

# Initialize DagsHub with MLflow tracking
dagshub.init(repo_owner=REPO_OWNER, repo_name=REPO_NAME, mlflow=True)

# Test MLflow logging
with mlflow.start_run(run_name="init_test"):
    mlflow.log_param("test_method", "dagshub_init")
    mlflow.log_metric("test_score", 100)
    print("MLflow connection successful!")
    print(f"Run ID: {mlflow.active_run().info.run_id}")
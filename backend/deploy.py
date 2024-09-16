import os
from dotenv import load_dotenv
import subprocess

# Load environment variables from .env file
load_dotenv()

# Deploy Chalice app
deploy_result = subprocess.run(["chalice", "deploy"], capture_output=True, text=True)

# Check the deploy result
if deploy_result.returncode == 0:
    print("Successfully deployed Chalice app.")
else:
    print("Failed to deploy Chalice app.")
    print(deploy_result.stderr)

# Retrieve environment variables
var1 = os.getenv("BING_API_KEY")

# Define the AWS CLI command to set environment variables
command = [
    "aws",
    "lambda",
    "update-function-configuration",
    "--function-name",
    "localnews-finder-backend-dev",
    "--environment",
    f"Variables={{BING_API_KEY={var1}}}",
]

# Run the command
result = subprocess.run(command, capture_output=True, text=True)

# Check the result
if result.returncode == 0:
    print("Successfully updated environment variables.")
else:
    print("Failed to update environment variables.")
    print(result.stderr)

#!/bin/bash
export GCP_PROJECT='arctic-analyzer-435209-m1'  # Add your ProjectID
export GCP_REGION='europe-west3' # Add your Region
export GCP_BUCKET='demo_gradio_data' # Create a bucket for the temp uploaded files
export AR_REPO='cloud-run-source-deploy' # Create an artifact repository to store docker files
export SERVICE_NAME='hackathon-sample-app'
#either copy paste to Cloud Shell or run
#chmod +x initial.sh
#source ./initial.sh

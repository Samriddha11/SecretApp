from flask import Flask, jsonify
from featureflags.client import CfClient
from featureflags.evaluations.auth_target import Target
import boto3
import json

app = Flask(__name__)

# AWS Secrets Manager setup
def get_secret():
    secret_name = "harness_api_key"
    region_name = "us-east-1"  # Change this to your AWS region

    # Create a Secrets Manager client
    session = boto3.session.Session()
    client = session.client(service_name='secretsmanager', region_name=region_name)

    try:
        # Retrieve secret value
        get_secret_value_response = client.get_secret_value(SecretId=secret_name)
        secret = get_secret_value_response['SecretString']
        return json.loads(secret)['api_key']  # Assuming the key is stored as a JSON object
    except Exception as e:
        print(f"Error fetching API key from Secrets Manager: {e}")
        raise

# Define target for feature flag evaluation
beta_testers = Target(identifier="test1", name="test1", attributes={"org": "blue"})

@app.route('/feature_flag_status', methods=['GET'])
def get_feature_flag_status():
    try:
        # Fetch the API key from Secrets Manager
        api_key = get_secret()

        # Initialize the feature flag client with the latest API key
        client = CfClient(api_key)

        # Wait for client initialization
        client.wait_for_initialization()

        # Ensure client is initialized before evaluating feature flag
        if not client.is_initialized():
            return jsonify({"status": "Failed to Initialize"}), 500
        
        result = client.bool_variation("ChaosFeatureDemo", beta_testers, False)
        return jsonify({"status": result}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8989)

import json
import os   # access env. variables
import boto3    # AWS Python SDK   
from botocore.exceptions import ClientError # AWS-specific error handling

# client init
dynamodb = boto3.resource("dynamodb")
kms = boto3.client("kms")

# reads .env variables set in Lambda config
TABLE_NAME = os.environ.get("TABLE_NAME")
KMS_KEY_ID = os.environ.get("KMS_KEY_ID")

cors_headers = {
    "Access-Control-Allow-Origin": "https://d3um4w745sq9lj.cloudfront.net",
    "Access-Control-Allow-Headers": "Content-Type",
    "Access-Control-Allow-Methods": "POST,OPTIONS"
}

def lambda_handler(event, context):
    if event.get("httpMethod") == "OPTIONS":
        return {
            "statusCode": 200,
            "headers": cors_headers,
            "body": json.dumps({"message": "CORS preflight OK"})
        }

    try:
        # parses incoming request body
        body = json.loads(event.get("body", "{}"))
        name = body.get("name", "").strip()
        email = body.get("email", "").strip()
        message = body.get("message", "").strip()

        # input validation to ensure all fields are provided
        if not name or not email or not message:
            return {
                "statusCode": 400,
                "headers": cors_headers,
                "body": json.dumps({"error": "All fields are required."})
            }

        # encrypts message with KMS
        try:
            encrypted_response = kms.encrypt(
                KeyId=KMS_KEY_ID,
                Plaintext=message.encode("utf-8")
            )
            encrypted_message = encrypted_response["CiphertextBlob"]
        except ClientError as e:
            print(f"KMS Error: {e}")
            return {
                "statusCode": 500,
                "headers": cors_headers,
                "body": json.dumps({"error": "Encryption failed."})
            }

        # stores form data in DynamoDB table
        try:
            table = dynamodb.Table(TABLE_NAME)
            table.put_item(Item={
                "email": email,
                "name": name,
                "message": encrypted_message.hex()  # stores encrpyted message as hex string
            })
        except ClientError as e:
            print(f"DynamoDB Error: {e}")
            return {
                "statusCode": 500,
                "headers": cors_headers,
                "body": json.dumps({"error": "Database write failed."})
            }

        # returns success reponse after data is stored
        return {
            "statusCode": 200,
            "headers": cors_headers,
            "body": json.dumps({"message": "Form submitted securely."})
        }

    # catch-all error handling in case of unexpected errors
    except Exception as e:
        print(f"Unexpected Error: {e}")
        return {
            "statusCode": 500,
            "headers": cors_headers,
            "body": json.dumps({"error": "Unexpected error occurred."})
        }

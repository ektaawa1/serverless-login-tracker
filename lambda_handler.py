# lambda_handler.py
import json
import os
import time
import boto3
from boto3.dynamodb.conditions import Key

# DynamoDB resource - Lambda has AWS credentials via IAM role
dynamodb = boto3.resource("dynamodb")
TABLE_NAME = os.environ.get("TABLE_NAME", "LoginEvents")
table = dynamodb.Table(TABLE_NAME)

def lambda_handler(event, context):
    """
    Supports:
     - POST /login  (body JSON: {"userId": "...", "status": "success"|"failed"})
     - GET  /logins/{userId}
    Event shapes differ slightly between REST and HTTP APIs; this handler handles common shapes.
    """
    # Determine HTTP method (works for REST proxy and HTTP API)
    http_method = event.get("httpMethod") or event.get("requestContext", {}).get("http", {}).get("method")

    # --- POST: store login event ---
    if http_method == "POST":
        body = event.get("body", "{}")
        if isinstance(body, str):
            try:
                body = json.loads(body)
            except Exception:
                return {"statusCode": 400, "body": json.dumps({"message": "Invalid JSON body"})}

        user_id = body.get("userId")
        status = body.get("status", "success")
        if not user_id:
            return {"statusCode": 400, "body": json.dumps({"message": "userId required"})}

        ts = int(time.time())
        item = {
            "userId": user_id,
            "timestamp": ts,
            "status": status
        }
        table.put_item(Item=item)
        return {
            "statusCode": 200,
            "body": json.dumps({"message": "Login event recorded", "item": item})
        }

    # --- GET: query login events for a user ---
    if http_method == "GET":
        # REST API v1 puts path params in event['pathParameters']
        user_id = None
        if event.get("pathParameters"):
            user_id = event["pathParameters"].get("userId")
        # HTTP API v2 can also provide it under pathParameters
        if not user_id:
            user_id = event.get("pathParameters", {}).get("userId")

        if not user_id:
            return {"statusCode": 400, "body": json.dumps({"message": "userId path parameter required"})}

        # Query DynamoDB (latest first)
        resp = table.query(
            KeyConditionExpression=Key("userId").eq(user_id),
            ScanIndexForward=False,   # newest first
            Limit=50
        )
        items = resp.get("Items", [])
        return {
            "statusCode": 200,
            "body": json.dumps(items)
        }

    return {"statusCode": 400, "body": json.dumps({"message": "Unsupported method"})}

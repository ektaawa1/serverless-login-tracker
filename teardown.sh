#!/usr/bin/env bash
set -e

# Replace with your actual values if you know them
API_ID="<your-api-id>"
FUNC="login-tracker-function"
TABLE="LoginEvents"
ROLE="lambda-dynamodb-role"
LOGGROUP="/aws/lambda/$FUNC"

echo "Deleting API Gateway..."
aws apigatewayv2 delete-api --api-id "$API_ID" || true

echo "Deleting Lambda function..."
aws lambda delete-function --function-name "$FUNC" || true

echo "Deleting DynamoDB table..."
aws dynamodb delete-table --table-name "$TABLE" || true

echo "Detaching and deleting IAM role..."
for arn in $(aws iam list-attached-role-policies --role-name "$ROLE" --query 'AttachedPolicies[].PolicyArn' --output text); do
  aws iam detach-role-policy --role-name "$ROLE" --policy-arn "$arn" || true
done
for pol in $(aws iam list-role-policies --role-name "$ROLE" --query 'PolicyNames[]' --output text); do
  aws iam delete-role-policy --role-name "$ROLE" --policy-name "$pol" || true
done
aws iam delete-role --role-name "$ROLE" || true

echo "Deleting CloudWatch log group..."
aws logs delete-log-group --log-group-name "$LOGGROUP" || true

echo "Teardown complete."

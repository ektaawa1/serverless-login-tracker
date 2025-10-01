# Serverless User Login Tracker

A serverless user login tracker project using **AWS Lambda, API Gateway, and DynamoDB** (records and queries login events).  
It records user login events and allows querying login history in real time.

## How to run / test (Postman steps):
## POST an event
curl -X POST "https://<API_ID>.execute-api.<region>.amazonaws.com/prod/login" \
-H "Content-Type: application/json" \
-d '{"userId":"alice","status":"failed"}'

## GET events
curl "https://<API_ID>.execute-api.<region>.amazonaws.com/prod/logins/alice"



## Teardown (AWS cleanup)
To remove deployed resources and avoid charges:
1. Delete API in API Gateway (Console → API Gateway → APIs → Delete).
2. Delete Lambda function `login-tracker-function` (Console → Lambda → Functions → Delete).
3. Delete DynamoDB table `LoginEvents` (Console → DynamoDB → Tables → Delete).
4. Delete IAM Role `lambda-dynamodb-role` (Console → IAM → Roles → detach policies → Delete).
5. (Optional) Delete CloudWatch log group `/aws/lambda/login-tracker-function`.

CLI: see `teardown.sh` for a script to delete these resources (edit placeholders first).
 

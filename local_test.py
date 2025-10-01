# local_test.py
from lambda_handler import lambda_handler
event = {"httpMethod":"POST", "body": "{\"userId\": \"ekta\", \"status\":\"failed\"}"}
print(lambda_handler(event, None))

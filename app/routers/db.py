# Use this code snippet in your app.
# If you need more information about configurations
# or implementing the sample code, visit the AWS docs:
# https://aws.amazon.com/developer/language/python/

import boto3
import psycopg2
from botocore.exceptions import ClientError
import json
import os
from dotenv import load_dotenv

load_dotenv()

def get_secret():

  secret_name = "rds!cluster-691c662e-3952-4785-86d7-c9b346d9e27a"
  region_name = "eu-north-1"

  # Create a Secrets Manager client
  session = boto3.session.Session()
  client = session.client(
    service_name='secretsmanager',
    region_name=region_name,
    aws_access_key_id=os.getenv("AWS_ACCESS_KEY"),
    aws_secret_access_key=os.getenv("AWS_SECRET_KEY")
  )

  try:
    get_secret_value_response = client.get_secret_value(
      SecretId=secret_name
    )
  except ClientError as e:
    # For a list of exceptions thrown, see
    # https://docs.aws.amazon.com/secretsmanager/latest/apireference/API_GetSecretValue.html
    raise e

  secret = get_secret_value_response['SecretString']

  return json.loads(secret)


def connect_to_db():
  secret = get_secret()
  print(secret)


  db_host = os.getenv("AWS_HOST")
  db_port = 5432
  db_user = secret['username']
  db_password = secret['password']

  try:
    conn = psycopg2.connect(
      host=db_host,
      port=db_port,
      user=db_user,
      password=db_password
    )
    cursor = conn.cursor()
    print("Connected")

    # Example query
    cursor.execute("SELECT version();")
    db_version = cursor.fetchone()
    print("Database version:", db_version)

    cursor.close()
    conn.close()

  except Exception as e:
    print(f"Error connecting to the database: {e}")

if __name__ == "__main__":
  connect_to_db()

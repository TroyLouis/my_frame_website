import boto3
from my_frame.config import Config

s3 = boto3.client(
   "s3",
   aws_access_key_id=Config.S3_KEY,
   aws_secret_access_key=Config.S3_SECRET
)

s3_resource = boto3.resource('s3')
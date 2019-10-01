"""
Grab data, start with Reddit, as json blobs and store them in S3.
1. Connect to reddit
2. Grab json data
3. Store json in S3
"""
import boto3
import json

s3 = boto3.resource('s3')
obj = s3.Object('wsankey-capstone','hello.json')
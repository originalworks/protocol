import json
import boto3
from iscc_sdk import iscc_generate
import os
import tempfile

s3_client = boto3.client('s3')

def lambda_handler(event, context):
    bucket_name = event['bucket_name']
    media_files = event['media_files']  # List of S3 keys of media files
    iscc_codes = []

    # Create a temporary directory for downloading files
    with tempfile.TemporaryDirectory() as tmp_dir:
        for s3_key in media_files:
            file_name = s3_key.split('/')[-1]
            file_path = os.path.join(tmp_dir, file_name)

            # Download the media file from S3
            s3_client.download_file(bucket_name, s3_key, file_path)

            # Generate the ISCC code for the file
            iscc_code = iscc_generate(file_path)

            # Append the file and its ISCC code to the list
            iscc_codes.append({
                's3_key': s3_key,  # S3 location of the file
                'file_name': file_name,
                'iscc_code': iscc_code
            })

    return {
        'statusCode': 200,
        'iscc_data': iscc_codes,
        'bucket_name': bucket_name,
        'all_files': event['all_files']  # Pass all files along for CID generation
    }

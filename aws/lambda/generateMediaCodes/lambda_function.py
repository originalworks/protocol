import json
import boto3
import zipfile
import os
import tempfile
from iscc_sdk import iscc_generate
from cid import make_cid
import multihash

s3_client = boto3.client('s3')

def lambda_handler(event, context):
    # Extract S3 bucket and file information from the event
    bucket_name = event['Records'][0]['s3']['bucket']['name']
    zip_key = event['Records'][0]['s3']['object']['key']

    # Download the ZIP file to a temporary directory
    with tempfile.TemporaryDirectory() as tmp_dir:
        zip_path = os.path.join(tmp_dir, 'file.zip')
        s3_client.download_file(bucket_name, zip_key, zip_path)

        # Unzip the downloaded file
        with zipfile.ZipFile(zip_path, 'r') as zip_ref:
            zip_ref.extractall(tmp_dir)

        # Process each file in the extracted directory
        for root, _, files in os.walk(tmp_dir):
            for file in files:
                file_path = os.path.join(root, file)
                if file_path.endswith(('.mp3', '.mp4', '.wav', '.flac')):  # Add other media types if needed
                    # Generate ISCC Code
                    iscc_code = iscc_generate(file_path)
                    
                    # Generate CIDv1
                    with open(file_path, 'rb') as f:
                        file_data = f.read()
                        digest = multihash.digest(file_data, 'sha2-256')
                        cidv1 = make_cid(1, 'raw', digest)

                    # Output or store the ISCC code and CID
                    print(f"ISCC: {iscc_code}, CIDv1: {cidv1}")

    return {
        'statusCode': 200,
        'body': json.dumps('Processing completed')
    }


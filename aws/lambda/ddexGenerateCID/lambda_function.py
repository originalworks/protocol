import json
import boto3
from ipfs_cid import cid_sha256_hash
import os
import tempfile

s3_client = boto3.client('s3')

def lambda_handler(event, context):
    bucket_name = event['bucket_name']
    iscc_data = event['iscc_data']  # List of ISCC data with media files and ISCC codes
    all_files = event['all_files']  # List of all files from the unzip process
    final_output = []

    # Create a temporary directory for downloading files
    with tempfile.TemporaryDirectory() as tmp_dir:
        for s3_key in all_files:
            file_name = s3_key.split('/')[-1]
            file_path = os.path.join(tmp_dir, file_name)

            # Download the file from S3
            s3_client.download_file(bucket_name, s3_key, file_path)

            # Generate the CIDv1 hash using ipfs-cid
            with open(file_path, 'rb') as f:
                file_data = f.read()
                cidv1 = cid_sha256_hash(file_data)

            # Try to find the ISCC code if it exists
            iscc_code = next((item['iscc_code'] for item in iscc_data if item['s3_key'] == s3_key), None)

            # Append the final result with file name, ISCC code (if any), and CIDv1
            final_output.append({
                'file_name': file_name,
                'iscc_code': iscc_code,  # This will be None for non-media files
                'cidv1': cidv1
            })

    return {
        'statusCode': 200,
        'output': final_output  # Final JSON with file name, ISCC, and CIDv1
    }

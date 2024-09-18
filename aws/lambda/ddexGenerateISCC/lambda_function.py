import json
import boto3
from iscc_sdk import iscc_generate, dirs
import os

# Set the user data directory to a writable location
dirs.user_data_dir = '/tmp/iscc_sdk'

s3_client = boto3.client('s3')

def lambda_handler(event, context):
    try:
        bucket_name = event['bucket_name']
        media_files = event.get('media_files', [])  # List of S3 keys of media files
        iscc_codes = []

        # Create a temporary directory for downloading files
        with tempfile.TemporaryDirectory() as tmp_dir:
            for s3_key in media_files:
                file_name = s3_key.split('/')[-1]
                file_path = os.path.join(tmp_dir, file_name)

                try:
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
                except Exception as e:
                    print(f"Error processing {s3_key}: {str(e)}")

        return {
            'statusCode': 200,
            'iscc_data': iscc_codes,
            'bucket_name': bucket_name,
            'all_files': event.get('all_files', [])  # Pass all files along for CID generation
        }

    except Exception as e:
        print(f"Error: {str(e)}")
        return {
            'statusCode': 500,
            'error': str(e)
        }

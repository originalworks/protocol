import json
import boto3
import zipfile
import os
import tempfile

s3_client = boto3.client('s3')

def lambda_handler(event, context):
    bucket_name = event['bucket_name']
    zip_key = event['zip_key']  # Example: "example/file1.zip"

    # Extract the base file name from the zip_key (e.g., "file1")
    base_name = os.path.splitext(os.path.basename(zip_key))[0]
    
    # Create a temporary directory
    with tempfile.TemporaryDirectory() as tmp_dir:
        zip_path = os.path.join(tmp_dir, 'file.zip')

        # Download the ZIP file from S3
        s3_client.download_file(bucket_name, zip_key, zip_path)

        all_files = []
        media_files = []

        # Unzip the file
        with zipfile.ZipFile(zip_path, 'r') as zip_ref:
            zip_ref.extractall(tmp_dir)

        # Upload extracted media and non-media files back to S3
        for root, _, files in os.walk(tmp_dir):
            for file in files:
                file_path = os.path.join(root, file)
                # Create a new S3 key for each file (e.g., "example/unzipped/file1/file.mp3")
                new_key = f'example/unzipped/{base_name}/{file}'
                
                # Upload the file to S3
                s3_client.upload_file(file_path, bucket_name, new_key)

                # Add the uploaded file's S3 path to the all_files list
                all_files.append(new_key)

                # Check if the file is a media file
                if file_path.endswith(('.mp3', '.mp4', '.wav', '.flac')):
                    media_files.append(new_key)

    return {
        'statusCode': 200,
        'all_files': all_files,  # List of all S3 keys of unzipped files
        'media_files': media_files,  # List of media S3 keys only
        'bucket_name': bucket_name  # Return the bucket name as well
    }

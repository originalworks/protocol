import os
import json
import boto3
from iscc_sdk import iscc_generate, dirs
import tempfile

# Set HOME to a writable directory before importing iscc_sdk or other modules
os.environ['HOME'] = '/tmp'

# Update all dirs to point to /tmp
dirs.user_data_dir = '/tmp/iscc_sdk/data'
dirs.user_cache_dir = '/tmp/iscc_sdk/cache'
dirs.user_config_dir = '/tmp/iscc_sdk/config'

s3_client = boto3.client('s3')

def process_files(bucket_name, media_files):
    try:
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
            'status': 'success',
            'iscc_data': iscc_codes,
            'bucket_name': bucket_name
        }
    except Exception as e:
        print(f"Error: {str(e)}")
        return {
            'status': 'error',
            'error_message': str(e)
        }

def main():
    # Simulate receiving input (can be adapted to ECS event triggers)
    input_data = {
        "bucket_name": "ddex-messages-dev",
        "media_files": [
            "Revelator_750x372.jpg"
        ]
    }

    # Call the function to process files
    result = process_files(input_data['bucket_name'], input_data['media_files'])

    # Print the result (or log it for monitoring)
    print(json.dumps(result, indent=4))

if __name__ == "__main__":
    main()


from google.cloud import storage
from google.oauth2.service_account import Credentials
import json
import os 


# DESC: Google Cloud Storage Init

project_id = 'twittersheet-275317'
creds = Credentials.from_service_account_file('creds.json')
client = storage.Client(project=project_id, credentials=creds)

def upload_to_bucket(blob_name, path_to_file, bucket_name):
    """ Upload data to a bucket"""

    #print(buckets = list(storage_client.list_buckets())

    bucket = client.get_bucket(bucket_name)
    blob = bucket.blob(blob_name)
    blob.upload_from_filename(path_to_file)

    print(f"File {path_to_file} uploaded to {bucket_name}.")

# upload_to_bucket("main.py", "main.py", "twittersheet-275317")

save_location = os.path.join(os.getcwd(), 'attachments')
    
if os.path.exists(save_location):
    files = os.listdir(save_location)
    for file in files:
        upload_to_bucket(file, "attachments/"+file, "twittersheet-275317")
        file_path = "attachments/"+file
        try:
            if os.path.isfile(file_path):
                    os.unlink(file_path)
            elif os.path.isdir(file_path): shutil.rmtree(file_path)
        except Exception as e:
            print(f"Failed to delete {file_path}. Reason: {e}")
else:
    print("No 'attachments' directory found.")
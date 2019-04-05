from google.cloud import storage
from time import gmtime, strftime
import json

def upload_blob(bucket_name, blob_text, destination_blob_name):
    """Uploads a file to the bucket."""
    storage_client = storage.Client()
    bucket = storage_client.get_bucket(bucket_name)
    blob = bucket.blob(destination_blob_name)

    blob.upload_from_string(blob_text)

    print('File {} uploaded to {}.'.format(
        destination_blob_name,
        bucket_name))


def get_existing_file(bucket, filename):
    storage_client = storage.Client()
    bucket = storage_client.get_bucket(bucket)
    blob = bucket.blob(filename)

    return json.loads(blob.download_as_string())


def log_tip(request):
    # Set CORS headers for preflight requests
    if request.method == 'OPTIONS':
        # Allows GET requests from origin https://mydomain.com with
        # Authorization header
        headers = {
            'Access-Control-Allow-Origin': 'https://mydomain.com',
            'Access-Control-Allow-Methods': 'GET',
            'Access-Control-Allow-Headers': 'Authorization',
            'Access-Control-Max-Age': '3600',
            'Access-Control-Allow-Credentials': 'true'
        }
        return ('', 204, headers)

    # Set CORS headers for main requests
    headers = {
        'Access-Control-Allow-Origin': 'https://mydomain.com',
        'Access-Control-Allow-Credentials': 'true'
    }

    return ('Hello World!', 200, headers)
    request_json = request.get_json()
    BUCKET_NAME = 'cabin-6598-tips'
    BLOB_NAME = 'tips.json'

    current = get_existing_file(BUCKET_NAME, BLOB_NAME)
    if 'tips' not in current.keys():
        current['tips'] = []

    current['tips'].append(request_json['tipText'])
    output = json.dumps(current)

    upload_blob(BUCKET_NAME, output, BLOB_NAME)

    response.headers.set('Access-Control-Allow-Origin', '*')
    response.headers.set('Access-Control-Allow-Methods', 'GET, POST')
    return ('Success!', 200, headers)

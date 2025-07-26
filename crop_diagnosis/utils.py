from google.cloud import storage
import uuid

def upload_image_to_gcs(file, bucket_name, folder='vegetables'):
    client = storage.Client()
    bucket = client.bucket(bucket_name)
    filename = f"{folder}/{uuid.uuid4()}.{file.name.split('.')[-1]}"
    blob = bucket.blob(filename)
    blob.upload_from_file(file, content_type=file.content_type)
    blob.make_public()
    return blob.public_url
from google.cloud import storage
import uuid

def upload_image_to_gcs(file_obj, bucket_name, folder_name='community'):
    client = storage.Client()
    bucket = client.bucket(bucket_name)
    
    # Generate unique file name
    ext = file_obj.name.split('.')[-1]
    filename = f"{folder_name}/{uuid.uuid4()}.{ext}"
    
    blob = bucket.blob(filename)
    blob.upload_from_file(file_obj, content_type=file_obj.content_type)
    
    # Make public
    blob.make_public()
    
    return blob.public_url

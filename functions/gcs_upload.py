import io
import nbformat
from google.cloud import storage

def upload_notebook_to_gcs(nb, bucket_name, blob_path, service_account_file):
    """
    Upload a notebook object directly to GCS without saving locally.
    Maintains folder structure using blob_path.
    """
    client = storage.Client.from_service_account_json(service_account_file)
    bucket = client.bucket(bucket_name)

    # Convert notebook object to string in memory
    notebook_bytes = io.StringIO()
    nbformat.write(nb, notebook_bytes)
    notebook_bytes.seek(0)

    # Upload to GCS
    blob = bucket.blob(blob_path.replace("\\", "/"))
    blob.upload_from_string(notebook_bytes.getvalue(), content_type="application/x-ipynb+json")

    gcs_path = blob_path.replace("\\", "/")
    print(f"Upload completed to gs://{bucket_name}/{gcs_path}")

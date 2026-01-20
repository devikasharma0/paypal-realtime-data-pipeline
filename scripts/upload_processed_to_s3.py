import boto3
from pathlib import Path

BUCKET_NAME = "paypal-data-pipeline-dev"
REGION = "eu-north-1"

PROJECT_ROOT = Path(__file__).resolve().parent.parent
PROCESSED_DIR = PROJECT_ROOT / "data" / "processed"

if not PROCESSED_DIR.exists():
    raise FileNotFoundError("Processed directory not found")

s3 = boto3.client("s3", region_name=REGION)

for file in PROCESSED_DIR.iterdir():
    if file.is_file():
        s3_key = f"processed/payments/{file.name}"
        s3.upload_file(str(file), BUCKET_NAME, s3_key)
        print(f"✅ Uploaded {file.name} → s3://{BUCKET_NAME}/{s3_key}")
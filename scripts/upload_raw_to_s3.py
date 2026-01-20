import boto3
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables (optional but safe)
load_dotenv()

# ==========================
# CONFIG
# ==========================
BUCKET_NAME = "paypal-data-pipeline-dev"
REGION = "eu-north-1"

# ==========================
# PATH RESOLUTION
# ==========================
PROJECT_ROOT = Path(__file__).resolve().parent.parent
RAW_DIR = PROJECT_ROOT / "data" / "raw"

print(f"📂 Looking for raw files in: {RAW_DIR}")

# ==========================
# VALIDATION
# ==========================
if not RAW_DIR.exists():
    raise FileNotFoundError(f"❌ Raw directory does not exist: {RAW_DIR}")

raw_files = list(RAW_DIR.iterdir())
if not raw_files:
    raise RuntimeError("❌ Raw directory exists but contains no files")

# ==========================
# S3 CLIENT
# ==========================
s3 = boto3.client(
    "s3",
    region_name=REGION
)

# ==========================
# UPLOAD
# ==========================
for file_path in raw_files:
    if file_path.is_file():
        s3_key = f"raw/paypal/{file_path.name}"

        s3.upload_file(
            Filename=str(file_path),
            Bucket=BUCKET_NAME,
            Key=s3_key
        )

        print(f"✅ Uploaded {file_path.name} → s3://{BUCKET_NAME}/{s3_key}")

print("🎉 All raw files uploaded successfully.")
# Mailchimp Extract & Load

Two approaches for extracting Mailchimp data:

## 1) Airbyte Extract and Load

**AWS Setup:**
- Created `mailchimp-airbyte/` folder in S3 bucket
- Configured Airbyte destination using KMS encryption key (reused from previous Airbyte project)
- Updated IAM user policy with object-level permissions for the new folder:
  - Modified List, Get, and Put action roots to include new bucket path
  - Same IAM user as Amplitude project

**Airbyte Configuration:**
- Source: Mailchimp connector
- Destination: S3 with KMS encryption
- Output location: `s3://bucket/mailchimp-airbyte/`

## 2) Python Extract and Load

**AWS Config:**
- Created `mailchimp-python/` folder in S3 bucket
- Updated Python IAM policy (previously used for Amplitude) to include permissions for new bucket folder
- Added List, Get, and Put permissions for `mailchimp-python/*` path

**VSCode Setup:**
```bash
# Environment setup
python -m venv venv
pip install mailchimp-marketing boto3 python-dotenv
pip freeze > requirements.txt
git commit -m "Initial setup"

# Development
git checkout -b dev
# Created .env with AWS and Mailchimp credentials
# Built extract.py
```

**Script Functionality:**
- Extracts campaign data from Mailchimp API
- Saves locally to `data/` folder as timestamped JSON
- Uploads to S3: `s3://bucket/mailchimp-python/Campaigns_YYYYMMDD_HHMMSS.json`
- Deletes local copy after successful upload
- Logs all operations to `logs/` folder

**Key Implementation Details:**
- Uses context managers (`with open()`) for safe file handling
- `json.dump()` with `indent=2` for readable output
- boto3 S3 client for uploads
- Automatic cleanup of local files post-upload

## Project Structure
```
mailchimp/
├── data/                          # Temp local storage (gitignored)
├── logs/                          # Execution logs (gitignored)
├── venv/                          # Virtual environment (gitignored)
├── .env                           # Credentials (gitignored)
├── mailchimp_extract_events.py   # Main extraction script
├── requirements.txt
└── README.md
```

## Usage
```bash
# Activate environment
source venv/bin/activate

# Run extraction
python mailchimp_extract_events.py

# Check output
aws s3 ls s3://bucket/mailchimp-python/
```
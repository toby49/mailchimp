# Define Logging
import logging
from datetime import datetime, timezone

# Set Log filepath location
log_filename = f"logs/mailchimp_extract_events_{datetime.now().strftime('%Y%m%d_%H%M%S')}.log"

# Configure logs to retrieve INFO messages and higher
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    filename=log_filename
)

logger = logging.getLogger()

# Load libraries
import os
import boto3
import json
from dotenv import load_dotenv
from mailchimp_marketing import Client
from mailchimp_marketing.api_client import ApiClientError

logger.info('Libraries Loaded')

# Load .env file
load_dotenv()

# Define variables
aws_access_key=os.getenv('aws_access_key')
aws_secret_key=os.getenv('aws_secret_key')
aws_bucket=os.getenv('aws_bucket')

api_key = os.getenv('api_key')
server_prefix = os.getenv('server_prefix')

# Make the GET request 
try: 
    mailchimp = Client()
    mailchimp.set_config({
    "api_key": api_key,
    "server": server_prefix
    })
    # Make the GET request to the /campaigns endpoint to list all campaigns
    response = mailchimp.campaigns.list()
    logger.info('Data extracted')
    
    # Construct file name with data folder path
    file = f"data/Campaigns_{datetime.now(timezone.utc).strftime('%Y%m%d_%H%M%S')}.json"
    
    # Save response to file
    with open(file, 'w') as f:
        json.dump(response, f, indent=2)
    
    logger.info(f'Data saved to {file}')
    print(f"Data saved to: {file}")

     # Upload to S3
    s3_client = boto3.client(
        's3',
        aws_access_key_id=aws_access_key,
        aws_secret_access_key=aws_secret_key
    )
    
    # Set S3 key with mailchimp-python folder prefix
    s3_key = f"mailchimp-python/{os.path.basename(file)}"
    
    # Upload local file to S3
    s3_client.upload_file(file, aws_bucket, s3_key)
    logger.info(f'Data uploaded to S3: s3://{aws_bucket}/{s3_key}')
    print(f"Data uploaded to S3: s3://{aws_bucket}/{s3_key}")
    
    # Delete local file
    os.remove(file)
    logger.info(f'Local file deleted: {file}')
    print(f"Local file deleted: {file}")
    
except ApiClientError as error:
    logger.error("Error: {}".format(error.text))
except Exception as e:
    logger.error(f"Unexpected error: {str(e)}")


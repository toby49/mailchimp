# Define Logging
import logging
from datetime import datetime

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
from dotenv import load_dotenv
from mailchimp_marketing import Client
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

mailchimp = Client()
mailchimp.set_config({
  "api_key": api_key,
  "server": server_prefix
})

response = mailchimp.ping.get()
print(response)
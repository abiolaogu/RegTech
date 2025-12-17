import os
import shutil
import boto3
from botocore.exceptions import NoCredentialsError

# --- Storage Service ---

class StorageService:
    def __init__(self, provider='local', bucket_name='regtech-reports'):
        self.provider = provider
        self.bucket_name = bucket_name
        self.local_storage_path = os.path.join(os.getcwd(), 'storage')
        
    def upload_file(self, file_path: str, destination_name: str) -> str:
        """
        Uploads a file to the configured storage provider.
        Returns the clickable URL or path.
        """
        if self.provider == 'local':
            os.makedirs(self.local_storage_path, exist_ok=True)
            dest_path = os.path.join(self.local_storage_path, destination_name)
            shutil.copy(file_path, dest_path)
            return f"file://{dest_path}"
        
        elif self.provider == 's3':
            # This requires AWS credentials to be configured in env
            s3 = boto3.client('s3')
            try:
                s3.upload_file(file_path, self.bucket_name, destination_name)
                # Generate a signed URL valid for 1 hour
                url = s3.generate_presigned_url(
                    'get_object',
                    Params={'Bucket': self.bucket_name, 'Key': destination_name},
                    ExpiresIn=3600
                )
                return url
            except NoCredentialsError:
                print("Credentials not available for S3 upload")
                return ""
            except Exception as e:
                print(f"Failed to upload to S3: {e}")
                return ""
        
        return ""

# --- Notification Service ---

class NotificationService:
    def send_email(self, recipient: str, subject: str, body: str):
        """
        Mock email sender. In production, use SMTP or SES.
        """
        print(f"--- EMAIL SENT TO {recipient} ---")
        print(f"Subject: {subject}")
        print(f"Body: {body}")
        print("-------------------------------")

    def send_slack_alert(self, channel: str, message: str):
        """
        Mock Slack sender.
        """
        print(f"--- SLACK ALERT TO {channel} ---")
        print(f"Message: {message}")
        print("--------------------------------")

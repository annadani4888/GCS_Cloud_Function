import os
import zipfile
import shutil
import subprocess
from google.cloud import storage

def install_rclone():
    try:
        # Define paths
        rclone_zip_path = "/tmp/rclone.zip"
        rclone_extracted_dir = "/tmp/rclone-v1.68.2-linux-amd64"
        rclone_binary_path = f"{rclone_extracted_dir}/rclone"

        # Ensure no leftover files from previous runs
        if os.path.exists(rclone_extracted_dir):
            shutil.rmtree(rclone_extracted_dir)
        if os.path.exists(rclone_zip_path):
            os.remove(rclone_zip_path)

        # Download the rclone zip file
        subprocess.run(["curl", "-o", rclone_zip_path, "-L",
                        "https://downloads.rclone.org/v1.68.2/rclone-v1.68.2-linux-amd64.zip"], check=True)

        # Unzip the rclone archive
        subprocess.run(["unzip", rclone_zip_path, "-d", "/tmp/"], check=True)

        # Ensure the binary exists
        if not os.path.isfile(rclone_binary_path):
            raise FileNotFoundError(f"Expected rclone binary not found at: {rclone_binary_path}")

        # Make the rclone binary executable
        subprocess.run(["chmod", "+x", rclone_binary_path], check=True)

        print(f"Rclone installed successfully at {rclone_binary_path}")
        return rclone_binary_path

    except subprocess.CalledProcessError as e:
        print(f"Error during subprocess execution: {e}")
        raise
    except Exception as e:
        print(f"General error installing rclone: {e}")
        raise


def setup_rclone_config():
    """Set up the rclone configuration for OTC and GCS remotes."""
    try:
        # Use /tmp for better compatibility with GCP Functions
        rclone_config_dir = "/tmp/rclone_config"
        rclone_config_file = f"{rclone_config_dir}/rclone.conf"

        # Ensure the config directory exists
        os.makedirs(rclone_config_dir, exist_ok=True)

        # Retrieve environment variables for OTC
        otc_access_key = os.environ.get("OTC_ACCESS_KEY")
        otc_secret_key = os.environ.get("OTC_SECRET_KEY")
        otc_endpoint = os.environ.get("OTC_ENDPOINT")

        if not otc_access_key or not otc_secret_key or not otc_endpoint:
            raise ValueError("Missing required environment variables for OTC configuration")

        # Retrieve environment variables for GCS
        gcs_service_account_file = os.environ.get("GCS_SERVICE_ACCOUNT_FILE")

        if not gcs_service_account_file:
            raise ValueError("Missing required environment variable: GCS_SERVICE_ACCOUNT_FILE")

        # Write the rclone config file
        with open(rclone_config_file, "w") as f:
            # OTC Remote
            f.write("[otc]\n")
            f.write("type = s3\n")
            f.write("provider = Other\n")
            f.write(f"access_key_id = {otc_access_key}\n")
            f.write(f"secret_access_key = {otc_secret_key}\n")
            f.write(f"endpoint = {otc_endpoint}\n\n")

            # GCS Remote
            f.write("[gcs]\n")
            f.write("type = google cloud storage\n")
            f.write(f"service_account_file = {gcs_service_account_file}\n")

        print(f"Rclone config file created at {rclone_config_file}")
        return rclone_config_file

    except Exception as e:
        print(f"Error setting up rclone config: {e}")
        raise


def copy_to_otc(rclone_path, rclone_config_file, bucket_name, folder_name):
    """Copy the processed folder to OTC using rclone."""
    source_path = f"gcs:{bucket_name}/{folder_name}"  # Use the GCS remote for the source
    destination_path = "otc:planet-data-prod"  # OTC bucket path

    # Rclone copy command
    command = [
        rclone_path,  # Full path to the rclone binary
        "copy",       # Copy command
        source_path,  # Source path using GCS remote
        destination_path,  # Destination path using OTC remote
        "--config", rclone_config_file  # Path to the rclone config file
    ]

    # Execute the rclone command
    result = subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    if result.returncode == 0:
        print(f"Successfully copied {folder_name} to OTC.")
    else:
        print(f"Error copying {folder_name} to OTC: {result.stderr.decode()}")


# MAIN TRIGGER FUNCTION
def gcs_rclone_delivery(event, context):
    """Triggered by the creation or update of a GCS object."""
    print(f"Event received: {event}")

    bucket_name = event['bucket']
    file_path = event['name']

    # Filter files not in the desired folder
    if not file_path.startswith('processed/'):  # Replace with sub-folder name
        print(f"Skipping file not in 'processed-data/' folder: {file_path}")
        return

    # Proceed with your rclone delivery logic
    print(f"File {file_path} in 'processed-data/' folder. Proceeding...")
    rclone_path = install_rclone()
    rclone_config = setup_rclone_config()
    copy_to_otc(rclone_path, rclone_config, bucket_name, file_path)



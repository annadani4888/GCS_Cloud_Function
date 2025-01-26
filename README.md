## GCS-to-OTC Data Delivery Using Google Cloud Functions
This repository contains a Google Cloud Function designed to automate the transfer of data from a Google Cloud Storage (GCS) bucket to an OTC (Open Telekom Cloud) bucket. The function utilizes **rclone** to perform the transfer, addressing the lack of direct interoperability between GCS and OTC.

**Use Case**

This script was developed to facilitate the recurring delivery of processed satellite data from a GCS bucket to a client’s OTC bucket, ensuring secure and efficient transfers with minimal manual intervention.


**Features**:
-   **Automated Trigger**: The function is triggered by the creation or update of objects in a specified GCS folder.
-   **Dynamic Configuration**: Configures rclone at runtime using environment variables.
-   **Secure Credentials Handling**: Credentials for GCS and OTC are passed through environment variables and a configuration file.
-   **Reusable Script**: Designed for scalability and adaptability to similar cloud transfer tasks.

**Repository Structure**
The repository includes the following essential files:
-   **`main.py`**: The primary Python script that defines the Cloud Function. Handles rclone installation, configuration, and execution.
-   **`deployment.sh`**: Contains deployment parameters for the Google Cloud Function, such as `--trigger-resource` and `--entry-point`.
-   **`env.yaml`**: Stores environment variables, including OTC access keys and the GCS Service Account file location.
-   **`requirements.txt`**: Lists Python dependencies for the Cloud Function.
-   **GCS Service Account JSON**: The credentials file for GCS authentication (A dummy credentials file is included in the repository for demonstration purposes. Replace this with the actual GCS service account file for proper functionality).

**Prerequisites**
-   **Google Cloud Platform**: Set up a GCS bucket and enable Cloud Functions.
-   **Open Telekom Cloud**: Ensure access to an S3-compatible OTC bucket.
-   **Environment Variables**: Define the following in `env.yaml`:
    -   `OTC_ACCESS_KEY`: OTC access key.
    -   `OTC_SECRET_KEY`: OTC secret key.
    -   `OTC_ENDPOINT`: OTC S3 endpoint.
    -   `GCS_SERVICE_ACCOUNT_FILE`: Path to the GCS Service Account JSON file.

**How It Works**
1.  **Trigger**: The function is triggered when a new object is created or updated in the GCS bucket.
2.  **Install rclone**: The script downloads and configures rclone dynamically in the Cloud Function environment.
3.  **Setup rclone Config**: An rclone configuration file is generated at runtime using the provided environment variables.
4.  **Transfer Data**: The script uses rclone to transfer data from the GCS bucket to the OTC bucket.

**Limitations**

**Folder-Specific Triggering**: Currently hardcoded to transfer files from the `processed/` GCS source folder; modify as needed for your use case.

**Acknowledgments**

This solution leverages **Google Cloud Functions** and **rclone** to overcome cross-cloud transfer challenges, combining scalability with platform-agnostic compatibility

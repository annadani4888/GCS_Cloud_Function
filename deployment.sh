#!/bin/bash
gcloud functions deploy gcs_rclone_delivery \
  --runtime python310 \
  --trigger-resource esa-dwh-2024 \
  --trigger-event google.storage.object.finalize \
  --entry-point gcs_rclone_delivery \
  --region europe-west1 \
  --memory 2GiB \
  --timeout 300s \
  --env-vars-file env.yaml

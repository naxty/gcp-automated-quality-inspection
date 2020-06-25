# Automl

1. Create GCS and upload data
```sh
gsutil mb -p $PROJECT_ID  -l $BUCKET_LOCATION -b on gs://$BUCKET_NAME
gsutil -m cp -r ../data gs://$BUCKET_NAME
```

2. Run [prepare.py](prepare.py)
3. Upload preparation.csv to the bucket
```sh
gsutil cp preparation.csv gs://$BUCKET_NAME
```
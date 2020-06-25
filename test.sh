set -a
. ./config
set +a

## upload scratches pics to inbound bucket
gsutil cp data/sample_pics/test_pic_ok.jpeg gs://"${INBOUND_BUCKET}"
gsutil cp data/sample_pics/test_pic_def.jpeg gs://"${INBOUND_BUCKET}"

## wait a little for processing
sleep 60

### delete file from bucket in case of failure
gsutil rm gs://"${INBOUND_BUCKET}"/test_pic_ok.jpeg
gsutil rm gs://"${INBOUND_BUCKET}"/test_pic_def.jpeg

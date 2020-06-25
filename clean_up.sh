set -a
. ./config
set +a

## Delete the pubsub topic
gcloud pubsub topics delete $PREDICTION_TOPIC

## Delete all objects and buckets
gsutil rm -r gs://${INBOUND_BUCKET}
gsutil rm -r gs://${PREDICTION_BUCKET}

## Delete cloud functions
gcloud functions delete $PREDICT_CF_NAME --quiet
gcloud functions delete $MOVE_CF_NAME --quiet

## Undeploy autoML model
#curl -X POST \
#-H "Authorization: Bearer "$(gcloud auth application-default print-access-token) \
#-H "Content-Type: application/json; charset=utf-8" \
#-d "" \
#https://automl.googleapis.com/v1beta1/projects/"$(gcloud config get-value project)"/locations/us-central1/models/"${MODEL_ID}":undeploy

#curl -X POST \
#-H "Authorization: Bearer "$(gcloud auth application-default print-access-token) \
#-H "Content-Type: application/json; charset=utf-8" \
#-d "" \
#https://automl.googleapis.com/v1/projects/"$(gcloud config get-value project)"/locations/us-central1/models/"${MODEL_ID}":undeploy
set -a
. ./config
set +a

## Create bucket inbound bucket
echo "create bucket $INBOUND_BUCKET"
gsutil mb -c standard -l europe-west3 gs://"${INBOUND_BUCKET}"

## Create bucket predict bucket
echo "create bucket $PREDICTION_BUCKET"
gsutil mb -c standard -l europe-west3 gs://"${PREDICTION_BUCKET}"

## Create PubSub Topic
echo "create pubsub topic $PREDICTION_TOPIC"
gcloud pubsub topics create "$PREDICTION_TOPIC"

## Deploy cloud function with new file trigger for bucket
echo "deploy cloud function $PREDICT_CF_NAME triggered by new files in $INBOUND_BUCKET"
gcloud functions deploy "$PREDICT_CF_NAME" \
 --source "$PREDICT_CLOUD_FUNCTION_PATH" \
 --runtime python37 \
 --trigger-resource "$INBOUND_BUCKET" \
 --trigger-event google.storage.object.finalize \
 --set-env-vars model_id="$MODEL_ID",topic_id="$PREDICTION_TOPIC"

## Deploy cloud function with pubsub topic trigger
echo "deploy cloud function $MOVE_CF_NAME triggered by events in $PREDICTION_TOPIC"
gcloud functions deploy "$MOVE_CF_NAME" \
 --source "$MOVE_CLOUD_FUNCTION_PATH" \
 --runtime python37 \
 --trigger-topic "$PREDICTION_TOPIC" \
 --set-env-vars prediction_bucket="$PREDICTION_BUCKET",prediction_threshold="$PREDICTION_THRESHOLD"
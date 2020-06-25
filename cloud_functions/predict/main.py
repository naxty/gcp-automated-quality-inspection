import json
import os
from protobuf_to_dict import protobuf_to_dict

from google.cloud import storage
from google.cloud import automl_v1beta1
from google.cloud import pubsub_v1


def predict_pic_cf(data, context):
    print("Event ID: {}".format(context.event_id))
    print("Event type: {}".format(context.event_type))
    print("Bucket: {}".format(data["bucket"]))
    print("File: {}".format(data["name"]))
    print("Metageneration: {}".format(data["metageneration"]))
    print("Created: {}".format(data["timeCreated"]))
    print("Updated: {}".format(data["updated"]))

    project_id = os.environ.get("GCP_PROJECT")
    model_id = os.environ.get("model_id")
    topic_id = os.environ.get("topic_id")

    destination_file_path = "/tmp/pic.jpeg"

    print("Download Picture from Bucket")
    download_picture(data["bucket"], data["name"], destination_file_path)

    print("Predict Picture")
    response = predict_picture_with_automl(destination_file_path, model_id, project_id)
    print("Prediction response:")
    print(response)

    print("Get PubSub message")
    msg = get_pubsub_msg_from_response(data, response)
    print("Message: ", msg)

    print("Publish to PubSub")
    publisher = pubsub_v1.PublisherClient()
    topic_path = publisher.topic_path(project_id, topic_id)
    publisher.publish(topic_path, data=json.dumps(msg).encode("utf-8"))


def get_pubsub_msg_from_response(data, response):
    serialized = protobuf_to_dict(response)
    result = serialized.get("payload")[0]
    msg = {
        "bucket_name": data["bucket"],
        "pic_name": data["name"],
        "prediction_label": result.get("display_name"),
        "prediction_score": result.get("classification").get("score"),
    }
    return msg


def predict_picture_with_automl(destination_file_path, model_id, project_id):
    with open(destination_file_path, "rb") as content_file:
        content = content_file.read()
    prediction_client = automl_v1beta1.PredictionServiceClient()
    name = f"projects/{project_id}/locations/us-central1/models/{model_id}"
    payload = {"image": {"image_bytes": content}}
    params = {}
    response = prediction_client.predict(name, payload, params)
    return response


def download_picture(bucket_name, blob_name, destination_file_path):
    storage_client = storage.Client()
    bucket = storage_client.bucket(bucket_name)
    blob = bucket.blob(blob_name)
    blob.download_to_filename(destination_file_path)

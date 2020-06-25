import json
import base64
import os

from google.cloud import storage


def move_pic_cf(event, context):
    print(
        f"This Function was triggered by messageId {context.event_id} published at {context.timestamp}"
    )

    prediction_threshold = float(os.environ.get("prediction_threshold"))
    prediction_bucket = os.environ.get("prediction_bucket")

    print("Got Env Variables:")
    print("prediction threshold= ", prediction_threshold)
    print("prediction bucket = ", prediction_bucket)

    inbound_bucket, pic_name, prediction_label, prediction_score = decode_data(
        event["data"]
    )
    new_blob_name = get_new_blob_name(
        pic_name, prediction_label, prediction_score, prediction_threshold
    )
    print("new blob = ", new_blob_name)

    mv_blob(inbound_bucket, pic_name, prediction_bucket, new_blob_name)


def decode_data(data):
    print("Start decoding...")
    print("Received data: ", data)
    data_decoded = base64.b64decode(data)
    print("base64 decoded:, ", data_decoded)
    msg = json.loads(data_decoded.decode("utf-8"))
    print("msg dict: ", msg)
    return (
        msg["bucket_name"],
        msg["pic_name"],
        msg["prediction_label"],
        msg["prediction_score"],
    )


def get_new_blob_name(
    blob_name, prediction_label, prediction_score, prediction_threshold
):
    folder_name = get_blob_folder_by_prediction(
        prediction_label, prediction_score, prediction_threshold
    )
    print("new folder name: ", folder_name)
    return folder_name + "/" + blob_name


def get_blob_folder_by_prediction(
    prediction_label, prediction_score, prediction_threshold
):
    folder_name = prediction_label
    if prediction_score < prediction_threshold:
        folder_name = "undecided"
    return folder_name


def mv_blob(bucket_name, blob_name, new_bucket_name, new_blob_name):
    print(f"Start moving {blob_name} to {new_blob_name}")
    storage_client = storage.Client()
    source_bucket = storage_client.get_bucket(bucket_name)
    source_blob = source_bucket.blob(blob_name)
    destination_bucket = storage_client.get_bucket(new_bucket_name)

    # copy to new destination
    new_blob = source_bucket.copy_blob(source_blob, destination_bucket, new_blob_name)
    # delete in old destination
    source_blob.delete()
    print(f"File moved from {source_blob} to {new_blob_name}")

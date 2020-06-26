import os
import pandas as pd
from google.cloud import storage

BUCKET_NAME = os.environ["TRAINING_DATA_BUCKET"]

client = storage.Client()
bucket = client.get_bucket(BUCKET_NAME)

TRAIN_SET = []
TEST_SET = []
for blob in bucket.list_blobs():
    name = blob.name

    if "def_front" in name:
        LABEL = "Defect"
    elif "ok_front" in name:
        LABEL = "Ok"
    else:
        continue

    if "data/casting_data/test" in name:
        TEST_SET.append((name, LABEL))
    elif "data/casting_data/train" in name:
        TRAIN_SET.append((name, LABEL))

train_df = pd.DataFrame(TRAIN_SET, columns=["name", "label"])
train_df["set"] = "TRAIN"
test_df = pd.DataFrame(TEST_SET, columns=["name", "label"])
test_df["set"] = "TEST"

df = pd.concat([train_df, test_df])
df = df.drop_duplicates(subset="name", keep="first")

random_validation = df[df["set"] == "TRAIN"].sample(frac=0.15)
random_validation["set"] = "VALIDATION"
df.loc[random_validation.index] = random_validation
with open("preparation.csv", "w") as writer:
    for index, row in df.iterrows():
        SET = row["set"]
        LABEL = row["label"]
        NAME = row["name"]
        writer.write(f"{SET},gs://{BUCKET_NAME}/{NAME},{LABEL}\n")

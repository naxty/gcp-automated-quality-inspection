import os
from typing import List
from enum import Enum
from datetime import timedelta

from google.cloud import storage
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from fastapi.staticfiles import StaticFiles
from starlette.responses import HTMLResponse, FileResponse
from cryptography.fernet import Fernet

key = Fernet.generate_key()
f = Fernet(key)
BUCKET = os.environ['BUCKET']

client = storage.Client.from_service_account_json("app_engine_service_account.json")

bucket = client.get_bucket(BUCKET)
app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")


class NeedDecision(BaseModel):
    name: str
    blob_name: str


class NeedDecisionResponse(BaseModel):
    need_decisions: List[NeedDecision]


class DecisionEnum(str, Enum):
    ok = "ok"
    defect = "defect"


class Decision(BaseModel):
    id: str
    decision: DecisionEnum


@app.get("/need_decision", response_model=dict)
def get_need_decision_images():
    blobs = list(bucket.list_blobs(prefix="predictions/undecided/"))
    decisions = []
    return_blob = None
    for blob in blobs:
        if ".jpeg" in blob.name:
            return_blob = blob
            break
    if not return_blob:
        return {}
    url = blob.generate_signed_url(
        expiration=timedelta(seconds=60)
    )
    return {"url": url, "id": f.encrypt(str.encode(blob.name)).decode("utf-8")}


@app.post("/make_decision")
def make_decision(decision: Decision):
    token = decision.id.encode("utf-8")
    decrypted_blob_name = f.decrypt(token)
    blob = bucket.get_blob(decrypted_blob_name)
    if not blob:
        raise HTTPException(status_code=404, detail="Blob not found")

    value = decision.decision
    new_blob_name = f"{value}_{blob.name}"
    bucket.rename_blob(blob, f"predictions/human_decided/{new_blob_name}")
    return 200


@app.get("/.*", include_in_schema=False)
def root():
    return FileResponse("./static/index.html")

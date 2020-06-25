# Google Cloud Platform Automated Image Quality Inspection
This repository is showcase about how to leverage google cloud platform to quickly train and deploy a machine learning project. We are using different components of gcp such as [App Engine](https://cloud.google.com/appengine), [AutoML](https://cloud.google.com/automl), [Cloud Storage](https://cloud.google.com/storage), [Cloud Pub/Sub](https://cloud.google.com/pubsub) and [Cloud Functions](https://cloud.google.com/functions) are used to implement an end-to-end machine learning project. Based on this [dataset](https://www.kaggle.com/ravirajsinh45/real-life-industrial-dataset-of-casting-product) we train an AutoML image classification model and deploy it through AutoML.

## Overview
- [app_engine](app_engine/): Demo application for deployment. For the implementation we use [fastapi](https://fastapi.tiangolo.com/) and [React](https://reactjs.org/) and deploy it on the [App Engine](https://cloud.google.com/appengine).
- [automl](automl/): All the code and instructions that are necessary to prepare for [AutoML](https://cloud.google.com/automl) image classification training.
- [cloud_functions](cloud_functions):
- [data](data/): All the data that is used for this project. We used [product image data for quality insepection](https://www.kaggle.com/ravirajsinh45/real-life-industrial-dataset-of-casting-product) from [kaggle](https://www.kaggle.com/) for this project. 
- [docs](docs/): Find the documentation images. 


## Prerequirements
You need access to the Google Cloud Platform and a 

## Tutorial
There are X parts in this tutorial. We need to set the following configurations:
```sh
export PROJECT_ID="vigilant-shift-280708"
export BUCKET_LOCATION="US-CENTRAL1"
export BUCKET_NAME="product-quality"

```


### 1. AutoML Preparation, Training and Deployment
1. Download the [dataset](https://www.kaggle.com/ravirajsinh45/real-life-industrial-dataset-of-casting-product) and put it inside the [data](data/)-folder. Extract the zip file.
```
data
└── casting_data
    ├── test
    │   ├── def_front
    │   │   ├── ....
    │   │   └── new__0_9334.jpeg
    │   └── ok_front
    │       ├── ....
    │       └── cast_ok_0_9996.jpeg
    └── train
        ├── def_front
        │   ├── ...
        │   └── cast_def_0_9997.jpeg
        └── ok_front
            ├── ...
            └── cast_ok_0_9998.jpeg
```

2. Create a GCS bucket and upload the data:
```sh
gsutil mb -p $PROJECT_ID  -l $BUCKET_LOCATION -b on gs://$BUCKET_NAME
gsutil -m cp -r ../data gs://$BUCKET_NAME
```
from typing import TypedDict


class Extensions(TypedDict):
    compartmentId: str


class AdditionalDetails(TypedDict):
    eTag: str
    namespace: str
    bucketName: str
    bucketId: str
    archivalState: str


class Data(TypedDict):
    compartmentId: str
    compartmentName: str
    resourceName: str
    resourceId: str
    availabilityDomain: str
    additionalDetails: AdditionalDetails


class ObjectCreateEventPayload(TypedDict):
    cloudEventsVersion: str
    eventID: str
    eventType: str
    source: str
    eventTypeVersion: str
    eventTime: str
    contentType: str
    extensions: Extensions
    data: Data


{
    "cloudEventsVersion": "0.1",
    "eventID": "unique_ID",
    "eventType": "com.oraclecloud.objectstorage.createobject",
    "source": "objectstorage",
    "eventTypeVersion": "2.0",
    "eventTime": "2019-01-10T21:19:24.000Z",
    "contentType": "application/json",
    "extensions": {
        "compartmentId": "ocid1.compartment.oc1..unique_ID"
    },
    "data": {
        "compartmentId": "ocid1.compartment.oc1..unique_ID",
        "compartmentName": "example_name",
        "resourceName": "my_object",
        "resourceId": "/n/example_namespace/b/my_bucket/o/my_object",
        "availabilityDomain": "all",
        "additionalDetails": {
            "eTag": "f8ffb6e9-f602-460f-a6c0-00b5abfa24c7",
            "namespace": "example_namespace",
            "bucketName": "my_bucket",
            "bucketId": "ocid1.bucket.oc1.phx.unique_id",
            "archivalState": "Available"
        }
    }
}

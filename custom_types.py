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
    # object path
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

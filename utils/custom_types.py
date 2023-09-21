from typing import List, TypedDict


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
    # object path
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


class ObjectInfo(TypedDict):
    archival_state: str
    etag: str
    md5: str
    name: str
    size: str
    storage_tier: str
    time_created: str
    time_modified: str


Objects = List[ObjectInfo]

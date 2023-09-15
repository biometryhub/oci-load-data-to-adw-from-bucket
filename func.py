import io
import json
import logging
from fdk import response

# from .custom_types import ObjectCreateEventPayload

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


def handler(ctx, data: io.BytesIO = None):
    name = "World"
    try:
        body: ObjectCreateEventPayload = json.loads(data.getvalue())
        name = body.get("name")
        logging.getLogger().info(body)
    except (Exception, ValueError) as ex:
        logging.getLogger().info('error parsing json payload: ' + str(ex))

    logging.getLogger().info("Inside Python Hello World function")
    return response.Response(
        ctx, response_data=json.dumps(
            {"message": "Hello {0}".format(name)}),
        headers={"Content-Type": "application/json"}
    )

import io
import json
import logging
from fdk import response

from custom_types import ObjectCreateEventPayload


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

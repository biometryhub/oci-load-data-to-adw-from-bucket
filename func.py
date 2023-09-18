import io
import json
import logging
import oci
from fdk import response

from custom_types import ObjectCreateEventPayload
from utils.safe_io import BucketHandler


def handler(ctx, data: io.BytesIO = None):
    config = oci.config.from_file()
    logging.getLogger().info(config)
    signer = oci.auth.signers.get_resource_principals_signer()
    name = "World"
    try:
        body: ObjectCreateEventPayload = json.loads(data.getvalue())
        name = body.get("name")
    except (Exception, ValueError) as ex:
        logging.getLogger().info('error parsing json payload: ' + str(ex))

    logging.getLogger().info("Inside Python Hello World function")
    bucket_handler = BucketHandler(signer)
    namespace = bucket_handler.client.get_namespace().data
    print(namespace)
    logging.getLogger().info(namespace)
    objects = bucket_handler.list_objects(
        'axbqhk0rrkra', 'workshop-data-lake-client-1')
    logging.getLogger().info(objects.data)

    return response.Response(
        ctx, response_data=json.dumps(
            {"message": "Hello {0}".format(name)}),
        headers={"Content-Type": "application/json"}
    )

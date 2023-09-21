import io
import json
import logging
import oci
from fdk import response

from utils.custom_types import ObjectCreateEventPayload
from utils.safe_io import BucketHandler, parse_config
from utils.utils import validate_bucket


def handler(ctx, data: io.BytesIO = None):
    # TODO: convert to resource principal
    # signer = oci.auth.signers.get_resource_principals_signer()
    credential = oci.config.from_file('./.oci/config')
    parse_config('./config.yaml')

    try:
        body: ObjectCreateEventPayload = json.loads(data.getvalue())
        bucket_name = body['data']['additionalDetails']['bucketName']
        object_path = body['data']['resourceId']
    except (Exception, ValueError) as ex:
        logging.getLogger().info('error parsing json payload: ' + str(ex))

    client_number = validate_bucket(bucket_name)
    if client_number is None:
        logging.getLogger().info('Not a valid bucket, exiting!')
        return

    logging.getLogger().info(f'Client {client_number} is triggering this job.')

    logging.getLogger().info('object_path')
    logging.getLogger().info(object_path)

    bucket_handler = BucketHandler(credential)

    objects = bucket_handler.list_objects(bucket_name)
    logging.getLogger().info(len(objects))

    is_directory = bucket_handler.is_directory(bucket_name, object_path)
    logging.getLogger().info(is_directory)

    return response.Response(
        ctx, response_data=json.dumps({"message": 'yay'}),
        headers={"Content-Type": "application/json"}
    )

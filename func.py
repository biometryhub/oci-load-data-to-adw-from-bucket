import io
import json
import logging
import oci
from fdk import response

from utils.custom_types import ObjectCreateEventPayload
from utils.processor import Processor
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
        object_path = body['data']['resourceName']
    except (Exception, ValueError) as ex:
        logging.getLogger().info('error parsing json payload: ' + str(ex))

    client_number = validate_bucket(bucket_name)
    if client_number is None:
        logging.getLogger().info('Not a valid bucket, exiting!')
        return

    logging.getLogger().info(f'Client {client_number} is triggering this job.')

    bucket_handler = BucketHandler(credential)
    processor = Processor(
        bucket_handler, bucket_name, object_path, client_number)
    processor.execute()
    # req = bucket_handler.get_object(bucket_name, object_path)
    # df = read_bytes(req.data.content)
    # process_df(df)
    # target_path = create_target_path(client_number, object_path)
    # parquet_data = df.to_parquet()
    # bucket_handler.persist_object(parquet_data, processor.target_path)
    # processor.success(parquet_data)

    return response.Response(
        ctx, response_data=json.dumps({"message": 'Success!'}),
        headers={"Content-Type": "application/json"}
    )

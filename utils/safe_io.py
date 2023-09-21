import logging
import oci
import sys
import yaml
from .config import CLIENT, CONFIG
from .custom_types import Objects
from .utils import validate_object


def parse_config(config_path: str):
    with open(config_path, 'r') as f:
        config = yaml.load(f, Loader=yaml.SafeLoader)

    CONFIG.BUCKET.PERSISTENCE = config['bucket']['persistence']
    CONFIG.BUCKET.CLIENT.PATTERN = config['bucket']['client']['pattern']
    CONFIG.BUCKET.CLIENT.VALID_FILE = config['bucket']['client']['valid_file']


class BucketHandler:
    def __init__(self, credential):
        self.client = oci.object_storage.ObjectStorageClient(config=credential)
        self.namespace = self.client.get_namespace().data

    def get_object(self, bucket_name: str, object_path: str):
        is_directory = self.is_directory(bucket_name, object_path)
        if is_directory:
            logging.getLogger().info(f'{object_path} is a directoy, exiting!')
            sys.exit()

        is_valid_object = validate_object(object_path)
        if not is_valid_object:
            logging.getLogger().info(
                f'{object_path} is not matching {CLIENT.VALID_FILE}, exiting!')
            sys.exit()

        req = self.client.get_object(self.namespace, bucket_name, object_path)
        return req

    def list_objects(self, bucket_name: str, **kwargs):
        return self.client.list_objects(self.namespace, bucket_name, **kwargs) \
            .data \
            .objects

    def is_directory(self, bucket_name: str, object_path: str):
        objects: Objects = self.list_objects(bucket_name, prefix=object_path)
        for object_ in objects:
            name = object_.name
            if name.startswith(object_path) and name.endswith('/'):
                return True

        return False

    def persist_object(self, content: bytes, object_path: str):
        logging.getLogger().info(f'Writing to {object_path}')
        self.client.put_object(
            self.namespace, CONFIG.BUCKET.PERSISTENCE, object_path, content)

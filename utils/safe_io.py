import oci
import yaml
from .config import CONFIG
from .custom_types import Objects


def parse_config(config_path: str):
    with open(config_path, 'r') as f:
        config = yaml.load(f, Loader=yaml.SafeLoader)

    CONFIG.BUCKET.PERSISTENCE = config['bucket']['persistence']
    CONFIG.BUCKET.CLIENT.PATTERN = config['bucket']['client']['pattern']


class BucketHandler:
    def __init__(self, credential):
        self.client = oci.object_storage.ObjectStorageClient(config=credential)
        self.namespace = self.client.get_namespace().data

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

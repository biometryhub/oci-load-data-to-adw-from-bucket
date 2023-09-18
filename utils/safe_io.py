import oci


class BucketHandler:
    def __init__(self, config):
        self.client = oci.object_storage.ObjectStorageClient(config=config)

    def list_objects(self, namespace: str, bucket_name: str):
        return self.client.list_objects(namespace, bucket_name).data

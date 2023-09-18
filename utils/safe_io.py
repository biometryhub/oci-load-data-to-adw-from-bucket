import oci


class BucketHandler:
    def __init__(self, signer):
        self.signer = signer
        self.client = oci.object_storage.ObjectStorageClient(
            config={}, signer=signer)

    def list_objects(self, namespace: str, bucket_name: str):
        self.client.list_objects(namespace, bucket_name)

import re
from .config import CLIENT


def get_bucket_uri(namespace: str, bucket_name: str,
                   region: str = 'ap-melbourne-1'):
    return f'https://objectstorage.{region}.oraclecloud.com/n/{namespace}/b/{bucket_name}/o'


def validate_bucket(bucket_name: str):
    search = re.search(CLIENT.PATTERN, bucket_name)
    if search is not None:
        groups = search.groups()
        return groups[0]

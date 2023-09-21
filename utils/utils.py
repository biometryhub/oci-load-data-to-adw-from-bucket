from io import StringIO
from os import path
import pandas as pd
import re
from .config import CLIENT


def change_extension(object_path: str, new_extension: str):
    object_name, _ = path.splitext(object_path)
    return f'{object_name}.{new_extension}'


def create_client_path(client_number: str, object_path: str):
    return path.join(f'client_{client_number}', object_path)


def get_bucket_uri(namespace: str, bucket_name: str,
                   region: str = 'ap-melbourne-1'):
    return f'https://objectstorage.{region}.oraclecloud.com/n/{namespace}/b/{bucket_name}/o'


def read_bytes(b: bytes, **kwargs):
    return pd.read_csv(StringIO(str(b, 'utf-8')), **kwargs)


def validate_bucket(bucket_name: str):
    search = re.search(CLIENT.PATTERN, bucket_name)
    if search is not None:
        groups = search.groups()
        return groups[0]


def validate_object(object_path: str):
    search = re.search(CLIENT.VALID_FILE, object_path)
    if search is not None:
        return True

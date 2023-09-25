from datetime import datetime, timezone
import hashlib
from io import StringIO
from os import path
import pandas as pd
from typing import Tuple
import re
from .config import CLIENT


def change_extension(object_path: str, new_extension: str):
    object_name, _ = path.splitext(object_path)
    return f'{object_name}.{new_extension}'


def create_client_path(client_number: str, object_path: str):
    return path.join(f'client_{client_number}', object_path)


def current_utc():
    return datetime.now(timezone.utc)


def get_passwords() -> Tuple[str, str]:
    with open('./admin_password', 'r') as f:
        admin_password = f.read().strip()

    with open('./wallet_password', 'r') as f:
        wallet_password = f.read().strip()

    return admin_password, wallet_password


def hash_data(data: bytes):
    return hashlib.md5(data).hexdigest()


def hash_file(file_path: str, buf_size: int = 65536):
    md5 = hashlib.md5()
    with open(file_path, 'rb') as f:
        while True:
            data = f.read(buf_size)
            if not data:
                break
            md5.update(data)

    return md5.hexdigest()


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

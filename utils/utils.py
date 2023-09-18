def get_bucket_uri(namespace: str, bucket_name: str,
                   region: str = 'ap-melbourne-1'):
    return f'https://objectstorage.{region}.oraclecloud.com/n/{namespace}/b/{bucket_name}/o'

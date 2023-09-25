import logging
import oci
import oracledb
import sys
import yaml
from .config import CLIENT, CONFIG
from .custom_types import Objects
from . import utils


def parse_config(config_path: str):
    with open(config_path, 'r') as f:
        config = yaml.load(f, Loader=yaml.SafeLoader)

    CONFIG.BUCKET.PERSISTENCE = config['bucket']['persistence']
    CONFIG.BUCKET.CLIENT.PATTERN = config['bucket']['client']['pattern']
    CONFIG.BUCKET.CLIENT.VALID_FILE = config['bucket']['client']['valid_file']


class BucketHandler:
    def __init__(self, credential):
        logging.getLogger().info('Initiating object storage client')
        self.client = oci.object_storage.ObjectStorageClient(config=credential)
        self.namespace = self.client.get_namespace().data
        self.persist_uri = self.get_uri(CONFIG.BUCKET.PERSISTENCE)

    def get_object(self, bucket_name: str, object_path: str):
        is_directory = self.is_directory(bucket_name, object_path)
        if is_directory:
            logging.getLogger().info(f'{object_path} is a directoy, exiting!')
            sys.exit()

        is_valid_object = utils.validate_object(object_path)
        if not is_valid_object:
            logging.getLogger().info(
                f'{object_path} is not matching {CLIENT.VALID_FILE}, exiting!')
            sys.exit()

        logging.getLogger().info(f'Loading {object_path} from {bucket_name}')
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

    def get_uri(self, bucket_name: str, region: str = 'ap-melbourne-1'):
        return f'https://objectstorage.{region}.oraclecloud.com/n/{self.namespace}/b/{bucket_name}/o'


class DatabaseHandler:
    def __init__(self, user: str, password: str, wallet_password: str,
                 dsn: str = 'workshopdatalake_low',
                 config_dir: str = './wallet',
                 wallet_location: str = './wallet'):
        logging.getLogger().info('Connecting to database')
        self.connection = oracledb.connect(
            user=user, password=password, dsn=dsn, config_dir=config_dir,
            wallet_location=wallet_location, wallet_password=wallet_password)

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self.connection.close()

    def create_table(self, table_name: str, target_uri: str,
                     column_definition: str, credential_name: str = ''):
        logging.getLogger().info(f'Creating table {table_name}')
        create_statement = self.template['create_table'].format(
            table_name=table_name, credential_name=credential_name,
            target_uri=target_uri, column_definition=column_definition)
        self.execute(create_statement)

    def execute(self, statement: str):
        with self.connection.cursor() as c:
            c.execute(statement)
            rows = c.fetchall()

        return rows

    def _init_template(self):
        self.template = {
            'create_table': '''
                BEGIN
                    DBMS_CLOUD.CREATE_EXTERNAL_TABLE(
                        table_name => '{table_name}',
                        credential_name => '{credential_name}',
                        file_uri_list => '{target_uri}/*.parquet',
                        format => json_object('type' value 'parquet'),
                        column_list => '{column_definition}'
                    );
                END;
                /
            '''
        }

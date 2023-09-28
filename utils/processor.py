import logging
from os import path
import pandas as pd
import re
from typing import Tuple
from . import utils
from .config import BUCKET, DATABASE
from .safe_io import BucketHandler, DatabaseHandler


class Processor:
    def __init__(self, bucket_handler: BucketHandler, bucket_name: str,
                 object_path: str, client_number: str):
        logging.getLogger().info('Initiating object processor')
        self.bucket_handler = bucket_handler
        self.bucket_name = bucket_name
        self.object_path = object_path
        self.client_number = client_number

        self._set_paths()

    def process_object(self) -> Tuple[pd.DataFrame, str]:
        req = self.bucket_handler.get_object(
            self.bucket_name, self.object_path)
        self.df = utils.read_bytes(req.data.content)

        self.detect_date(self.df)
        self.column_definition = self.get_column_definition(self.df)

    def create_table(self):
        if self.is_table_exist():
            logging.getLogger().info(f'{self.table_name} already exists!')
            return

        password, wallet_password = utils.get_passwords()
        with DatabaseHandler('admin', password, wallet_password) as db_handler:
            target_uri = path.join(
                self.bucket_handler.persist_uri, self.target_files)
            db_handler.create_table(
                self.table_name, target_uri, self.column_definition,
                DATABASE.CREDENTIAL_NAME)

        success_time = utils.current_utc()
        success_content = f'{self.table_name}|{success_time}'
        self.bucket_handler.persist_object(success_content, self.success_table)

    def detect_date(self, df: pd.DataFrame):
        for col in df.columns:
            if df.dtypes[col] == object:
                try:
                    datetime_col = pd.to_datetime(df[col])
                    logging.getLogger().info(f'Parsing {col} to datetime')
                    df[col] = datetime_col
                except (pd._libs.tslibs.parsing.DateParseError,
                        pd._libs.tslibs.np_datetime.OutOfBoundsDatetime):
                    pass
                except Exception as e:
                    logging.getLogger() \
                        .error(f'Trying to parse {col} failed with {e}')

    def execute(self):
        self.process_object()
        parquet_data = self.df.to_parquet()

        self.bucket_handler.persist_object(parquet_data, self.target_path)
        self.success(parquet_data)
        self.create_table()

    def get_column_definition(self, df: pd.DataFrame):
        column_definitions = []
        for col in df.columns:
            column_definition = f'{col.upper()} '
            dtype = df.dtypes[col]
            if dtype == object:
                column_definition += 'VARCHAR2(64)'
            elif dtype == 'datetime64[ns]':
                column_definition += 'DATE'
            else:
                column_definition += 'NUMBER'

            column_definitions.append(column_definition)

        return ', '.join(column_definitions)

    def is_table_exist(self):
        return bool(self.bucket_handler.list_objects(
            BUCKET.PERSISTENCE, prefix=self.success_table))

    def success(self, content: bytes):
        success_time = utils.current_utc()
        hashed = utils.hash_data(content)
        success_content = f'{self.target_path}|{hashed}|{success_time}'
        self.bucket_handler.persist_object(success_content, self.success_path)

    def _get_table_name(self):
        return re.sub(r'(_|\W)+', '_', self.target_folder)

    def _get_target_files(self):
        return path.join(self.target_folder, '*.parquet')

    def _get_target_path(self):
        return utils.create_client_path(
            self.client_number,
            utils.change_extension(self.object_path, 'parquet'))

    def _get_success_path(self):
        return utils.change_extension(self.target_path, 'SUCCESS')

    def _set_paths(self):
        self.target_path = self._get_target_path()
        self.target_folder = path.join(*self.target_path.split('/')[:-1])

        self.table_name = self._get_table_name()
        self.target_files = self._get_target_files()
        self.success_path = self._get_success_path()
        self.success_table = path.join(self.target_folder, 'table.SUCCESS')

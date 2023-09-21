import logging
import pandas as pd
from .utils import create_client_path, change_extension


def create_target_path(client_number: str, object_path: str):
    return create_client_path(
        client_number, change_extension(object_path, 'parquet'))


def get_column_definition(df: pd.DataFrame):
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


def process_df(df: pd.DataFrame):
    # parse datetime columns
    for col in df.columns:
        if df.dtypes[col] == object:
            try:
                datetime_col = pd.to_datetime(df[col])
                logging.getLogger().info(f'Parsing {col} to datetime')
                df[col] = datetime_col
            except pd._libs.tslibs.parsing.DateParseError:
                pass

import os
from os import mkdir
from os.path import join
from os.path import exists
from os.path import basename
import re

import pandas as pd

from ..default_values import fields_filename
from ..default_values import tables_filename
from ..default_values import flatfields_path

from ..name_manipulation import create_table_filename
from ..name_manipulation import create_auxiliary_table_filename


def load_flatfields():
    fields_table = pd.read_csv(join(flatfields_path, fields_filename), sep='\t')
    tables_table = pd.read_csv(join(flatfields_path, tables_filename), sep='\t')
    fields_table.fillna('', inplace=True)
    tables_table.fillna('', inplace=True)

    data_table_filenames = [
        f for f in os.listdir(flatfields_path) if not f in [fields_filename, tables_filename]
    ]
    strip = lambda x : re.sub('\.tsv$', '', x)
    data_tables = {
        strip(basename(filename)) : pd.read_csv(join(flatfields_path, filename), sep='\t').fillna('')
        for filename in data_table_filenames
    }
    return [fields_table, tables_table, data_tables]


def write_flatfields(fields_table, tables_table, data_tables):
    if not exists(flatfields_path):
        mkdir(flatfields_path)

    for index, table_record in tables_table.iterrows():
        tablename = table_record['Name']
        df = data_tables[tablename]
        if table_record['Primary key'] != 'value':
            filename = create_table_filename(tablename)
        else:
            filename = create_auxiliary_table_filename(tablename)
        df.to_csv(join(flatfields_path, filename), sep='\t', index=False)

    fields_table.to_csv(join(flatfields_path, fields_filename), sep='\t', index=False)
    tables_table.to_csv(join(flatfields_path, tables_filename), sep='\t', index=False)

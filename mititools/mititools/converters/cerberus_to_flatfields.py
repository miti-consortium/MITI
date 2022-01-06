"""
This module converts the YAML-based schema for Cerberus-validated data bundles
into a schema based on a flat fields table. It is currently a lossy conversion.
"""
import re
import ast

import pandas as pd

from ..name_manipulation import create_table_filename
from ..name_manipulation import create_auxiliary_table_filename
from ..name_manipulation import create_auxiliary_table_name
from ..name_manipulation import create_machine_readable_token
from ..name_manipulation import create_human_readable_label
from ..name_manipulation import extract_table_name


def convert(dicts):
    """
    Args:
        dicts: The dictionary representation of the YAML-specified
        Cerberus-validated schema.
    Returns:
        The flat-fields representation, in the format of a triple: A fields
        dataframe, a tables dataframe, and a list of data-package-level dataframes
        containing headers only or default records.
    """
    dfs = []
    for filename, values in dicts.items():
        df = pd.DataFrame(values).transpose()
        df['Table'] = extract_table_name(filename)
        dfs.append(df)

    yaml_fields_table = pd.concat(dfs).fillna('')
    yaml_fields_table['Column name'] = [create_machine_readable_token(index) for index, r in yaml_fields_table.iterrows()]
    yaml_fields_table['Column label'] = [create_human_readable_label(index) for index, r in yaml_fields_table.iterrows()]
    yaml_fields_table.rename(inplace=True, columns={
        'description' : 'Description',
        'type' : 'Data type',
        'significance' : 'Significance',
        'category' : 'Category',
    })
    yaml_fields_table['Data format'] = [
        'default' if row['Data type'] == 'doi' else 'default'
        for i, row in yaml_fields_table.iterrows()
    ]
    type_convert = {
        'float' : 'number',
        'doi' : 'string',
        'filename' : 'string',
        'rrid' : 'string',
    }
    yaml_fields_table['Data type'] = [
        type_convert[row['Data type']] if row['Data type'] in type_convert else row['Data type']
        for i, row in yaml_fields_table.iterrows()
    ]

    auxiliary_tables = create_auxiliary_tables(yaml_fields_table)
    yaml_fields_table.drop('valid-values', axis=1, inplace=True)
    fields_table = yaml_fields_table

    ft = lambda field_record : create_auxiliary_table_name(field_record['Column name'], field_record['Table'])
    fields_table['Foreign table'] = [
        ft(field_record) if ft(field_record) in auxiliary_tables else ''
        for index, field_record in fields_table.iterrows()
    ]
    fields_table['Foreign key'] = [
        'value' if ft(field_record) in auxiliary_tables else ''
        for index, field_record in fields_table.iterrows()
    ]

    auxiliary_table_fields = pd.DataFrame([
        {
            'Table' : name,
            'Column name' : 'value',
            'Column label' : 'Value',
            'Data type' : 'string',
            'Description' : '',
            'Necessity' : 'required',
            'Category' : 'Controlled vocabulary',
            'Data format' : '',
            'Foreign table' : '',
            'Foreign key' : '',
        }
        for name, auxiliary_table in auxiliary_tables.items()
    ])
    fields_table = pd.concat([fields_table, auxiliary_table_fields])

    fields_table = fields_table[fields_column_order]
    tables_table = create_tables_table(fields_table)

    data_tables = {}
    for index, table_record in tables_table.iterrows():
        tablename = table_record['Name']
        if table_record['Primary key'] != 'value':
            fields = fields_table[fields_table['Table'] == tablename]
            df = pd.DataFrame({field['Column name'] : [] for i, field in fields.iterrows()})
            data_tables[tablename] = df

    data_tables = dict(**data_tables, **auxiliary_tables)
    return [fields_table, tables_table, data_tables]


fields_column_order = [
    'Table',
    'Column name',
    'Column label',
    'Data type',
    'Necessity',
    'Category',
    'Data format',
    'Foreign table',
    'Foreign key',
    'Description',
]


def parse_values(values_string):
    """
    Args:
        values_string: A Python-syntax string representing a list of strings.
    Returns:
        The list of strings, sorted. If parsing fails, returns None.
    """
    values = ast.literal_eval(values_string)
    if isinstance(values, list):
        values = [str(v) for v in values]
        return sorted(list(set(values)))
    return None


def create_auxiliary_tables(yaml_fields_table):
    """
    Args:
        yaml_fields_table: Dataframe listing all fields as specified in YAML
        sources.
    Returns:
        Dictionary whose keys are table names and whose values are controlled
        vocabulary dataframes extracted from valid values lists.
    """
    auxiliary_tables = {}
    condition = yaml_fields_table['valid-values'] != ''
    for index, field_record in yaml_fields_table[condition].iterrows():
        name = create_auxiliary_table_name(field_record['Column name'], field_record['Table'])
        values = parse_values(str(field_record['valid-values']))
        if values:
            if name in auxiliary_tables:
                print('Warning: Multiple controlled vocabularies named "%s".' % name)
                print(auxiliary_tables[name])
                print(values)
            auxiliary_tables[name] = pd.DataFrame({'value' : values})
    return auxiliary_tables


def create_tables_table(fields_table):
    """
    Args:
        fields_table: The flat table of fields.
    Returns:
        A dataframe whose records represent tables. The main datum is a guessed
        primary key column name, the "Primary key" field. Also has a "Name" column.
    """
    table_records = []
    for table_name, fields in fields_table.groupby('Table'):
        field_names = list(fields['Column name'])
        with_id = [n for n in field_names if re.search('_id$', n)]
        primary = None
        if len(with_id) == 1:
            primary = with_id[0]
        elif len(with_id) > 1:
            derived_name = table_name + '_id'
            if derived_name in with_id:
                primary = derived_name
            else:
                primary = sorted(with_id, key=lambda x: len(x))[0]
        if len(field_names) == 1:
            primary = field_names[0]
        if primary is None:
            print('Warning: Could not find primary key for table "%s".' % table_name)
        else:
            table_records.append({'Name' : table_name, 'Primary key' : primary})
    return pd.DataFrame(table_records)

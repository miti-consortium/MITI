import os
from os.path import join
import json
import importlib.resources

import jinja2
from jinja2 import Environment
from jinja2 import BaseLoader

with importlib.resources.path('mititools', 'miti_schema.json.jinja') as file:
    jinja_environment = Environment(loader=BaseLoader)
    schema_file_contents = open(file, 'rt').read()


def create_table_filename(table_name):
    return table_name + '.tsv'


def write_frictionless(
        fields_table,
        provider,
        ...
        package_dir = 'example_data_package',
        json_filename = 'datapackage.json',
    ):
    json_str = create_frictionless_schema(fields_table)
    json_object = json.loads(json_str)
    payload = json.dumps(json_object, indent=2)
    os.mkdir(package_dir)
    with open(join(package_dir, json_filename), 'wt') as f:
        f.write(payload)


def create_fields_and_tables(provider):
    resources = [
        {
            'table_name' : table_record['Name'],
            'filename' : create_table_filename(table_record['Name']),
            'fields' : [
                {
                    'column_name' : field_record['Column name'],
                    'title' : field_record['Column label'],
                    'type_string' : field_record['Data type'],
                    'data_format' : field_record['Data format'],
                    'description' : field_record['Description'],
                }
                for index_field, field_record in provider.fields_of(table_record)
            ],
            'primary_key' : table_record['Primary key'],
            'foreign_keys' : [
                {
                    'source_column' : field_record['Column name'],
                    'target_table' : field_record['Foreign table'],
                    'target_column' : field_record['Foreign key'],
                }
                for index_field, field_record in provider.foreign_fields_of(table_record)
            ],
            'has_foreign_keys' : len([e for e in provider.foreign_fields_of(table_record)]) > 0,
        }
        for index_table, table_record in provider.tables()
    ]
    return resources


def create_frictionless_schema(fields_table):
    resources = create_fields_and_tables(fields_table)
    variables = {
        'data_package_name' : 'data-package-name',
        'globally_unique_data_package_identifier' : 'globally unique data package identifier',
        'data_package_title' : 'data package title',
        'resources' : resources,
    }
    template = jinja_environment.from_string(schema_file_contents)
    return template.render(**variables)


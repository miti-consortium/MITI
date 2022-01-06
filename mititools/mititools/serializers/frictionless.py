import os
from os import mkdir
from os.path import join
from os.path import exists
import json
import importlib.resources

import jinja2
from jinja2 import Environment
from jinja2 import BaseLoader

with importlib.resources.path('mititools', 'fd_schema.json.jinja') as file:
    jinja_environment = Environment(loader=BaseLoader)
    fd_schema_file_contents = open(file, 'rt').read()

from ..default_values import fd_package_path
from ..name_manipulation import create_table_filename
from ..name_manipulation import create_auxiliary_table_filename


def write_frictionless(top_variables, data_tables):
    json_str = render_json_data_package(top_variables)
    json_object = json.loads(json_str)
    payload = json.dumps(json_object, indent=2)

    json_filename = 'datapackage.json'
    if not exists(fd_package_path):
        mkdir(fd_package_path)
    with open(join(fd_package_path, json_filename), 'wt') as f:
        f.write(payload)

    for tablename, df in data_tables.items():
        if list(df.columns) != ['value']:
            filename = create_table_filename(tablename)
        else:
            filename = create_auxiliary_table_filename(tablename)
        df.to_csv(join(fd_package_path, filename), sep='\t', index=False)


def render_json_data_package(variables):
    template = jinja_environment.from_string(fd_schema_file_contents)
    return template.render(**variables)

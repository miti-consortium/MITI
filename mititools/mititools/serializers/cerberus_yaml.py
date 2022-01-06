import re
import os
from os import listdir
from os.path import isfile
from os.path import join
from os.path import basename
import yaml

from ..default_values import yaml_path


def load_yaml_schema():
    """
    Returns:
        A dictionary whose keys are the schema file basenames and whose values are
        nested dictionaries represented by the YAML sources.
    """
    yaml_files = [f for f in listdir(yaml_path) if isfile(join(yaml_path, f))]
    for filename in yaml_files:
        if not re.search('\.yaml$', filename):
            print('%s not a YAML file?' % filename)
            exit(1)
        if not extract_dict(filename, validate_only=True):
            print('%s did not load properly.' % filename)
            exit(1)
    dicts = {basename(filename) : extract_dict(filename) for filename in yaml_files}
    return dicts


def extract_dict(yaml_filename, validate_only=False):
    """
    Args:
        yaml_filename: A YAML file.
        validate_only: If True, returns only a boolean validation flag.
    Returns:
        The nested dictionary represented by the YAML source. (Unless validate_only
        is True).
    """
    data = None
    with open(yaml_filename, 'rt') as file:
        try:
            data = yaml.load(file, Loader=yaml.FullLoader)
            if validate_only and (not data is None):
                return True
        except Exception as e:
            if validate_only:
                return False
    return data

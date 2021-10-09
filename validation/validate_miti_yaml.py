from cerberus import Validator
import yaml
import sys
import os

v = Validator()

def import_yaml(input_yaml):
    with open(input_yaml, 'r') as file:
        to_validate = yaml.safe_load(file)
    names = list(to_validate)
    attributes = list(map(lambda x: to_validate[x], names))

    return(names, attributes)

def import_schema(schema_path):
    with open(schema_path, 'r') as file:
        schema = yaml.safe_load(file)
    return(schema)

def validation(names, attributes, schema):
    check = v.validate(attributes, schema)
    errors = v.errors
    return(names, check,errors)

def main():

    input_yaml = sys.argv[1]
    schema_path = sys.argv[2]

    names, attributes = import_yaml(input_yaml)

    schema = import_schema(schema_path)

    check = list(map(lambda x, y: validation(x, y, schema), names, attributes))

    errors = list(filter(lambda c: c[1] == False, check))
    if (len(errors) > 0):
        print("Validation errors found in " + os.path.basename + ": " +str(len(errors)))
        print(errors)
        sys.exit(1)
    else:
        print("Passed validation: " + os.path.basename(input_yaml))
        
     

if __name__ == "__main__":
    main()

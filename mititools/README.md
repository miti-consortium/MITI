# mititools
These tools convert the MITI schema between 3 different formats:

1. `yaml`. The reference YAML specification, designed to be validated with [Cerberus](https://docs.python-cerberus.org/en/stable/).
2. `flatfields`. A specification based on a flat table of fields.
3. `frictionless`. A [Frictionless Data](https://frictionlessdata.io/standards/#standards-toolkit) [data package](https://specs.frictionlessdata.io/data-package/) schema.

The translation is not perfect, as the schema languages are not equivalent.

# Installation
From the top-level of this repository (probably called `MITI`), install this Python package with:

```sh
pip install mititools/
```

# Convert the Cerberus-validated YAML specification to flat fields

```sh
mititools convert yaml flatfields
```

This creates `flatfields/fields.tsv`, `flatfields/tables.tsv`, as well as empty/default data tables.


# Convert the flat fields specification to Frictionless Data

```sh
mititools convert flatfields frictionless
```

This creates `fd_data_package/datapackage.json`, as well as empty/default data tables.

Frictionless Data (FD) is an extensive and modular system of high-level data management tools, with consistent bindings in Python, JavaScript, and the bash command-line.

**Validation with FD**.

```sh
frictionless validate fd_data_package/datapackage.json
```

Output:

```
# -----
# valid: biospecimen.tsv
# -----
# -----
# valid: cell.tsv
# -----

...
```

**Description with FD**.

```sh
frictionless describe fd_data_package/cell.tsv
```

Output:

```yaml
# --------
# metadata: fd_data_package/cell.tsv
# --------

dialect:
  delimiter: "\t"
encoding: utf-8
format: tsv
hashing: md5
name: cell
path: fd_data_package/cell.tsv
profile: tabular-data-resource
schema:
  fields:
    - name: data_file_id
      type: any
    - name: filename
      type: any
    - name: file_format
      type: any
    - name: parent_id
      type: any
    - name: software_and_version
      type: any
    - name: commit_sha
      type: any
    - name: comment
      type: any
    - name: header_size
      type: any
    - name: object_classes_included
      type: any
    - name: object_classes_description
      type: any
    - name: fov_size_x
      type: any
    - name: fov_size_y
      type: any
    - name: pyramid
      type: any
    - name: z_stack
      type: any
    - name: t_series
      type: any
    - name: type
      type: any
    - name: physical_size_x
      type: any
    - name: physical_size_xunit
      type: any
    - name: physical_size_y
      type: any
    - name: physical_size_yunit
      type: any
    - name: physical_size_z
      type: any
    - name: physical_size_zunit
      type: any
    - name: cell_state_level
      type: any
scheme: file
```


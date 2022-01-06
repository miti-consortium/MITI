# mititools
These tools convert the MITI schema between 3 different formats:

1. `yaml`. The reference YAML specification, designed to be validated with [Cerberus](https://docs.python-cerberus.org/en/stable/).
2. `flatfields`. A specification based on a flat table of fields.
3. `frictionless`. A [Frictionless Data](https://frictionlessdata.io/standards/#standards-toolkit) [data package](https://specs.frictionlessdata.io/data-package/) schema.

The translation is not perfect, as the schema languages are not equivalent.

### Installation
From the top-level of this repository (probably called `MITI`), install this Python package with:

```sh
pip install mititools/
```

### Convert the Cerberus-validated YAML specification to flat fields

```sh
mititools convert yaml flatfields
```

This creates `flatfields/fields.tsv`, `flatfields/tables.tsv`, as well as empty/default data tables.


### Convert the flat fields specification to Frictionless Data

```sh
mititools convert flatfields frictionless
```

This creates `fd_data_package/datapackage.json`, as well as empty/default data tables.

Frictionless Data (FD) is an extensive and modular system of high-level data management tools, with consistent bindings in Python, JavaScript, and the bash command-line.

Validation with FD:

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


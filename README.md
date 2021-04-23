# MITI: Minimum Information about Tissue Imaging

Minimum Information about Tissue Images (MITI) reporting guidelines comprise minimal metadata for highly multiplexed tissue images and were developed in consultation with methods developers, experts in imaging metadata (e.g., DICOM and OME) and multiple large-scale atlasing projects; they are guided by existing standards and accommodate most multiplexed imaging technologies and both centralized and distributed data storage.

The YAML files in this repository provide detailed specification of the standard, as outlined in **[LINK TO PAPER]**. Individual files capture attributes, their description and significance, but also additional information that is essential for validating specific files; this includes ensuring that data in each field has the correct data type and that it meets constraints on valid values. Each attribute is associated with one of the following data types:

* `boolean`, `integer`, `float`, `string` - Standard data types representing boolean, integer, floating-point and character strings
* `filename` - A valid [POSIX-portable](https://www.ibm.com/docs/en/zos/2.2.0?topic=locales-posix-portable-file-name-character-set) filename
* `date` - A date specified in the [ISO 8601 standard](https://www.iso.org/iso-8601-date-and-time-format.html) YYYY-MM-DD
* `doi` - A valid [DOI identifier](https://www.doi.org/)

Valid values are specified as sets of predefined keywords for `string` and as [`min`, `max`] intervals for `integer` and `float` variables, where both `min` and `max` can be optionally omitted to define open intervals.

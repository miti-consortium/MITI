# MITI: Minimum Information about Tissue Imaging

Minimum Information about Tissue Images (MITI) reporting guidelines comprise minimal metadata for highly multiplexed tissue images and were developed in consultation with methods developers, experts in imaging metadata (e.g., DICOM and OME) and multiple large-scale atlasing projects; they are guided by existing standards and accommodate most multiplexed imaging technologies and both centralized and distributed data storage.

The YAML files in this repository provide detailed specification of the standard, as outlined in the corresponding **[manuscript](https://arxiv.org/abs/2108.09499)**. Individual files capture attributes, their description and significance, but also additional information that is essential for validating specific files; this includes ensuring that data in each field has the correct data type and that it meets constraints on valid values. Each attribute is associated with one of the following data types:

* `boolean`, `integer`, `float`, `string` - Standard data types representing boolean, integer, floating-point and character strings
* `filename` - A valid [POSIX-portable](https://www.ibm.com/docs/en/zos/2.2.0?topic=locales-posix-portable-file-name-character-set) filename
* `date` - A date specified in the [ISO 8601 standard](https://www.iso.org/iso-8601-date-and-time-format.html) YYYY-MM-DD
* `doi` - A valid [DOI identifier](https://www.doi.org/)
* `rrid` - A valid [Research Resource Identifier](https://scicrunch.org/resources)

Valid values are specified as sets of predefined keywords for `string` and as [`min`, `max`] intervals for `integer` and `float` variables, where both `min` and `max` can be optionally omitted to define one-sided intervals.

## Governance:
Changes to MITI require a submission via `Github Issues` with the following information:

* Scope and Field
* Summary of changes
* Example
* Implementation as a pull request

The community can discuss and vote for the submission via Github for at least 30 days.

The initial governance board comprises (i)  **Denis Schapiro**, PhD, Research Group Leader at the Heidelberg University (Chair); (ii) **Adam Taylor**, PhD, Senior Research Scientist, Sage Bionetworks; (iii) **Sarah Arena**, MS, Data Scientist, Harvard Medical School and (iv)  **Markus D. Herrmann**, MD, PhD, Assistant Professor of Pathology, Mass General Hospital.

The discussions should be limited to Github and `image.sc` forum in #mcmicro.

If the implementation needs a revision, this needs to be submitted latest 30 days after acceptance.

This board will remain for 12 months followed by a community based voting of a new governance board (4-5 board members) every January. New candidates can be proposed by board members, community members or via a direct application. Therefore, an issue will be opened (November) in this repository to collect names and for the voting via emojis. We welcome and encourage participation by everyone!

## Diversity statement¶

The MITI consortium welcomes and encourages participation by everyone. We are committed to being a community that everyone enjoys being part of. Although we may not always be able to accommodate each individual’s preferences, we try our best to treat everyone kindly.

No matter how you identify yourself or how others perceive you: we welcome you. Though no list can hope to be comprehensive, we explicitly honour diversity in: age, culture, ethnicity, genotype, gender identity or expression, language, national origin, neurotype, phenotype, political beliefs, profession, race, religion, sexual orientation, socioeconomic status, subculture and technical ability, to the extent that these do not conflict with this code of conduct.

## Example 1

The following YAML block defines a required attribute `Tumor tissue type` that relates to collection and processing of biospecimens. A valid field must be specified as a character string, using one of the pre-defined keywords: Primary Tumor, Local Tumor Recurrence, etc.

``` yaml
Tumor tissue type:
  description: Text that describes the kind of disease present in the tumor specimen
    as related to a specific time point.
  category: Collection and Processing
  type: string
  valid-values:
  - Primary Tumor
  - Local Tumor Recurrence
  - Distant Tumor Recurrence
  - Metastatic
  - Premalignant
  significance: required
```

## Example 2

The following YAML block defines a recommended attribute `Cycle Number`, which must be specified as a 1-based index (i.e., an integer belonging to the one-sided interval `[1, Inf)`).

``` yaml
Cycle Number:
  description: 'the cycle # in which the co-listed reagent(s) was(were) used'
  type: integer
  valid-values:
    min: 1.0
  significance: recommended
```

## Endnotes

We are thankful to the groups behind the following documents, from which we drew content and inspiration:

* [The napari Code of Conduct](https://github.com/napari)

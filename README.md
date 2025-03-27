# KBOpenBib Data

![License](https://img.shields.io/badge/License-CC0%5f1.0-orange)
![Python Version](https://img.shields.io/badge/Python-3.11-blue)
![Coverage](https://img.shields.io/badge/Coverage-99%25-4c1)

## About

The KBOpenBib project, maintained by the [Kompetenznetzwerk Bibliometrie](https://bibliometrie.info),  
provides access to curated OpenAlex data with a focus on the German research landscape.

Curated data is provided for following entities: 

- [Authors](docs/data_overview.md#-authors) 👩‍🎓
- [Publishers](docs/data_overview.md#-publishers) 📚
- [Funding information](docs/data_overview.md#-funding-information) 📄
- [Document types](docs/data_overview.md#-document-types) 🗂️
- [Address information](docs/data_overview.md#-address-information) 🏛️

Annual snapshots from the KBOpenBib project are openly available to users of the 
[Kompetenznetzwerk Bibliometrie](https://bibliometrie.info), via the 
[Open Scholarly Data Warehouse of the SUB Göttingen](https://subugoe.github.io/scholcomm_analytics/data.html)
and [Zenodo](https://zenodo.org).

The current release is based on the August 2024 snapshot of OpenAlex, limited to works
with publication years 2014 to 2024.

## Usage

<figure>
    <img src="examples/document_types_sectors.png" width="70%" />
    <figcaption>
        Fig.1: Classification of article and reviews in journals for German institutions in OpenAlex and by OPENBIB classifier.
    </figcaption>
</figure>

## How do I get it?

- If you are a user of the [Kompetenznetzwerk Bibliometrie](https://bibliometrie.info)
you can access the data snapshot via the KB data infrastructure hosted by FIZ Karlsruhe.

- For big scholarly data analysis in a Google Cloud environment, you can use the 
[Open Scholarly Data Warehouse](https://subugoe.github.io/scholcomm_analytics/data.html)
maintained by the SUB Göttingen.

- Alternatively, you can download the snapshot from Zenodo: https://zenodo.org. 

## Technical Documentation

- A list of all entities and fields included in the KBOpenBib snapshot can be found
[here](docs/data_overview).
- A guide for importing the KBOpenBib snapshot into a PostgreSQL environment can be 
found [here](docs/working_with_postgresql.md).
- A guide for importing the KBOpenBib snapshot into a Google BigQuery environment can be 
found [here](docs/working_with_bigquery.md).

## How I can get involved?

If you see mistakes, want to suggest changes or submit feature requests, please 
[create an issue](https://github.com/kbopenbib/kbopenbib_data/issues).

## License

## Citation

## Contact




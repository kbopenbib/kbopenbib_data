# KBOpenBib Data

![License](https://img.shields.io/badge/License-CC0%5f1.0-orange)
![Python Version](https://img.shields.io/badge/Python-3.11-blue)
![Coverage](https://img.shields.io/badge/Coverage-99%25-4c1)

## About

The OPENBIB project, maintained by the [Kompetenznetzwerk Bibliometrie](https://bibliometrie.info),  
provides access to curated OpenAlex data with a focus on the German research landscape.

Curated data is provided for following entities: 

- [Authors](docs/data_overview.md#-authors) 👩‍🎓
- [Publishers](docs/data_overview.md#-publishers) 📚
- [Funding information](docs/data_overview.md#-funding-information) 📄
- [Document types](docs/data_overview.md#-document-types) 🗂️
- [Address information](docs/data_overview.md#-address-information) 🏛️

Annual snapshots from the OPENBIB project are openly available to users of the 
[Kompetenznetzwerk Bibliometrie](https://bibliometrie.info), via the 
[Open Scholarly Data Warehouse of the SUB Göttingen](https://subugoe.github.io/scholcomm_analytics/data.html)
and [Zenodo](https://zenodo.org).

The current release is based on the August 2024 snapshot of OpenAlex, limited to works
with publication years 2014 to 2024.

## Usage

<figure>
    <img src="examples/kb_institution_disambiguation.png" width="70%" />
    <figcaption>
        <b>Fig.1:</b> Publications assigned to German institutions in OpenAlex and OPENBIB based on ROR-Matching. Only publications published between 2014 and 2024 are considered.
    </figcaption>
</figure>

<p></p>

<figure>
    <img src="examples/document_types_sectors.png" width="70%" />
    <figcaption>
        <b>Fig.2:</b> Classification of article and reviews in journals for German institutions in OpenAlex and by OPENBIB. Only publications published between 2014 and 2024 are considered.
    </figcaption>
</figure>

<p></p>

<figure>
    <img src="examples/funding_information_sectors.png" width="70%" />
    <figcaption>
        <b>Fig.3:</b> Publications containing funding information of the German Research Foundation in OpenAlex and by OPENBIB. Only publications published between 2020 and 2024 are considered. 
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

- A list of all entities and fields included in the OPENBIB snapshot can be found
[here](docs/data_overview.md).
- A guide for working with the OPENBIB snapshot in the KB data infrastructure can be 
found [here](examples/).
- A guide for working with the OPENBIB snapshot in the Open Scholarly 
Data Warehouse of the SUB Göttingen can be found [here](examples/bigquery_notebook.ipynb).

## How I can get involved?

If you see mistakes, want to suggest changes or submit feature requests, please 
[create an issue](https://github.com/kbopenbib/kbopenbib_data/issues).

## License

## Citation

## Contact




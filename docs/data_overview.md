# Working with OPENBIB data - Entities overview

This page contains a list of all entities included in the OPENBIB snapshot.
<br>
If you want detailed information about an individual entity, take a look at the [docs](../docs) directory.

- [Publishers](#-publishers)
- [Authors](#-authors)
- [Funding information](#-funding-information)
- [Document Types](#-document-types)
- [Address information](#-address-information)
- [Transformative Agreements](#-transformative-agreements)

## 📚 Publishers

### Publisher overview

The following table lists publishers with enriched information, including 
ROR and wikidata IDs.

Table: <i>add_publishers_20240831</i>

| Field | Type | Description |
|-------|------|-------------|
| publisher_id | INTEGER | The id for this publisher |
| publisher_id_orig | STRING | The OpenAlex id for this publisher |
| publisher_name | STRING | The name for this publisher |
| standard_name | STRING | The standardised name for this publisher |
| unit_pk | INTEGER | The internal ID for this publisher |
| wikidata | STRING | The Wikidata id for this publisher |
| ror | STRING | The ROR-id for this publisher |
| url | STRING | The URL for this publisher |

#### Example Record
```
publisher_id: 13711
publisher_id_orig: "https://openalex.org/P4310320330"
publisher_name: "Adis, Springer Healthcare"
standard_name: "Springer Healthcare"
unit_pk: 249
wikidata: "https://wikidata.org/wiki/Q52636673"
ror: ""
url: "https://springerhealthcare.com/"
```

### Relations between Publishers

The following table contains relationships between publishers, e.g. 
when a publisher belongs to another publisher.

Table: <i>add_publishers_relations_20240831</i>

| Field | Type | Description |
|-------|------|-------------|
| p_relation_id | INTEGER | The ID for this relation |
| child_name | STRING | The name of this publisher |
| child_id | STRING | The OpenAlex ID of this publisher |
| child_unit | INTEGER | The internal ID of this publisher |
| parent_name | STRING | The name of the parent publisher |
| parent_id | STRING | The OpenAlex ID of the parent publisher |
| parent_unit | INTEGER | The internal ID of this parent publisher |
| first_date | DATE | Date on which the connection to the parent publisher took place |
| last_date | DATE | Date on which the connection to the parent publisher was revoked |

#### Example Record
```
p_relation_id: 340
child_name: "BioMed Central"
child_id: "https://openalex.org/P4310320256"
child_unit: 81
parent_name: "Springer Science+Business Media"
parent_id: "https://openalex.org/P4310319900"
parent_unit: 79
first_date: "2008-10-01"
last_date: "2015-04-30"
```

## 👩‍🎓 Authors

The aim of curation is the automatic disambiguation of German Authors.

## 📄 Funding information

Funding information is provided for publications funded by the
German [Open-Access-Publikationskosten](https://www.dfg.de/en/research-funding/funding-opportunities/programmes/infrastructure/lis/funding-opportunities/open-access-publication-funding) program. 

Table: <i>add_funding_information_20240831</i>
<br>
Limitations: Only includes publications from 2022 to 2024
<br>

| Field | Type | Description |
|-------|------|-------------|
| openalex_id | STRING | The OpenAlex id of this work |
| doi | STRING | The DOI of this work |
| funding_id | TEXT | The grant id(s) we found for this work |

#### Example Record
```
openalex_id: "https://openalex.org/W4321327768"
doi: "10.1002/1873-3468.14601"
funding_id: ["430651076"]
```

## 🗂 Document types

Journals publish different types of scholarly works such as
research articles, reviews, book reviews, case reports and editorials.
The latter are sometimes classified as articles in OpenAlex. Using a machine 
learning classifier helps to distinguish between research
contributions and other types of works. 

Table: <i>add_document_types_20240831</i>
<br>
Limitations: Only includes articles and reviews from OpenAlex with the 
source type journal and the publication year 2014 to 2024.
<br>

| Field | Type | Description |
|-------|------|-------------|
| openalex_id | STRING | The OpenAlex id of this work |
| doi | STRING | The DOI of this work |
| is_research | BOOLEAN | True if the classifier detect this work as a research contribution |
| proba | FLOAT | The probability that this work is a research contribution |

#### Example Record
```
openalex_id: "https://openalex.org/W4256503663"
doi: "10.1016/s0099-2399(15)00667-6"
is_research: false
proba: 0.16
```

Examples of works that are considered as non-research publications by the classifier:
- https://openalex.org/works/W2264593839 (Abstract)
- https://openalex.org/works/W4256503663 (Table of Contents)
- https://openalex.org/works/W4400195825 (Book Review)
- https://openalex.org/works/W4255159712 (Case Report)

## 🏛 Address information

Disambiguation of address information is provided by the [Institute for Interdisciplinary Studies of
Science](https://www.uni-bielefeld.de/einrichtungen/i2sos/) in Bielefeld. 

Limitations: Only includes publications that are assigned to German institutions 
by the algorithm.

### Mode A

Mode A contains all assignments of publications to currently existing 
institutions.

#### Allocation of documents to institutions (Mode A)

Table: <i>add_address_information_a_addr_inst_sec_20240831</i>

| Field | Type | Description |
|-------|------|-------------|
| kb_inst_id | INTEGER | The institution id associated with this publication |
| openalex_id | STRING | The OpenAlex id associated with this publication |
| address_full | TEXT | The address string found for this publication in OpenAlex |
| kb_sector_id | STRING | The sector id(s) associated with this publication |
| doi | STRING | The DOI associated with this publication |
| identifier | STRING | The internal identifier for this publication |

#### Example Record
```
kb_inst_id: 5617
openalex_id: "https://openalex.org/W2074596230"
address_full: "Max-Plank-Institut für Biophysikalische Chemie, Göttingen, Germany, DE"
kb_sector_id: ["mpg"]
doi: "10.1007/s004310050674"
identifier: "10.1007/s004310050674§5617"
```

#### Allocation of institutions to sectors (Mode A)

Table: <i>add_address_information_a_inst_sec_20240831</i>

| Field | Type | Description |
|-------|------|-------------|
| kb_inst_id | INTEGER | The identifier for this institution |
| kb_sector_id | STRING | The sector id for this institution |

#### Example Record
```
kb_inst_id: 5617
kb_sector_id: "mpg"
```

### Mode S (Historic mode)

Mode S contains all assignments of publications to institutions that existed 
at the time of publication.

#### Allocation of documents to institutions (Mode S)

Table: <i>add_address_information_s_addr_inst_sec_20240831</i>

| Field | Type | Description |
|-------|------|-------------|
| kb_inst_id | INTEGER | The institution id associated with this publication |
| openalex_id | STRING | The OpenAlex id associated with this publication |
| address_full | TEXT | The address string found for this publication in OpenAlex |
| kb_sector_id | STRING | The sector id(s) associated with this publication |
| doi | STRING | The DOI associated with this publication |
| identifier | STRING | The internal identifier for this publication |

#### Example Record
```
kb_inst_id: 1073
openalex_id: "https://openalex.org/W3031617943"
address_full: "Department of Molecular Neurobiology, Max Planck Institute of Experimental Medicine, Göttingen 37075, Germany"
kb_sector_id: ["mpg"]
doi: "10.1016/j.isci.2020.101203"
identifier: "10.1016/j.isci.2020.101203§1073"
```

#### Allocation of institutions to sectors (Mode S)

Table: <i>add_address_information_s_inst_sec_20240831</i>

| Field | Type | Description |
|-------|------|-------------|
| kb_inst_id | INTEGER | The identifier for this institution |
| kb_sector_id | STRING | The sector id for this institution | 
| first_year | INTEGER | Date of the foundation of this institution (if available) |
| last_year | INTEGER | Year of closure of this institution (9999 if currently existing) |

#### Example Record
```
kb_inst_id: 1073
kb_sector_id: "mpg"
first_year: 1000
last_year: 9999
```

### Institutions

Table: <i>add_address_information_inst_20240831</i>

| Field | Type | Description |
|-------|------|-------------|
| kb_inst_id | INTEGER | The id of this institution |
| name | STRING | The name of this institution |
| first_year | INTEGER | Date of the foundation of this institution (if available) |
| last_year | INTEGER | Year of closure of this institution (9999 if currently existing) |
| ror | STRING | The ROR-id of this institution |
| dfg_instituts_id | INTEGER | The identifier assigned to this institution by the German Research Foundation |

#### Example Record
```
kb_inst_id: 137
name: "Universität Hamburg"
first_year: 1000
last_year: 9999
ror: "https://ror.org/00g30e956"
dfg_instituts_id: 10192
```

### Sectors

Table: <i>add_address_information_sectors_20240831</i>

| Field | Type | Description |
|-------|------|-------------|
| kb_sectorgroup_id | STRING | The abbreviation for this sector group |
| kb_sector_id | STRING | The id for this sector group |
| sectorgroup_name | STRING | The name of this sector group |
| sector_name | STRING | The name of this sector |
| remarks | STRING | A description of this sector |

#### Example Record
```
kb_sectorgroup_id: "FHG"
kb_sector_id: "fhg"
sectorgroup_name: "Fraunhofer-Gesellschaft"
sector_name: "Fraunhofer-Gesellschaft"
remarks: ""
```

###  Institutional changes

Table: <i>add_address_information_inst_trans_20240831</i>

| Field | Type | Description |
|-------|------|-------------|
| inst_ante | INTEGER | The institution id before the transition |
| transition_date | DATE | The date of the merger, inclusion or exclusion |
| inst_post | INTEGER | The institution id after the transition |
| type | STRING | The type of structural change (merger, inclusion, exclusion) |

#### Example Record
```
inst_ante: 1073
transition_date: "2022-01-01"
inst_post: 5617
type: "inclusion"
```

## 📑 Transformative Agreements

### Overview

This dataset comprises historic snapshots from the [cOAlitionS Transformative Agreements Public Data](https://journalcheckertool.org/transformative-agreements/) dump underlying the cOAlition S Journal Checker Tool (JCT). The data files were safeguarded on a weekly basis using a [robot](https://github.com/njahn82/jct_data).

### Dataset Components

The dataset consists of four primary tables:

1. `jct_journals` - Journals covered by transformative agreements
2. `jct_institutions` - Institutions participating in transformative agreements
3. `jct_articles` - Articles published under transformative agreements
4. `jct_esac` - Metadata about the transformative agreements from the ESAC registry

### Table Descriptions

#### Journals (`add_jct_journals_20240831`)

This table contains journals covered by transformative agreements. Journal ISSN variants are disambiguated using ISSN-L according to the ISSN agency.

| Field | Type | Description |
|-------|------|-------------|
| id | STRING | OpenAlex journal identifier |
| esac_id | STRING | Identifier for the transformative agreement |
| issn_l | STRING | ISSN-L identifying the journal |
| time_last_seen | TIMESTAMP | Last time this data was available in the Journal Checker Tool |
| commit | STRING | Data snapshot Git commit ID |

#### Example Record
```
id: "https://openalex.org/S2764691006"
esac_id: "acm2020delft"
issn_l: "2153-2184"
time_last_seen: "2024-04-01 09:23:06 UTC"
commit: "a689426e782c5f42b850b327a1a89d9ad9d19a16"
```

#### Institutions (`add_jct_institutions_20240831`)

This table maps institutions to transformative agreements they participate in. The institution data is enriched with associated ROR-IDs according to OpenAlex.

| Field | Type | Description |
|-------|------|-------------|
| id | STRING | OpenAlex institution identifier |
| esac_id | STRING | Identifier for the transformative agreement |
| ror_id | STRING | ROR-ID of the participating institution |
| time_last_seen | TIMESTAMP | Last time this data was available in the Journal Checker Tool |
| commit | STRING | Data snapshot Git commit ID |

#### Example Record
```
id: "https://openalex.org/I42934936"
esac_id: "acm2020ie"
ror_id: "https://ror.org/04a1a1e81"
time_last_seen: "2023-01-02 02:19:56 UTC"
commit: "fd749477fbe5e0d58040bdaa4466e63886e9fb17"
```

#### Articles (`add_jct_articles_20240831`)

This table contains articles enabled by transformative agreements based on first-author affiliations in OpenAlex.

| Field | Type | Description |
|-------|------|-------------|
| id | STRING | OpenAlex identifier for the publication |
| doi | STRING | Digital Object Identifier for the publication |
| matching_issn_l | STRING | ISSN-L identifying the journal |
| matching_ror | STRING | ROR-ID used to match between OpenAlex and Journal Checker Tool data |
| ror_type | STRING | Type of ROR match (e.g., "ror_jct") |
| esac_id | STRING | Identifier for the transformative agreement from ESAC Registry |
| start_date | DATE | Agreement start date |
| end_date | DATE | Agreement end date |
| publication_date | DATE | Publication date according to OpenAlex |

#### Example Record
```
id: "https://openalex.org/W3107077096"
doi: "10.1145/3428248"
matching_issn_l: "2475-1421"
matching_ror: "https://ror.org/02e2c7k09"
ror_type: "ror_jct"
esac_id: "acm2020delft"
start_date: "2020-11-01"
end_date: "2023-12-31"
publication_date: "2020-11-13"
```

#### ESAC Registry (`add_jct_esac_20240831`)

This table provides metadata about transformative agreements from the ESAC Registry.

| Field | Type | Description |
|-------|------|-------------|
| publisher | STRING | Name of the publisher |
| country | STRING | Country where the agreement is applicable |
| organization | STRING | Organization that negotiated the agreement |
| annual_publications | INTEGER | Estimated number of articles published annually under the agreement |
| start_date | TIMESTAMP | Agreement start date |
| end_date | TIMESTAMP | Agreement end date |
| id | STRING | Unique identifier for the agreement |
| url | STRING | URL to the agreement details in the ESAC Registry |
| jct_jn | BOOLEAN | Indicates if any journals are recorded under this agreement in JCT |
| jct_inst | BOOLEAN | Indicates if any institutions are recorded under this agreement in JCT |

#### Example Record
```
publisher: "Taylor & Francis"
country: "Austria"
organization: "KEMOE/FWF"
annual_publications: 70
start_date: "2014-01-01 00:00:00 UTC"
end_date: "2016-12-31 00:00:00 UTC"
id: "tf2014kemoe"
url: "https://esac-initiative.org/about/transformative-agreements/agreement-registry/tf2014kemoe/"
jct_jn: false
jct_inst: false
```

### Data Relationships

- **Articles to Journals**: Articles are linked to journals via the `matching_issn_l` field
- **Articles to Institutions**: Articles are linked to institutions via the `matching_ror` field
- **Agreements**: All tables are linked via the `esac_id` field representing specific transformative agreements
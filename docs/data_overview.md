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

```bash
publisher_id: 13711
publisher_id_orig: "https://openalex.org/P4310320330"
publisher_name: "Adis, Springer Healthcare"
standard_name: "Springer Healthcare"
unit_pk: 249
wikidata: "https://wikidata.org/wiki/Q52636673"
ror: ""
url: "https://springerhealthcare.com/"
```

#### Fields

- publisher_id (INTEGER): The id for this publisher.
- publisher_id_orig (STRING): The OpenAlex id for this publisher.
- publisher_name (STRING): The name for this publisher.
- standard_name (STRING): The standardised name for this publisher.
- unit_pk (INTEGER): The internal ID for this publisher.
- wikidata (STRING): The Wikidata id for this publisher.
- ror (STRING): The ROR-id for this publisher.
- url (STRING): The URL for this publisher.

### Relations between Publishers

The following table contains relationships between publishers, e.g. 
when a publisher belongs to another publisher.

Table: <i>add_publishers_relations_20240831</i>

```bash
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

#### Fields

- p_relation_id (INTEGER): The ID for this relation. 
- child_name (STRING): The name of this publisher.
- child_id (STRING): The OpenAlex ID of this publisher.
- child_unit (INTEGER): The internal ID of this publisher
- parent_name (STRING): The name of the parent publisher.
- parent_id (STRING): The OpenAlex ID of the parent publisher.
- parent_unit (INTEGER): The internal ID of this parent publisher.
- first_date (DATE): Date on which the connection to the parent publisher took place.
- last_date (DATE): Date on which the connection to the parent publisher was revoked.

## 👩‍🎓 Authors

The aim of curation is the automatic disambiguation of German Authors.

## 📄 Funding information

Funding information is provided for publications funded by the
German [Open-Access-Publikationskosten](https://www.dfg.de/en/research-funding/funding-opportunities/programmes/infrastructure/lis/funding-opportunities/open-access-publication-funding) program. 

Table: <i>add_funding_information_20240831</i>
<br>
Limitations: Only includes publications from 2022 to 2024
<br>

```bash
openalex_id: "https://openalex.org/W4321327768"
doi: "10.1002/1873-3468.14601"
funding_id: ["430651076"]
```

### Fields

- openalex_id (STRING): The OpenAlex id of this work.
- doi (STRING): The DOI of this work.
- funding_id (TEXT): The grant id(s) we found for this work. 

## 🗂 Document types

Journals publish different types of scholarly works such as
research articles, reviews, book reviews, case reports and editorials.
The latter are often classified as articles in OpenAlex. Using a machine 
learning classifier helps to distinguish between research
contributions and other types of works. 

Table: <i>add_document_types_20240831</i>
<br>
Limitations: Only includes articles and reviews from OpenAlex with the 
source type journal and the publication year 2014 to 2024.
<br>

```bash
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

### Fields

- openalex_id (STRING): The OpenAlex id of this work.
- doi (STRING): The DOI of this work.
- is_research (BOOLEAN): True if the classifier detect this work as a research contribution.
- proba (FLOAT): The probability that this work is a research contribution.

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

```bash
kb_inst_id: 5617
openalex_id: "https://openalex.org/W2074596230"
address_full: "Max-Plank-Institut für Biophysikalische Chemie, Göttingen, Germany, DE"
kb_sector_id: ["mpg"]
doi: "10.1007/s004310050674"
identifier: "10.1007/s004310050674§5617"
```

#### Fields 

- kb_inst_id (INTEGER): The institution id associated with this publication.
- openalex_id (STRING): The OpenAlex id associated with this publication.
- address_full (TEXT): The address string found for this publication in OpenAlex.
- kb_sector_id (STRING): The sector id(s) associated with this publication.
- doi (STRING): The DOI associated with this publication.
- identifier (STRING): The internal identifier for this publication.

#### Allocation of institutions to sectors (Mode A)

Table: <i>add_address_information_a_inst_sec_20240831</i>

```bash
kb_inst_id: 5617
kb_sector_id: "mpg"
```

#### Fields

- kb_inst_id (INTEGER): The identifier for this institution.
- kb_sector_id (STRING): The sector id for this institution.

### Mode S (Historic mode)

Mode S contains all assignments of publications to institutions that existed 
at the time of publication.

#### Allocation of documents to institutions (Mode S)

Table: <i>add_address_information_s_addr_inst_sec_20240831</i>

```bash
kb_inst_id: 1073
openalex_id: "https://openalex.org/W3031617943"
address_full: "Department of Molecular Neurobiology, Max Planck Institute of Experimental Medicine, Göttingen 37075, Germany"
kb_sector_id: ["mpg"]
doi: "10.1016/j.isci.2020.101203"
identifier: "10.1016/j.isci.2020.101203§1073"
```

#### Fields 

- kb_inst_id (INTEGER): The institution id associated with this publication.
- openalex_id (STRING): The OpenAlex id associated with this publication.
- address_full (TEXT): The address string found for this publication in OpenAlex.
- kb_sector_id (STRING): The sector id(s) associated with this publication.
- doi (STRING): The DOI associated with this publication.
- identifier (STRING): The internal identifier for this publication.

#### Allocation of institutions to sectors (Mode S)

Table: <i>add_address_information_s_inst_sec_20240831</i>

```bash
kb_inst_id: 1073
kb_sector_id: "mpg"
first_year: 1000
last_year: 9999
```

#### Fields 

- kb_inst_id (INTEGER): The identifier for this institution.
- kb_sector_id (STRING): The sector id for this institution. 
- first_year (INTEGER): Date of the foundation of this institution (if available).
- last_year (INTEGER): Year of closure of this institution (9999 if currently existing).

### Institutions

Table: <i>add_address_information_inst_20240831</i>

```bash
kb_inst_id: 137
name: "Universität Hamburg"
first_year: 1000
last_year: 9999
ror: "https://ror.org/00g30e956"
dfg_instituts_id: 10192
```

#### Fields 

- kb_inst_id (INTEGER): The id of this institution.
- name (STRING): The name of this institution.
- first_year (INTEGER): Date of the foundation of this institution (if available).
- last_year (INTEGER): Year of closure of this institution (9999 if currently existing).
- ror (STRING): The ROR-id of this institution.
- dfg_instituts_id (INTEGER): The identifier assigned to this institution by the German Research Foundation.

### Sectors

Table: <i>add_address_information_sectors_20240831</i>

```bash
kb_sectorgroup_id: "FHG"
kb_sector_id: "fhg"
sectorgroup_name: "Fraunhofer-Gesellschaft"
sector_name: "Fraunhofer-Gesellschaft"
remarks: ""
```

#### Fields 

- kb_sectorgroup_id (STRING): The abbreviation for this sector group.
- kb_sector_id (STRING): The id for this sector group.
- sectorgroup_name (STRING): The name of this sector group.
- sector_name (STRING): The name of this sector.
- remarks (STRING): A description of this sector.

###  Institutional changes

Table: <i>add_address_information_inst_trans_20240831</i>

```bash
inst_ante: 1073
transition_date: "2022-01-01"
inst_post: 5617
type: "inclusion"
```

- inst_ante (INTEGER): The institution id before the transition.
- transition_date (DATE): The date of the merger, inclusion or exclusion.
- inst_post (INTEGER): The institution id after the transition. 
- type (STRING): The type of structural change (merger, inclusion, exclusion).

## 📑 Transformative Agreements

### Articles

Table: <i>add_jct_articles_20240831</i>

```bash
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

#### Fields

- id (STRING): The OpenAlex id associated with this publication.
- doi (STRING): The DOI associated with this publication. 
- matching_issn_l (STRING): 
- matching_ror (STRING): 
- esac_id (STRING): 
- start_date (DATE):
- end_date (DATE):
- publication_date (DATE):

### ESAC

Table: <i>add_jct_esac_20240831</i>

```bash
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

#### Fields

- publisher (STRING): 
- country (STRING): 
- organization (STRING): 
- annual_publications (INTEGER): 
- start_date (TIMESTAMP): 
- end_date (TIMESTAMP):
- id (STRING):
- url (STRING):
- jct_jn (BOOL):
- jct_inst (BOOL):

### Institutions

Table: <i>add_jct_institutions_20240831</i>

```bash
id: "https://openalex.org/I42934936"
esac_id: "acm2020ie"
ror_id: "https://ror.org/04a1a1e81"
time_last_seen: "2023-01-02 02:19:56 UTC"
commit: "fd749477fbe5e0d58040bdaa4466e63886e9fb17"
```

#### Fields

- id (STRING): 
- esac_id (STRING): 
- ror_id (STRING): 
- time_last_seen (TIMESTAMP): 
- commit (STRING):

### Journals

Table: <i>add_jct_journals_20240831</i>

```bash
id: "https://openalex.org/S2764691006"
esac_id: "acm2020delft"
issn_l: "2153-2184"
time_last_seen: "2024-04-01 09:23:06 UTC"
commit: "a689426e782c5f42b850b327a1a89d9ad9d19a16"
```

#### Fields

- id (STRING): 
- esac_id (STRING): 
- issn_l (STRING): 
- time_last_seen (TIMESTAMP): 
- commit (STRING):
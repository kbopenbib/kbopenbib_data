# Working with KBOpenBib data - Entities overview

This page contains a list of all entities included in the KBOpenbib snapshot.
<br>
If you want detailed information about an individual entity, take a look at the [docs](../docs) directory.
## Publishers

Table: <i>kb_publisher_standard_relation</i>

```bash
publisher_id: 13711
publisher_id_orig: "P4310320330"
publisher_name: "Adis, Springer Healthcare"
standard_name: "Springer Healthcare"
unit_pk: 249
other_name: "Adis, Springer Healthcare"
wikidata: "Q52636673"
ror: ""
url: "https://springerhealthcare.com/"
parent_name: "Springer Nature"
parent_id: "P4310319965"
parent_unit: 220
```

### Fields

- publisher_id (INTEGER): The id for this publisher.
- publisher_id_orig (STRING): The OpenAlex id for this publisher.
- publisher_name (STRING): The name for this publisher.
- standard_name (STRING): The standardised name for this publisher.
- unit_pk (INTEGER): 
- other_name (STRING): Other names for this publisher.
- wikidata (STRING): The Wikidata id for this publisher.
- ror (STRING): The ROR-id for this publisher.
- url (STRING): The URL for this publisher.
- parent_name (STRING): The name for the parent organisation of this publisher.
- parent_id (STRING): The OpenAlex id for the parent organisation of this publisher.
- parent_unit (INTEGER):

## Authors

## Funding information

Table: <i>dfg_oa</i>
<br>
Limitations: Only includes publications from 2022 to 2024
<br>

```bash
openalex_id: "W4321327768"
doi: "10.1002/1873-3468.14601"
funding_id: ["430651076"]
```

### Fields

- openalex_id (STRING): The OpenAlex id of this work.
- doi (STRING): The DOI of this work.
- funding_id (TEXT): The grant id(s) we found for this work. 

## Document types

Table: <i>classification_article_reviews_2014_2024_august24 (placeholder)</i>
<br>
Limitations: Only includes articles and reviews with the source type journal from 2014 onwards.
<br>

A machine learning classifier detects whether an article or review
is actually a research contribution or not.

```bash
openalex_id: "W4256503663"
doi: "10.1016/s0099-2399(15)00667-6"
is_research: False
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
- is_research (BOOLEAN): True if our classifier detect this work as a research contribution.
- proba (FLOAT): The probability that this work is a research contribution.

## Address information

### Modus A

#### kb_a_addr_inst_sec_open_alex

Table: <i>kb_a_addr_inst_sec_oa_b_20240831</i>

```bash
kb_inst_id: 5617
openalex_id: "W2074596230"
address_full: "Max-Plank-Institut für Biophysikalische Chemie, Göttingen, Germany, DE"
kb_sector_id: ["mpg"]
doi: "10.1007/S004310050674"
identifier: "10.1007/S004310050674§5617"
```

#### Fields 

- kb_inst_id (INTEGER): The institution id associated with this publication.
- openalex_id (STRING): The OpenAlex id associated with this publication.
- address_full (TEXT): The address string found for this publication in OpenAlex.
- kb_sector_id (STRING): The sector id(s) associated with this publication.
- doi (STRING): The DOI associated with this publication.
- identifier (STRING): 

#### kb_a_inst_sec_open_alex

Table: <i>kb_a_inst_sec_oa_b_20240831</i>

```bash
kb_inst_id: 5617
kb_sector_id: "mpg"
```

#### Fields

- kb_inst_id (INTEGER): The identifier for this institution.
- kb_sector_id (STRING): The sector id for this institution.

### Modus S (Historic mode)

#### kb_s_addr_inst_sec_open_alex

Table: <i>kb_s_addr_inst_sec_oa_b_20240831</i>

```bash
kb_inst_id: 142
openalex_id: "W2097461905"
address_full: "Department for Bioanalytics, Georg-August University Göttingen, Göttingen, Germany."
kb_sector_id: ["uni"]
doi: "10.1038/NMETH.3493"
identifier: "10.1038/NMETH.3493§142"
```

#### Fields 

- kb_inst_id (INTEGER): The institution id associated with this publication.
- openalex_id (STRING): The OpenAlex id associated with this publication.
- address_full (TEXT): The address string found for this publication in OpenAlex.
- kb_sector_id (STRING): The sector id(s) associated with this publication.
- doi (STRING): The DOI associated with this publication.
- identifier (STRING):  

#### kb_s_inst_sec_open_alex

Table: <i>kb_s_inst_sec_oa_b_20240831</i>

```bash
kb_inst_id: 142
kb_sector_id: "uni"
first_year: 1000
last_year: 9999
```

#### Fields 

- kb_inst_id (INTEGER): The identifier for this institution.
- kb_sector_id (STRING): The sector id for this institution. 
- first_year (INTEGER): Date of the foundation of this institution (if available).
- last_year (INTEGER): Year of closure of this institution (9999 if currently existing).

### Institutions

#### kb_inst_open_alex

Table: <i>kb_inst_oa_b_20240831</i>

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

#### kb_sectors_open_alex

Table: <i>kb_sectors_oa_b_20240831</i>

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

####  kb_inst_trans_open_alex

Table: <i>kb_inst_trans_oa_b_20240831</i>

```bash
inst_ante: 854
transition_date: "2008-01-01"
inst_post: 801
type: "fusion"
```

- inst_ante (INTEGER): The institution id before the transition.
- transition_date (DATE): The date of the merger, inclusion or exclusion.
- inst_post (INTEGER): The institution id after the transition. 
- type (STRING): The type of structural change (merger, inclusion, exclusion).


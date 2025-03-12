# Funding information

## Overview

On behalf of the DFG, FZ Jülich collects data on the use of open access funding from the DFG by German research organizations. This funding comes from the "Open-Access-Publikationskosten" program, to which institutions can apply. The funded institutions are expected to deliver data to FZ Jülich about the publications whose open access publication was financed with these funds. In the first phase of the program (2022-2024), institutions that received the subsidies could use them for any open access publications meeting the funding criteria that they were billed for. When reporting them to FZ Jülich, institutions had the option of supplying DFG funding identifiers. In those cases in which this was done, one can reasonably assume that the OA subsidies were in fact used specifically for the publications of the named DFG research projects.

This subset of publications registered at FZ Jülich by funded institutions with specific DFG research projects mentioned is provided for further analysis of DFG funding data presence in OpenAlex data in the OpenBib project.

## Data and data structure

The data is uploaded to the KB relational database in the table `kb_project_openbib.dfg_oa` with the following table structure:

```sql
doi	        text
funding_id	text[]
item_id_oal	text
```
	
Column 'doi' contains the DOI of the paper. 'funding_id' is a text array which contains all DFG project identifiers provided by the institutions for that DOI. 'item_id_oal' is the OpenAlex item ID for that DOI. The data was cleaned by removing 9 records with missing DOI and removing 112 duplicates of records, keeping only the first occurrence of any DOI.

This dataset contains 9255 records of which 9217, or 99.6%, could by identified in OpenAlex (20240831 version).

The funding identifiers are stored in a text array column, as there can be several for each publication. To get the funding_id data in a simpler table structure, the `unnest()` function can be used, like in this example, which calculate the average number of funding IDs per publication:

```sql
SELECT avg(c)
FROM (
    SELECT doi, count(funding_id) c
    FROM (
        SELECT doi, unnest(funding_id) funding_id
        FROM kb_project_openbib.dfg_oa
    ) a
    GROUP BY doi
) b;
┌────────────────────┐
│        avg         │
├────────────────────┤
│ 1.3827120475418693 │
└────────────────────┘
```

## Example analysis

We next provide some initial analysis how this data can be linked to OpenAlex data and how this may be useful for users to better assess the data of OpenAlex.

We begin with a simple analysis of the publications' publication years:

```sql
SELECT pubyear, count(*)
FROM fiz_openalex_bdb_20240831_openbib.items
WHERE item_id IN (
    SELECT item_id_oal
    FROM kb_project_openbib.dfg_oa 
    WHERE item_id_oal IS NOT NULL
)
GROUP BY ROLLUP(pubyear)
ORDER BY pubyear;

┌─────────┬───────┐
│ pubyear │ count │
├─────────┼───────┤
│    2020 │     4 │
│    2021 │    41 │
│    2022 │  2637 │
│    2023 │  6300 │
│    2024 │   235 │
│         │  9217 │
└─────────┴───────┘
```

As is to be expected, they fall well within the official funding period of 'Open-Access-Publikationskosten' with most appearing in 2023. Reassuringly, the total figure is also 9217, which means there is a valid publication year present in OpenAlex for every record that could be linked.



With the next query, we look at OpenAlex's new 'topics' (https://docs.openalex.org/api-entities/topics) classification system, specifically the top 10 classes into which the ostensibly DFG funded open access publications are assigned. Not shown below is that they fall into 1992 out of a total of 4518 topic classes in the OpenAlex system.

```sql
SELECT class_name[1], count(*)
FROM fiz_openalex_bdb_20240831_openbib.items
WHERE item_id IN (
    SELECT item_id_oal
    FROM kb_project_openbib.dfg_oa 
    WHERE item_id_oal IS NOT NULL
)
GROUP BY ROLLUP(class_name[1])
ORDER BY 2 DESC
LIMIT 11;

┌────────────────────────────────────────────────────────────┬───────┐
│                         class_name                         │ count │
├────────────────────────────────────────────────────────────┼───────┤
│                                                            │  9217 │
│ Particle Physics and High-Energy Collider Experiments      │   227 │
│ Neuronal Oscillations in Cortical Networks                 │    57 │
│ Tectonic and Geochronological Evolution of Orogens         │    56 │
│ Neural Mechanisms of Cognitive Control and Decision Making │    54 │
│ Coronavirus Disease 2019 Research                          │    50 │
│ Chemistry of Main Group Elements and Compounds             │    47 │
│ Climate Change and Paleoclimatology                        │    44 │
│ Two-Dimensional Materials                                  │    44 │
│ Ribosome Structure and Translation Mechanisms              │    44 │
│ Impact of Pollinator Decline on Ecosystems and Agriculture │    39 │
└────────────────────────────────────────────────────────────┴───────┘
```
	
Now for something more directly relevant to funding data. With this query, we can calculate for how many of the records OpenAlex also has funding information that states the papers were funded by DFG. The result of 5509 papers is about 60 % of the OA-Monitor dataset.

```sql
SELECT count(distinct item_id)
FROM fiz_openalex_bdb_20240831_openbib.funding_agencies_grants
WHERE item_id IN (
    SELECT item_id_oal
    FROM kb_project_openbib.dfg_oa
    WHERE item_id_oal IS NOT NULL
)
AND funding_agency = 'Deutsche Forschungsgemeinschaft';

┌───────┐
│ count │
├───────┤
│  5509 │
└───────┘
```

The German organizations responsible for the papers and OA funding are also of interest. One way to get an approximate notion of the most important organizations is to look at the papers' corresponding authors and their institutional affiliations, as disambiguated by OpenAlex:

```sql
SELECT org, count(*) c
FROM (
    SELECT ia.item_id, aa.organization[1] org
    FROM fiz_openalex_bdb_20240831_openbib.items_authors ia
    JOIN fiz_openalex_bdb_20240831_openbib.authors_affiliations aa ON (ia.item_id, ia.author_seq_nr) = (aa.item_id, aa.author_seq_nr)
    WHERE ia.item_id IN (
        SELECT item_id_oal
        FROM kb_project_openbib.dfg_oa
        WHERE item_id_oal IS NOT NULL
    )
    AND ia.corresponding = true
) a
GROUP BY org
ORDER BY c DESC
LIMIT 10;

┌────────────────────────────────────────┬─────┐
│                  org                   │  c  │
├────────────────────────────────────────┼─────┤
│ University of Göttingen                │ 371 │
│ University of Potsdam                  │ 331 │
│ University of Stuttgart                │ 274 │
│ TU Dresden                             │ 177 │
│ University of Cologne                  │ 141 │
│ Humboldt-Universität zu Berlin         │ 140 │
│ Ludwig-Maximilians-Universität München │ 139 │
│ Ruhr University Bochum                 │ 130 │
│ Leibniz University Hannover            │ 122 │
│ Heidelberg University                  │ 120 │
└────────────────────────────────────────┴─────┘
```
	
The whole list included 515 institutions, many of which are not located in Germany.

The colleagues at Bielefeld University have worked on a first trial version of the KB German institution disambiguation system for OpenAlex. However, use of this data and interpretation of any results must be very careful because of important differences in the data of OpenAlex compared to that of the commercial data providers. In the recent test bibliometric databases for OpenAlex there is no comparable data in the author sequence number and affiliation sequence number columns loaded yet. The trial institution disambiguation is therefore not set up to work at the level of specific author-address combinations of publications but only at the linking level of publications. We cannot make any restriction to corresponding authors either. Also, the trial disambiguation was built for an older OpenAlex snapshot (fiz_openalex_rep_20230819_openbib), so the publication figures are not comparable. Nevertheless, just counting the total number of papers per institution in the DFG open access dataset with the trial version German institution coding, we can get the following result.

```sql
SELECT name, count(item_id)
FROM (
SELECT DISTINCT k.name, kboal.item_id
FROM kb_project_openbib.kb_a_addr_inst_sec_open_alex kboal
JOIN kb_project_openbib.kb_inst_open_alex k ON kboal.kb_inst_id = k.kb_inst_id
WHERE kboal.item_id IN (
    SELECT item_id_oal
    FROM kb_project_openbib.dfg_oa
    WHERE item_id_oal IS NOT NULL)
) a
GROUP BY name
ORDER BY 2 DESC
LIMIT 10;

┌──────────────────────────────────────────────┬───────┐
│                     name                     │ count │
├──────────────────────────────────────────────┼───────┤
│ Georg-August-Universität Göttingen           │   854 │
│ Universität Potsdam                          │   518 │
│ Ludwig-Maximilians-Universität München (LMU) │   501 │
│ Technische Universität Dresden               │   426 │
│ Ruprecht-Karls-Universität Heidelberg        │   415 │
│ Humboldt-Universität zu Berlin               │   346 │
│ Universität Stuttgart                        │   335 │
│ Universität zu Köln                          │   324 │
│ Philipps-Universität Marburg                 │   315 │
│ Eberhard Karls Universität Tübingen          │   300 │
└──────────────────────────────────────────────┴───────┘
```

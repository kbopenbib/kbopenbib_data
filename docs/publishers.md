# Publisher data in OpenAlex

In the OpenAlex database, a large number of publishers have been given a standardized name instead of different name variants. Each publisher record receives a publisher ID (e.g. P4323430492). 
Relationships (child-parent) are also displayed in some cases and links are created to external IDs such as Wikidata and ROR.

However, the analyses of publishers at the level of individual publications shows a large number of publisher names without OpenAlex publisher IDs and thus without name normalization. Since OpenAlex has many different sources, it is probably not possible to keep all data up to date and clean.

For the KB OpenBib project, a supplementary standardization of publishers has therefore been carried out based on the OpenAlex data. This should simplify the evaluation of publications by publishers: results summarize different designations and thus facilitate the search for all publications belonging to a publisher. 
Relationships between publishers are shown in another table. These can be helpful if, for example, imprints and sub-publishers are to be identified under the label of the main publisher.

## Procedure 

From OpenAlex (OpenBib version with data as of 31.08.2024), all publishers with the number of publications from the publications from the publication year 2014 onwards have been compiled in a table. They are supplemented (if available) with the publisher, Wikidata and ROR IDs as well as an URL from OpenAlex. 
The table was reduced to publishers in Latin spelling. 

The Wikidata IDs, ROR IDs and URLs were used to merge the actual publisher names with the standard names. The given names and standard names were also compared as substrings and the result was manually checked for correctness.

Tabelle **add_publishers_20240831** 

| table field       | data                                    |
|-------------------|-----------------------------------------|
| publisher_id      | 34297                                   |
| publisher_id_orig | P4366736682                             |
| publisher_name    | Nature Publishing Group                 |
| standard_name     | Nature Portfolio                        |
| unit_pk           | 182                                     |
| wikidata          | Q180419                                 |
| ror               | 03dsk4d59                               |
| url               | https://www.nature.com/nature-portfolio |

Tabelle **add_publishers_relations_20240831** 

| table field       | data                              |
|-------------------|-----------------------------------|
| p_relation_id     | 337                               |
| child_name        | Nature Portfolio                  |
| child_id          | P4310319908                       |
| child_unit        | 182                               |
| parent_name       | Macmillan Publishers              |
| parent_id         | P4310319964                       |
| parent_unit       | 38                                |
| first_date        | 1999-01-01                        |
| last_date         | 2015-04-30                        |

## Conventions

Starting from the publishers with the highest publication numbers, standard names with an ID were assigned to each publisher in a new table. 
In doing so, different spellings of publishers were combined to form one publisher name (e.g. Multidisciplinary Digital Publishing Institute or MDPI AG to MDPI), taking into account the publisher standard names already created by OpenAlex. 
If the current name was unclear, the English name was usually taken from Wikidata.

Information about the relationships between publishers sometimes includes details of the period of validity of a relationship; publishers can also have more than one entry in the table due to changes in affiliation. The table is under construction and does not claim to be complete.

## Application scenarios

For example, to query the publications of the Nomos publishing house, all publisher IDs or publisher names found in the **add_publishers_20240831** table under the standard **Nomos** are determined. When querying the publications in the items table, they are specified as a where condition.

The **add_publishers_relations_20240831** table indicates that Nomos-Verlag is part of C.H. Beck-Verlag. This can be taken into account in an overall query for the publisher C.H. Beck by additionally selecting the Publisher_ID of the Nomos-Verlag in a query.
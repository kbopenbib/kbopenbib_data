# Authors
## Note 
    Due to computational restraints, the Author data is still processingas of 2nd May 2025. It will be added to the open data release when complete.
##
Our aim is to provide better author disambiguation for German authors specifically, to this end we have created a machine learning pipeline to discriminate which authorships belong to which author. We shall refer to this as Author Name Disambiguation (AND). 

## Data Gathering
We selected a combination of attributes from the authorship and work metadata in OpenAlex. 

Our restrictions were German affiliated works (the country code of the authorship), non-retracted records and a time restriction from 2000-2024.

The attributes selected were:
From Authorships:
    * raw_author_name,
    * author_position,
    * author_id,
    * work_id
From Works (and related tables):
    * doi,
    * title,
    * keywords,
    * publication_date,
    * publication_year,
    * type,
    * referenced_work_ids (from reference table),
    * primary_topic,
    * source_id (from source table)

### Statistics (to update)

| Measure | Count |
| -- | -- |
| Authorships (Count of rows) | - |
| Unique OpenAlex WorkIDs | - |
| Unique OpenAlex AuthorIDs | - |
| Unique Orcids | - |
| Authorships without Orcid | - |
| Unique Raw Name Strings | -  |


This gives an average of - authors per WorkID, - works per AuthorID, - works per Orcid.

## Blocking
AND algorithms reduce the number of comparisons required by filtering names which are very unlikely to be referring to the same person into equivalence classes or blocks. For example if two authors have different last and first names it is assumed it is unlikely that these are the same person. This is not always the case, for example when someone changes their last name after marriage or parnership, or changes their first name for personal reasons, however for computing over such a large corpus such generalisations are required.
### Last Name First Initial (LNFI) Blocking
LNFI blocking takes the last name and first initial of a raw author name and uses this as the equivalence class. 

E.g:

*Jack H. Culbert* = *Culbert J*

For computational efficiency the last name is placed first.

### Progressive Blocking - In Progress
Future releases may incorporate a progressive blocking algorithm following the work of Dr. Backes, more information may be found [here](https://nbn-resolving.org/urn:nbn:de:hbz:061-20230411-132939-9). 

## Modelling
### Logistic Embedding

Hyperparameter | Value      |
| -- | -- |
| | |

#### Statistics

### Graph Embedding - In Progress
A more sophisticated model is being developed within the KB utilizing a graph embedding model, however this was not ready in time for this data release.
## Performance Analysis
### Comparisons to OpenAlex
### Comparisons to Orcid

## Using the data

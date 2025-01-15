# Working with KBOpenBib data

## Publishers 

## Journals

## Authors

## Funding information

```sql
SELECT doi, openalex_id, funding_id
FROM kb_project_openbib.dfg_oa
```

### Fields

- openalex_id (STRING): The OpenAlex id of this work.
- doi (STRING): The DOI of this work.
- funding_id (TEXT): The grant id(s) we found for this work. 

## Document types
The table <i>classification_article_reviews</i> contains articles
and reviews with the source type journal from 2014 onwards.
A machine learning classifier detects whether an article or review
is actually a research contribution or not.

```sql
SELECT doi, openalex_id
FROM kb_project_openbib.classification_article_reviews
WHERE is_research=TRUE
```

Examples of works that are considered as non-research publications by the classifier:
- https://openalex.org/works/W2264593839 (Abstract)
- https://openalex.org/works/W4256503663 (Table of Contents)
- https://openalex.org/works/W4246924978 (Table of Contents)

### Fields

- openalex_id (STRING): The OpenAlex id of this work.
- doi (STRING): The DOI of this work.
- is_research (BOOLEAN): True if our classifier detect this work as a research contribution.
- proba (FLOAT): The probability that this work is a research contribution.

## Address information


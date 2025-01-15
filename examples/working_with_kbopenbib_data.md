# Working with KBOpenBib data

## Publishers 

## Journals

## Authors

## Funding information

### Fields

- openalex_id (STRING)
- doi (STRING)
- funding_id (TEXT)

## Document types
The table <i>classification_article_reviews</i> contains articles
and reviews with the source type journal from 2014 onwards.
A machine learning classifier detects whether an article or review
is actually a research contribution or not.

```sql
SELECT COUNT(DISTINCT(doi)), is_research
FROM kb_project_openbib.classification_article_reviews
GROUP BY is_research
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


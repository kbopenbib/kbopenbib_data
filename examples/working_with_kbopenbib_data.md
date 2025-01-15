# Working with KBOpenBib data

## Publishers 

## Journals

## Authors

## Funding information

```bash
openalex_id: "W4361302015"
doi: "10.3390/mti7040037"
funding_id: ["DFG 32955190"]
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

```bash
openalex_id: "https://openalex.org/W4256503663"
doi: "10.1016/s0099-2399(15)00667-6"
is_research: False
proba: 0.18
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


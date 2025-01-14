# Working with KBOpenBib data

## Publishers 

## Journals

## Authors

## Funding information

## Document types

```sql
SELECT COUNT(DISTINCT(doi)), is_research
FROM  kb_project_openbib.classification_article_reviews
GROUP BY is_research
```

## Address information


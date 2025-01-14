# Working with PostgreSQL

## Create a table in your database

```sql
create table kb_project_openbib.classification_article_reviews_december24 (
	openalex_id text,
	doi text,
	is_research boolean,
	proba float
)
```

## Load data into the table

Tools used: 
- jq (https://jqlang.github.io/jq/)
- spyql (https://github.com/dcmoura/spyql)
- psql (https://www.postgresql.org)

```bash
$ cat document_types.jsonl | \
  jq -c '{openalex_id: .openalex_id, doi: .doi, is_research: .is_research, proba: .proba}' | \
  spyql -Otable=classification_article_reviews_december24 \
  'IMPORT json AS js SELECT json->openalex_id, json->doi, json->is_research, json->proba FROM json TO sql' | \
  psql postgresql://{NAME}:{PASSWORD}@{SERVER}:{PORT}/{DATABASE}
```

## Query the data

```sql
SELECT COUNT(DISTINCT(doi)), is_research
FROM  kb_project_openbib.classification_article_reviews_december24
GROUP BY is_research
```
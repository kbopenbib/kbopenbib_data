# Working with PostgreSQL

This guide shows you how you can work with OpenBib data in a 
[PostgreSQL](https://www.postgresql.org) environment. We assume that you
have already worked with PostgreSQL and have a running instance. 

## Create a table in your database

If you want to work with a specific table from the OpenBib snapshot, 
you do not have to write a schema yourself. We have already prepared 
schemas for you that you can reuse. You can find these schemas [here](../schemas).

```sql
create table kb_project_openbib.classification_article_reviews (
	openalex_id text,
	doi text,
	is_research boolean,
	proba float
)
```

There is a difference between JSONL and CSV files in the snapshot. 
While the JSONL files contain arrays and nested fields, this is not 
the case with CSV files. Keep this in mind when reusing a schema. 
You may need to adapt array types to non-array types as we have unpacked 
arrays for CSV files during export.

## Load data into the table

There are many ways to import data into a database. Here we use the 
terminal to upload data to a previously defined table.

The following tools were used: 
- jq (https://jqlang.github.io/jq/)
- spyql (https://github.com/dcmoura/spyql)
- psql (https://www.postgresql.org)

```bash
$ cat document_types.jsonl | \
  jq -c '{openalex_id: .openalex_id, doi: .doi, is_research: .is_research, proba: .proba}' | \
  spyql -Otable=classification_article_reviews \
  'IMPORT json AS js SELECT json->openalex_id, json->doi, json->is_research, json->proba FROM json TO sql' | \
  psql postgresql://{NAME}:{PASSWORD}@{SERVER}:{PORT}/{DATABASE}
```

## Query the data

Once you have uploaded files from the snapshot to the database, 
you can finally query the data:

```sql
SELECT COUNT(DISTINCT(doi)), is_research
FROM  kb_project_openbib.classification_article_reviews
GROUP BY is_research
```
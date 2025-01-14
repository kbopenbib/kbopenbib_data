# Working with BigQuery

## 1. Install gcloud CLI

https://cloud.google.com/sdk/docs/install

## 2. Create a Table in BigQuery

```bash
$ bq load
  --source_format=NEWLINE_DELIMITED_JSON
  project_id:dataset.table
  path_to_file
  path_to_schema
```

## 3. Query a Table in BigQuery 

```sql
SELECT *
FROM project_id:dataset.table
```
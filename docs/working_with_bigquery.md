# Working with BigQuery

This guide shows you how you can work with OpenBib data in a 
[Google BigQuery](https://cloud.google.com/bigquery?hl=en) environment. 
We assume that you have already worked with BigQuery and have a running instance. 

## 1. Install gcloud CLI

To upload files from your computer to BigQuery, you can either use the web 
interface or an official client. For this guide we use the Google Cloud SDK. 
You can download it here: https://cloud.google.com/sdk/docs/install

## 2. Create a Table in BigQuery

After you have installed the client you can use the command `bq mk` to 
create a dataset within BigQuery.

```bash
$ bq mk openbib_snapshot
```

Once you have created a dataset, you can upload the OpenBib snapshot to it. 
Use the `bq load` command for this. Replace `path_to_file` and `path_to_schema` 
with the file you want to upload and the corresponding schema. You can find 
schemas for different tables [here](../schemas/bigquery)

```bash
$ bq load
  --source_format=NEWLINE_DELIMITED_JSON
  project_id:openbib_snapshot.table 
  path_to_file # files/document_types.jsonl
  path_to_schema # schemas/bigquery/document_types.json
```

## 3. Query a Table in BigQuery 

After files has been uploaded, you can now query the data!

```sql
SELECT *
FROM project_id:openbib_snapshot.table
```
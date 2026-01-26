# Author Disambiguation

## Overview

Author name disambiguation (AND) is a critical challenge in bibliometrics because the same person may appear under different name variations, and different people may share the same name. OpenAlex provides author identifiers, but these can be incomplete or inconsistent, particularly for authors without ORCIDs.

We developed a machine learning classifier to disambiguate authors in German-affiliated publications. The classifier uses a logistic regression model trained on author pairs where ORCID matches serve as ground truth. Features include name similarity, publication year differences, affiliation overlap, institutional co-occurrence, and shared references.

The approach uses Last Name First Initial (LNFI) blocking to reduce the comparison space, generating approximately 869 million author pairs from 9.2 million authorship records. The model achieves 96.94% accuracy on held-out test data.

## Data

The results are uploaded to the KB relational database in two tables:

**Author-level predictions** in `add_author_disambig_author_level`:

```sql
work_id                   TEXT NOT NULL
author_id                 TEXT NOT NULL
predicted_author_id       TEXT
orcid                     TEXT
final_author_prediction   TEXT
certainty                 DOUBLE PRECISION
```

Column `work_id` contains the OpenAlex work identifier. `author_id` is the OpenAlex author identifier for this authorship. `predicted_author_id` is the disambiguated cluster ID (either an ORCID URL or a generated cluster ID like `CLUSTER_00348118`). `orcid` contains the known ORCID if present in the source data. `final_author_prediction` prefers the known ORCID when available, falling back to the predicted cluster ID. `certainty` is a confidence score between 0 and 1, calculated as the average match probability from the logistic regression model.

This table contains 9,165,443 authorship records.

**Work-level predictions** in `add_author_disambig_work_level`:

```sql
work_id                   TEXT NOT NULL
final_predicted_authors   TEXT[]
```

Column `work_id` contains the OpenAlex work identifier. `final_predicted_authors` is a text array containing all disambiguated author identifiers for that work.

This table contains 2,786,294 work records.

To expand the author array into individual rows, use the `unnest()` function:

```sql
SELECT work_id, unnest(final_predicted_authors) AS author
FROM kb_project_openbib.add_author_disambig_work_level
LIMIT 10;
```

## Example Analysis

To examine the distribution of certainty scores to understand prediction confidence:

```sql
SELECT
    CASE
        WHEN certainty >= 0.9 THEN '0.9-1.0 (high confidence)'
        WHEN certainty >= 0.7 THEN '0.7-0.9 (medium confidence)'
        WHEN certainty >= 0.5 THEN '0.5-0.7 (low confidence)'
        ELSE '< 0.5 (uncertain)'
    END AS confidence_band,
    COUNT(*) AS n,
    ROUND(100.0 * COUNT(*) / SUM(COUNT(*)) OVER (), 2) AS pct
FROM kb_project_openbib.add_author_disambig_author_level
GROUP BY 1
ORDER BY 1 DESC;
```

To find authors with the most publications in the disambiguated dataset:

```sql
SELECT final_author_prediction, COUNT(*) AS n_authorships
FROM kb_project_openbib.add_author_disambig_author_level
GROUP BY final_author_prediction
ORDER BY n_authorships DESC
LIMIT 20;
```

To compare our predictions against known ORCIDs (validation):

```sql
SELECT
    CASE WHEN orcid IS NOT NULL THEN 'Has ORCID' ELSE 'No ORCID' END AS orcid_status,
    COUNT(*) AS n,
    ROUND(AVG(certainty), 3) AS avg_certainty
FROM kb_project_openbib.add_author_disambig_author_level
GROUP BY 1;
```

To identify works with multiple authors and examine the disambiguation:

```sql
SELECT
    w.work_id,
    array_length(w.final_predicted_authors, 1) AS n_authors,
    w.final_predicted_authors
FROM kb_project_openbib.add_author_disambig_work_level w
WHERE array_length(w.final_predicted_authors, 1) > 5
LIMIT 10;
```

To find cases where our prediction differs from the OpenAlex author_id:

```sql
SELECT
    work_id,
    author_id AS openalex_author_id,
    final_author_prediction,
    certainty
FROM kb_project_openbib.add_author_disambig_author_level
WHERE final_author_prediction != author_id
    AND certainty > 0.9
LIMIT 20;
```

## Interpretation

The `final_author_prediction` column contains two types of values:

- **ORCID URLs** (e.g., `https://orcid.org/0000-0001-7063-9334`): The author was matched to a known ORCID, either from the source data or through clustering with other ORCID-bearing records.

- **Cluster IDs** (e.g., `CLUSTER_00348118`): The author was grouped with similar authors based on the machine learning model, but no ORCID was available for the cluster.

Higher `certainty` scores indicate stronger evidence for the cluster assignment based on name similarity, institutional overlap, co-authorship patterns, and shared references.

## Pipeline

The disambiguation pipeline processes German-affiliated publications from OpenAlex (2000-2024):

1. **Data Extraction** — Extract author and work metadata from the OpenAlex July 2025 snapshot, filtering for German-affiliated, non-retracted records.

2. **Blocking** — Block authors by Last Name, First Initial (LNFI) to reduce the comparison space to manageable subgroups.

3. **Data Aggregation** — Denormalize author records with work metadata, aggregating institution IDs, source IDs, keywords, and references into arrays.

4. **Pair Generation** — Generate all author pairs within each blocking group (~869 million pairs) and compute similarity features: name similarity, year difference, title similarity, affiliation overlap, institution overlap, source overlap, keyword overlap, reference overlap, and topic match.

5. **Model Training** — Train a logistic regression classifier using pairs from ORCID-containing blocking groups, with ORCID match as the ground truth label. (Achieves 96.94% accuracy.)

6. **Prediction** — Apply the trained model to all pairs, outputting binary predictions and match probabilities.

7. **Clustering** — Use Union-Find to group predicted matches into author clusters. Assign cluster IDs prioritizing known ORCIDs.

8. **Certainty Scoring** — Calculate confidence scores for each author by averaging match probabilities from connected edges.

9. **Output Generation** — Format results into author-level and work-level prediction tables with final disambiguated identifiers and certainty scores.


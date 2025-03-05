# Document Types
 
We identified certain types of works that are classified as journal 
articles in OpenAlex.
Among these are:
- Book Reviews
- Paratexts (e.g. Frontmatter, Table of Contents, Ads)
- Editorial Materials (e.g. Editorials, Letter to the Editor)
- Conference articles 
- (Structured) Abstracts
- Case Reports

Based on these findings, we have developed a machine learning classifier with the
purpose to support the identification of those types of works. The classifier uses
open metadata such as the number of references and the number of authors that 
are linked to a publication.

The results of this approach are structured as follows. For each publication, a
probability score is calculated that represents whether a publication is a 
research article or not. If the probability score is higher or equal to 0.5, 
the publication will be classified as a research article. 

```bash
openalex_id: "W4256503663"
doi: "10.1016/s0099-2399(15)00667-6"
is_research: False
proba: 0.16
```

These scores can now be used to analyse journals that contain a higher 
frequency of non-research items. 

```sql
SELECT s.display_name AS journal, is_research, COUNT(DISTINCT(doi)) AS n
FROM kb_project_openbib.classification_article_reviews_2014_2024_august24 AS dt
JOIN fiz_openalex_rep_20240831_openbib.works_primary_locations AS wpl
	ON LOWER(TRIM('https://openalex.org/' FROM dt.openalex_id)) = LOWER(wpl.work_id)
JOIN fiz_openalex_rep_20240831_openbib.sources AS s
	ON LOWER(wpl.source_id) = LOWER(s.id)
GROUP BY journal, is_research
ORDER BY n DESC
```

For example, among the journals with the highest percentage of 
classified non-research publications are sources like 

- Reactions Weekly (mainly publishes case reports)
- Eos (mainly publishes news in popular scientific form)
- Physics Today (mainly publishes news in popular scientific form)
- ISEE Conference Abstracts (mainly publishes abstracts)
- The Proceedings of the Annual Convention of the Japanese Psychological Association (mainly publishes abstracts)
- PharmacoEconomics & Outcomes News (mainly publishes clinical studies and news)
- Bulletin of the Center for Children's Books./Bulletin of the Center for Children's Books (mainly publishes book reviews)

## Info

For more information about the classifier, see: https://subugoe.github.io/scholcomm_analytics/posts/oal_document_types_classifier/

The source code used for the classifier can be found here: https://github.com/naustica/openalex_doctypes/tree/classifier/classifier
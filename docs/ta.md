# Transformative Agreements Dataset

This dataset preserves historical records of transformative agreements in scholarly publishing. By linking agreement data with OpenAlex and using standardised identifiers (ISSN-L, ROR), it enables research on these agreements' evolution and impact over time.

## About 

Research studies increasingly examine transformative agreements' impact on scholarly publishing. Unfortunately, information about this licensing model is only partly available and scattered around various open data sources.

For example, the cOAlition SJournal Checker Tool, which is the most comprehensive source for journals and intuitions covered by transformative agreements, provides data only for current agreements; information about expired agreements is regularly deleted, limiting longitudinal studies.

This dataset combines open data from various sources to improve transparency around transformative agreements and estimates articles published under these agreements in OpenAlex. It uses transformative agreement data from the Journal Checker Tool for information about journal portfolios and participating institutions.

The data were normalised using ISSN-L for journals (according to the ISSN Agency) and associated ROR-IDs (according to OpenAlex).

Due to limited public invoicing data, articles published under transformative agreements were identified by linking first author affiliations from OpenAlex to eligible institutions according to agreement data.

The dataset aims to support empirical research on open access business models and transformative agreements.

In the following, the methods and use-cases are presented.

## Methods

A [bot](https://github.com/njahn82/jct_data/) has been fetching the cOAlition S Public Transformative Agreement Data dump serving the Journal Checker Tool weekly since December 2022. The resulting data versions were saved using Git and are available via GitHub. To combine these snapshots, the weekly git versions were checked out and the resulting data combined (see [script](https://github.com/njahn82/jct_data/blob/main/combine.R)). As the Transformative Agreement Data are continuously curated, only the most recent data about an agreement were safeguarded. For expired agreements, this represented the latest snapshot available.

The Transformative Agreement Data dumps link agreements to journals represented by journal names and ISSN. After mapping ISSN variants to the corresponding linking ISSN (ISSN-L), as provided by the ISSN International Centre, journals were associated with publishers according to the ESAC Transformative Agreement Registry. This reflects that some portfolios may include imprints.

Transformative Agreement Data did not comprehensively cover associated institutions, such as university hospitals or institutes of large research organisations like the Max Planck Society. To improve matching, Transformative Agreement Data were automatically enriched with ROR-IDs from associated organisations according to OpenAlex's institution entity data.

To estimate articles enabled by transformative agreements, article metadata were retrieved for each journal from OpenAlex. Then, participating institutions were matched with the first author affiliations recorded by OpenAlex. The matching considered first author affiliations instead of corresponding author affiliation due to the lack of corresponding author data in OpenAlex. Matching also considered the duration of agreements according to the ESAC registry.

The matching was carried out on [Google BigQuery](https://console.cloud.google.com/bigquery) for performance reasons.

The compilation of the datasets was carried out in April 2025 using the most recent datasets.

## Data files

You can find the documentation of data files in the [data documentation](data_overview.md#-transformative-agreements)

## Use case


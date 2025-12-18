import pandera as pa

jct_esac_schema = pa.DataFrameSchema(
    columns={
        'publisher': pa.Column(str, nullable=True, required=True),
        'country': pa.Column(str, nullable=True, required=True),
        'organization': pa.Column(str, nullable=True, required=True),
        'annual_publications': pa.Column(int, nullable=True, required=True),
        'start_date': pa.Column(str, nullable=True, required=True),
        'end_date': pa.Column(str, nullable=True, required=True),
        'id': pa.Column(str, nullable=True, required=True),
        'url': pa.Column(str, nullable=True, required=True),
        'jct_jn': pa.Column(bool, nullable=True, required=True),
        'jct_inst': pa.Column(bool, nullable=True, required=True)
    },
    index=pa.Index(int),
)

jct_institutions_schema = pa.DataFrameSchema(
    columns={
        'esac_id': pa.Column(str, nullable=True, required=True),
        'inst_name': pa.Column(str, nullable=True, required=True),
        'ror_id': pa.Column(str, nullable=True, required=True),
        'time_last_seen': pa.Column(str, nullable=True, required=True),
        'commit_hash': pa.Column(str, nullable=True, required=True)
    },
    index=pa.Index(int),
)

jct_journals_schema = pa.DataFrameSchema(
    columns={
        'esac_id': pa.Column(str, nullable=True, required=True),
        'issn_l': pa.Column(str, nullable=True, required=True),
        'time_last_seen': pa.Column(str, nullable=True, required=True),
        'commit_hash': pa.Column(str, nullable=True, required=True)
    },
    index=pa.Index(int),
)

jct_articles_schema = pa.DataFrameSchema(
    columns={
        'id': pa.Column(str, nullable=True, required=True,
                        checks=pa.Check(lambda s: s.str.startswith('https://openalex.org/'))),
        'doi': pa.Column(str, nullable=True, required=True),
        'matching_issn_l': pa.Column(str, nullable=True, required=True),
        'matching_ror': pa.Column(str, nullable=True, required=True),
        'ror_type': pa.Column(str, nullable=True, required=True),
        'esac_id': pa.Column(str, nullable=True, required=True),
        'start_date': pa.Column(str, nullable=True, required=True),
        'end_date': pa.Column(str, nullable=True, required=True),
        'publication_date': pa.Column(str, nullable=True, required=True)
    },
    index=pa.Index(int),
)
import pandera as pa

document_type_schema = pa.DataFrameSchema(
    columns={
        'openalex_id': pa.Column(str, nullable=True, required=True,
                                 checks=pa.Check(lambda s: s.str.startswith('https://openalex.org/'))),
        'doi': pa.Column(str, nullable=True, required=True),
        'is_research': pa.Column(bool, required=True),
        'proba': pa.Column(float, required=True)
    },
    index=pa.Index(int),
)
import pandera as pa

document_type_schema = pa.DataFrameSchema(
    columns={
        'openalex_id': pa.Column(str, nullable=True, required=True),
        'doi': pa.Column(str, nullable=True, required=True),
        'is_research': pa.Column(bool, required=True),
        'proba': pa.Column(float, required=True)
    },
    index=pa.Index(int),
)
import pandera as pa

publisher_schema = pa.DataFrameSchema(
    columns={
        'publisher_id': pa.Column(int, nullable=True, required=True),
        'publisher_id_orig': pa.Column(str, nullable=True, required=True),
        'publisher_name': pa.Column(str, nullable=True, required=True),
        'standard_name': pa.Column(str, nullable=True, required=True),
        'unit_pk': pa.Column(int, nullable=True, required=True),
        'other_name': pa.Column(str, nullable=True, required=True),
        'wikidata': pa.Column(str, nullable=True, required=True),
        'ror': pa.Column(str, nullable=True, required=True),
        'url': pa.Column(str, nullable=True, required=True),
        'parent_name': pa.Column(str, nullable=True, required=True),
        'parent_id': pa.Column(str, nullable=True, required=True),
        'parent_unit': pa.Column(float, nullable=True, required=True),
    },
    index=pa.Index(int),
)
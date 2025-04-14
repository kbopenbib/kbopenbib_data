import pandera as pa

publisher_schema = pa.DataFrameSchema(
    columns={
        'publisher_id': pa.Column(int, nullable=True, required=True),
        'publisher_id_orig': pa.Column(str, nullable=True, required=True,
                                       checks=pa.Check(lambda s: s.str.startswith('https://openalex.org/'))),
        'publisher_name': pa.Column(str, nullable=True, required=True),
        'standard_name': pa.Column(str, nullable=True, required=True),
        'unit_pk': pa.Column(int, nullable=True, required=True),
        'wikidata': pa.Column(str, nullable=True, required=True,
                              checks=pa.Check(lambda s: s.str.startswith('https://wikidata.org/wiki/'))),
        'ror': pa.Column(str, nullable=True, required=True,
                         checks=pa.Check(lambda s: s.str.startswith('https://ror.org/'))),
        'url': pa.Column(str, nullable=True, required=True)
    },
    index=pa.Index(int),
)

publisher_relation_schema = pa.DataFrameSchema(
    columns={
        'p_relation_id': pa.Column(int, nullable=True, required=True),
        'child_name': pa.Column(str, nullable=True, required=True),
        'child_id': pa.Column(str, nullable=True, required=True,
                              checks=pa.Check(lambda s: s.str.startswith('https://openalex.org/'))),
        'child_unit': pa.Column(int, nullable=True, required=True),
        'parent_name': pa.Column(str, nullable=True, required=True),
        'parent_id': pa.Column(str, nullable=True, required=True,
                               checks=pa.Check(lambda s: s.str.startswith('https://openalex.org/'))),
        'parent_unit': pa.Column(int, nullable=True, required=True),
        'first_date': pa.Column(str, nullable=True, required=True),
        'last_date': pa.Column(str, nullable=True, required=True)
    },
    index=pa.Index(int),
)
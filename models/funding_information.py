import pandera as pa
from typing import List

funding_information_schema_nested = pa.DataFrameSchema(
    columns={
        'openalex_id': pa.Column(str, nullable=True, required=True),
        'doi': pa.Column(str, nullable=True, required=True),
        'funding_id': pa.Column(List[str], nullable=True, required=True, coerce=True),
    },
    index=pa.Index(int),
)

funding_information_schema_unnested = pa.DataFrameSchema(
    columns={
        'openalex_id': pa.Column(str, nullable=True, required=True),
        'doi': pa.Column(str, nullable=True, required=True),
        'funding_id': pa.Column(str, nullable=True, required=True, coerce=True),
    },
    index=pa.Index(int),
)
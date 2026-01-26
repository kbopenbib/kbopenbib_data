import pandera as pa
from typing import List

author_disambiguation_work_level_schema_nested = pa.DataFrameSchema(
    columns={
        'work_id': pa.Column(str, nullable=True, required=True,
                             checks=pa.Check(lambda s: s.str.startswith('https://openalex.org/'))),
        'final_predicted_authors': pa.Column(List[str], nullable=True, required=True)
    },
    index=pa.Index(int),
)

author_disambiguation_work_level_schema_unnested = pa.DataFrameSchema(
    columns={
        'work_id': pa.Column(str, nullable=True, required=True,
                             checks=pa.Check(lambda s: s.str.startswith('https://openalex.org/'))),
        'final_predicted_authors': pa.Column(str, nullable=True, required=True)
    },
    index=pa.Index(int),
)

author_disambiguation_author_level_schema = pa.DataFrameSchema(
    columns={
        'work_id': pa.Column(str, nullable=True, required=True,
                             checks=pa.Check(lambda s: s.str.startswith('https://openalex.org/'))),
        'author_id': pa.Column(str, nullable=True, required=True,
                               checks=pa.Check(lambda s: s.str.startswith('https://openalex.org/'))),
        'predicted_author_id': pa.Column(str, nullable=True, required=True),
        'orcid': pa.Column(str, nullable=True, required=True),
        'final_author_prediction': pa.Column(str, nullable=True, required=True),
        'certainty': pa.Column(float, nullable=True, required=True)
    },
    index=pa.Index(int),
)
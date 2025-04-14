import pandera as pa
from typing import List

kb_a_addr_inst_sec_schema_nested = pa.DataFrameSchema(
    columns={
        'kb_inst_id': pa.Column(int, required=True),
        'openalex_id': pa.Column(str, nullable=True, required=True,
                                 checks=pa.Check(lambda s: s.str.startswith('https://openalex.org/'))),
        'address_full': pa.Column(str, required=True),
        'kb_sector_id': pa.Column(List[str], nullable=True, required=True),
        'doi': pa.Column(str, nullable=True, required=True),
        'identifier': pa.Column(str, required=True)
    },
    index=pa.Index(int),
)

kb_a_addr_inst_sec_schema_unnested = pa.DataFrameSchema(
    columns={
        'kb_inst_id': pa.Column(int, required=True),
        'openalex_id': pa.Column(str, nullable=True, required=True,
                                 checks=pa.Check(lambda s: s.str.startswith('https://openalex.org/'))),
        'address_full': pa.Column(str, required=True),
        'kb_sector_id': pa.Column(str, nullable=True, required=True),
        'doi': pa.Column(str, nullable=True, required=True),
        'identifier': pa.Column(str, required=True)
    },
    index=pa.Index(int),
)

kb_a_inst_sec_schema = pa.DataFrameSchema(
    columns={
        'kb_inst_id': pa.Column(int, required=True),
        'kb_sector_id': pa.Column(str, required=True)
    },
    index=pa.Index(int),
)

kb_s_addr_inst_sec_schema_nested = pa.DataFrameSchema(
    columns={
        'kb_inst_id': pa.Column(int, required=True),
        'openalex_id': pa.Column(str, nullable=True, required=True,
                                 checks=pa.Check(lambda s: s.str.startswith('https://openalex.org/'))),
        'address_full': pa.Column(str, required=True),
        'kb_sector_id': pa.Column(List[str], nullable=True, required=True),
        'doi': pa.Column(str, nullable=True, required=True),
        'identifier': pa.Column(str, required=True)
    },
    index=pa.Index(int),
)

kb_s_addr_inst_sec_schema_unnested = pa.DataFrameSchema(
    columns={
        'kb_inst_id': pa.Column(int, required=True),
        'openalex_id': pa.Column(str, nullable=True, required=True,
                                 checks=pa.Check(lambda s: s.str.startswith('https://openalex.org/'))),
        'address_full': pa.Column(str, required=True),
        'kb_sector_id': pa.Column(str, nullable=True, required=True),
        'doi': pa.Column(str, nullable=True, required=True),
        'identifier': pa.Column(str, required=True)
    },
    index=pa.Index(int),
)

kb_s_inst_sec_schema = pa.DataFrameSchema(
    columns={
        'kb_inst_id': pa.Column(int, required=True),
        'kb_sector_id': pa.Column(str, required=True),
        'first_year': pa.Column(int, required=True),
        'last_year': pa.Column(int, required=True)
    },
    index=pa.Index(int),
)

kb_inst_schema = pa.DataFrameSchema(
    columns={
        'kb_inst_id': pa.Column(int, required=True),
        'name': pa.Column(str, nullable=True, required=True),
        'first_year': pa.Column(int, required=True),
        'last_year': pa.Column(int, required=True),
        'ror': pa.Column(str, nullable=True, required=True),
        'dfg_instituts_id': pa.Column(int, nullable=True, required=True)
    },
    index=pa.Index(int),
)

kb_sectors_schema = pa.DataFrameSchema(
    columns={
        'kb_sectorgroup_id': pa.Column(str, required=True),
        'kb_sector_id': pa.Column(str, nullable=True, required=True),
        'sectorgroup_name': pa.Column(str, required=True),
        'sector_name': pa.Column(str, required=True),
        'remarks': pa.Column(str, nullable=True, required=True),
    },
    index=pa.Index(int),
)

kb_inst_trans_schema = pa.DataFrameSchema(
    columns={
        'inst_ante': pa.Column(int, required=True),
        'transition_date': pa.Column(str, nullable=True, required=True),
        'inst_post': pa.Column(int, required=True),
        'type': pa.Column(str, required=True)
    },
    index=pa.Index(int),
)
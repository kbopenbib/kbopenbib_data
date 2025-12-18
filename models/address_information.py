import pandera as pa
from typing import List

kb_a_addr_inst_sec_schema_nested = pa.DataFrameSchema(
    columns={
        'inst_id_top': pa.Column(int, required=True),
        'openalex_id': pa.Column(str, nullable=True, required=True,
                                 checks=pa.Check(lambda s: s.str.startswith('https://openalex.org/'))),
        'address_full': pa.Column(str, required=True),
        'sector_id': pa.Column(List[str], nullable=True, required=True),
        'doi': pa.Column(str, nullable=True, required=True),
        'identifier': pa.Column(str, required=True)
    },
    index=pa.Index(int),
)

kb_a_addr_inst_sec_schema_unnested = pa.DataFrameSchema(
    columns={
        'inst_id_top': pa.Column(int, required=True),
        'openalex_id': pa.Column(str, nullable=True, required=True,
                                 checks=pa.Check(lambda s: s.str.startswith('https://openalex.org/'))),
        'address_full': pa.Column(str, required=True),
        'sector_id': pa.Column(str, nullable=True, required=True),
        'doi': pa.Column(str, nullable=True, required=True),
        'identifier': pa.Column(str, required=True)
    },
    index=pa.Index(int),
)

kb_s_addr_inst_sec_schema_nested = pa.DataFrameSchema(
    columns={
        'inst_id_top': pa.Column(int, required=True),
        'openalex_id': pa.Column(str, nullable=True, required=True,
                                 checks=pa.Check(lambda s: s.str.startswith('https://openalex.org/'))),
        'address_full': pa.Column(str, required=True),
        'sector_id': pa.Column(List[str], nullable=True, required=True),
        'doi': pa.Column(str, nullable=True, required=True),
        'identifier': pa.Column(str, required=True)
    },
    index=pa.Index(int),
)

kb_s_addr_inst_sec_schema_unnested = pa.DataFrameSchema(
    columns={
        'inst_id_top': pa.Column(int, required=True),
        'openalex_id': pa.Column(str, nullable=True, required=True,
                                 checks=pa.Check(lambda s: s.str.startswith('https://openalex.org/'))),
        'address_full': pa.Column(str, required=True),
        'sector_id': pa.Column(str, nullable=True, required=True),
        'doi': pa.Column(str, nullable=True, required=True),
        'identifier': pa.Column(str, required=True)
    },
    index=pa.Index(int),
)

kb_inst_name_lookup_schema = pa.DataFrameSchema(
    columns={
        'inst_id': pa.Column(int, required=True),
        'name': pa.Column(str, required=True)
    },
    index=pa.Index(int),
)

kb_sector_name_lookup_schema = pa.DataFrameSchema(
    columns={
        'sector_id': pa.Column(str, required=True),
        'name': pa.Column(str, required=True)
    },
    index=pa.Index(int),
)

kb_inst_lookup_schema_nested = pa.DataFrameSchema(
    columns={
        'inst_id': pa.Column(int, required=True),
        'first_year': pa.Column(int, required=True),
        'last_year': pa.Column(int, required=True),
        'ror': pa.Column(str, nullable=True, required=True,
                         checks=pa.Check(lambda s: s if not isinstance(s,
                                                                       str) else s.str.startswith('https://ror.org/'))),
        'dfg_instituts_id': pa.Column(int, nullable=True, required=True),
        'current_sectors': pa.Column(List[str], nullable=True, required=True)
    },
    index=pa.Index(int),
)

kb_inst_lookup_schema_unnested = pa.DataFrameSchema(
    columns={
        'inst_id': pa.Column(int, required=True),
        'first_year': pa.Column(int, required=True),
        'last_year': pa.Column(int, required=True),
        'ror': pa.Column(str, nullable=True, required=True,
                         checks=pa.Check(lambda s: s if not isinstance(s,
                                                                       str) else s.str.startswith('https://ror.org/'))),
        'dfg_instituts_id': pa.Column(int, nullable=True, required=True),
        'current_sectors': pa.Column(str, nullable=True, required=True)
    },
    index=pa.Index(int),
)

kb_sector_lookup_schema = pa.DataFrameSchema(
    columns={
        'sector_id': pa.Column(str, nullable=True, required=True),
        'sectorgroup_id': pa.Column(str, required=True),
        'sectorgroup_name': pa.Column(str, required=True),
        'remarks': pa.Column(str, nullable=True, required=True),
    },
    index=pa.Index(int),
)
create table kb_project_openbib.kb_a_addr_inst (
    inst_id_top integer,
    openalex_id text,
    address_full text,
    sector_id text[],
    doi text,
    identifier text,
)

create table kb_project_openbib.kb_s_addr_inst (
    inst_id_top integer,
    openalex_id text,
    address_full text,
    sector_id text[],
    doi text,
    identifier text
)

create table kb_project_openbib.kb_inst_name_lookup (
    inst_id integer,
    name text,
)

create table kb_project_openbib.kb_sector_name_lookup (
    sector_id text,
    name text,
)

create table kb_project_openbib.kb_inst_lookup (
    inst_id integer,
    name text,
    first_year integer,
    last_year integer,
    ror text,
    dfg_instituts_id integer,
    current_sectors text[]
)

create table kb_project_openbib.kb_sector_lookup (
    sector_id text,
    sectorgroup_id text,
    sectorgroup_name text,
    remarks text
)
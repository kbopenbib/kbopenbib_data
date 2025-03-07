create table kb_project_openbib.kb_a_addr_inst_sec_open_alex (
	kb_inst_id integer
    openalex_id text
    address_full text
    kb_sector_id text[]
    doi text
    identifier text
)

create table kb_project_openbib.kb_a_inst_sec_open_alex (
	kb_inst_id integer
    kb_sector_id text[]
)

create table kb_project_openbib.kb_s_addr_inst_sec_open_alex (
	kb_inst_id integer
    openalex_id text
    address_full text
    kb_sector_id text[]
    doi text
    identifier text
)

create table kb_project_openbib.kb_s_inst_sec_open_alex (
	kb_inst_id integer
    kb_sector_id text[]
    first_year integer
    last_year integer
)

create table kb_project_openbib.kb_inst_open_alex (
	kb_inst_id integer
    name text
    first_year integer
    last_year integer
    ror text
    dfg_instituts_id integer
)

create table kb_project_openbib.kb_sectors_open_alex (
	kb_sectorgroup_id text
    kb_sector_id text
    sectorgroup_name text
    sector_name text
    remarks text
)

create table kb_project_openbib.kb_inst_trans_open_alex (
	inst_ante integer
    transition_date text
    inst_post integer
    type text
)
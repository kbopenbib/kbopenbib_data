create table kb_project_openbib.publishers (
    publisher_id integer,
    publisher_id_orig text,
    publisher_name text,
    standard_name text,
    unit_pk integer,
    wikidata text,
    ror text,
    url text
)

create table kb_project_openbib.publishers_relations (
    p_relation_id integer,
    child_name text,
    child_id text,
    child_unit integer,
    parent_name text,
    parent_id text,
    parent_unit integer,
    first_date date,
    last_date date
)
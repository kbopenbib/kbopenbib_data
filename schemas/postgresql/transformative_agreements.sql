create table kb_project_openbib.jct_esac (
    publisher text,
    country text,
    organization text,
    annual_publications int,
    start_date timestamp,
    end_date timestamp,
    id text,
    url text,
    jct_jn bool,
    jct_inst bool
)

create table kb_project_openbib.jct_institutions (
    id text,
    esac_id text,
    ror_id text,
    time_last_seen timestamp,
    commit text
)

create table kb_project_openbib.jct_journals (
    id text,
    esac_id text,
    issn_l text,
    time_last_seen timestamp,
    commit text
)

create table kb_project_openbib.jct_articles (
    id text,
    doi text,
    matching_issn_l text,
    matching_ror text,
    ror_type text,
    esac_id text,
    start_date date,
    end_date date,
    publication_date date
)
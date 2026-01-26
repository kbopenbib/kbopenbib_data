create table kb_project_openbib.author_disambiguation_author_level (
	work_id text,
	author_id text,
	predicted_author_id text,
	orcid text,
	final_author_prediction text,
	certainty float
)

create table kb_project_openbib.author_disambiguation_work_level (
	work_id text,
	final_predicted_authors text[]
)
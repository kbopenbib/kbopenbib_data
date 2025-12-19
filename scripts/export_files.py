import os
import pandas as pd
import json
from sqlalchemy import create_engine
import shutil
from pathlib import Path
from models.document_type import document_type_schema
from models.funding_information import funding_information_schema_nested
from models.publisher import publisher_schema, publisher_relation_schema
from models.address_information import (kb_a_addr_inst_sec_schema_nested,
                                        kb_s_addr_inst_sec_schema_nested,
                                        kb_inst_name_lookup_schema,
                                        kb_sector_name_lookup_schema,
                                        kb_inst_lookup_schema_nested,
                                        kb_sector_lookup_schema)
from models.transformative_agreements import (jct_institutions_schema,
                                              jct_journals_schema,
                                              jct_articles_schema,
                                              jct_esac_schema)
import logging
import sys

log_level = os.environ.get('LOG_LEVEL', 'INFO')

logging.basicConfig(
    level=log_level,
    format='%(asctime)s : %(levelname)s : %(message)s',
    stream=sys.stdout
)


class OpenBibDataRelease:

    def __init__(self,
                 export_directory: str,
                 export_file_name: str,
                 host: str,
                 database: str,
                 port: str,
                 user: str,
                 password: str,
                 overwrite_snapshot: bool=True):

        self.export_directory = export_directory
        self.export_file_name = export_file_name
        self.host = host
        self.database = database
        self.port = port
        self.user = user
        self.password = password

        self.engine = create_engine(f'postgresql://{self.user}:{self.password}@{self.host}:{self.port}/{self.database}')

        if overwrite_snapshot:

            if Path(self.export_directory).exists() and Path(self.export_directory).is_dir():
                shutil.rmtree(self.export_directory)

            os.makedirs(self.export_directory, exist_ok=False)

            if Path(self.export_file_name).exists() and Path(self.export_file_name).is_file():
                os.remove(self.export_file_name)

        else:
            os.makedirs(self.export_directory, exist_ok=True)

    @staticmethod
    def export_to_jsonl(export_directory: str, export_file_name: str, dataframe: pd.DataFrame) -> None:

        logging.info('Start exporting: JSONL')

        with open(f'{export_directory}/{export_file_name}', 'w') as f:
            result = [json.dumps(record, ensure_ascii=False) for record in
                      dataframe.to_dict(orient='records')]
            for line in result:
                f.write(line + '\n')

        logging.info('Finish exporting: JSONL')

    @staticmethod
    def export_to_csv(export_directory: str, export_file_name: str, dataframe: pd.DataFrame) -> None:

        logging.info('Start exporting: CSV')

        normalized_publishers_export = pd.json_normalize(
            dataframe.to_dict(orient='records'))
        normalized_publishers_export.to_csv(
            path_or_buf=os.path.join(export_directory,
                                     export_file_name), index=False)

        logging.info('Finish exporting: CSV')

    def export_publishers(self, limit: str | int='NULL', export_format: str='csv') -> None:

        logging.info('Query table: add_publishers_20250711')

        publishers_export = pd.read_sql(sql=
                                           f"""
                                           SELECT publisher_id, 
                                                  CASE
                                                    WHEN publisher_id_orig != '' THEN CONCAT('https://openalex.org/', publisher_id_orig)
                                                    ELSE NULL
                                                  END AS publisher_id_orig, 
                                                  publisher_name,
                                                  standard_name, 
                                                  unit_pk, 
                                                  CASE 
                                                    WHEN wikidata != '' THEN CONCAT('https://wikidata.org/wiki/', wikidata)
                                                    ELSE NULL
                                                  END AS wikidata,
                                                  CASE 
                                                    WHEN ror != '' THEN CONCAT('https://ror.org/', ror)
                                                    ELSE NULL
                                                  END AS ror,
                                                  url
                                           FROM kb_project_openbib.add_publishers_20250711
                                           LIMIT {limit}
                                           """,
                                           con=self.engine)

        logging.info('Query completed.')

        publishers_export['publisher_id'] = publishers_export['publisher_id'].fillna('-1')
        publishers_export['publisher_id'] = publishers_export['publisher_id'].astype('int')

        publisher_schema.validate(publishers_export)

        if export_format == 'jsonl':

            OpenBibDataRelease.export_to_jsonl(export_directory=self.export_directory,
                                               export_file_name='publishers.jsonl',
                                               dataframe=publishers_export)

        if export_format == 'csv':

            OpenBibDataRelease.export_to_csv(export_directory=self.export_directory,
                                             export_file_name='publishers.csv',
                                             dataframe=publishers_export)

    def export_publishers_relations(self, limit: str | int='NULL', export_format: str='csv') -> None:

        logging.info('Query table: add_publishers_relations_20250711')

        publishers_relation_export = pd.read_sql(sql=
                                           f"""
                                           SELECT p_relation_id, 
                                                  child_name, 
                                                  CASE
                                                    WHEN child_id != '' THEN CONCAT('https://openalex.org/', child_id)
                                                    ELSE NULL
                                                  END AS child_id, 
                                                  child_unit, 
                                                  parent_name, 
                                                  CASE
                                                    WHEN parent_id != '' THEN CONCAT('https://openalex.org/', parent_id)
                                                    ELSE NULL
                                                  END AS parent_id, 
                                                  parent_unit, 
                                                  first_date, 
                                                  last_date
                                           FROM kb_project_openbib.add_publishers_relations_20250711
                                           LIMIT {limit}
                                           """,
                                           con=self.engine)

        logging.info('Query completed.')

        publishers_relation_export['child_unit'] = publishers_relation_export['child_unit'].fillna('0')
        publishers_relation_export['child_unit'] = publishers_relation_export['child_unit'].astype('int')

        publishers_relation_export['first_date'] = publishers_relation_export['first_date'].fillna('')
        publishers_relation_export['first_date'] = publishers_relation_export['first_date'].astype('str')

        publishers_relation_export['last_date'] = publishers_relation_export['last_date'].fillna('')
        publishers_relation_export['last_date'] = publishers_relation_export['last_date'].astype('str')

        publisher_relation_schema.validate(publishers_relation_export)

        if export_format == 'jsonl':

            OpenBibDataRelease.export_to_jsonl(export_directory=self.export_directory,
                                               export_file_name='publishers_relation.jsonl',
                                               dataframe=publishers_relation_export)

        if export_format == 'csv':

            OpenBibDataRelease.export_to_csv(export_directory=self.export_directory,
                                             export_file_name='publishers_relation.csv',
                                             dataframe=publishers_relation_export)

    def export_funding_information(self, limit: str | int='NULL', export_format: str='csv') -> None:

        logging.info('Query table: add_funding_information_20251211')

        funding_information_export = pd.read_sql(sql=
                                                 f"""
                                                 SELECT 
                                                    CASE
                                                        WHEN item_id_oal IS NOT NULL THEN CONCAT('https://openalex.org/', item_id_oal)
                                                        ELSE NULL
                                                    END AS openalex_id, 
                                                    doi, 
                                                    funding_id
                                                 FROM kb_project_openbib.add_funding_information_20251211
                                                 LIMIT {limit}
                                                 """,
                                                 con=self.engine)

        logging.info('Query completed.')

        funding_information_schema_nested.validate(funding_information_export)

        if export_format == 'jsonl':

            OpenBibDataRelease.export_to_jsonl(export_directory=self.export_directory,
                                               export_file_name='funding_information.jsonl',
                                               dataframe=funding_information_export)

        if export_format == 'csv':

            logging.info('Start exporting: CSV')

            normalized_funding_information_export = pd.json_normalize(
                funding_information_export.to_dict(orient='records'),
                record_path='funding_id',
                meta=['doi', 'openalex_id'])
            normalized_funding_information_export.columns = ['funding_id',
                                                             'doi',
                                                             'openalex_id']
            normalized_funding_information_export = normalized_funding_information_export[['openalex_id',
                                                                                           'doi',
                                                                                           'funding_id']]
            normalized_funding_information_export.to_csv(path_or_buf=os.path.join(
                self.export_directory, 'funding_information.csv'), index=False)

            logging.info('Finish exporting: CSV')

    def export_document_types(self, limit: str | int='NULL', export_format: str='csv') -> None:

        logging.info('Query table: add_document_types_20250711')

        document_type_export = pd.read_sql(sql=
                                           f"""
                                           SELECT 
                                            CASE
                                                WHEN openalex_id IS NOT NULL THEN CONCAT('https://openalex.org/', openalex_id)
                                                ELSE NULL
                                            END AS openalex_id, 
                                            dt.doi, 
                                            is_research, 
                                            proba
                                           FROM kb_project_openbib.add_document_types_20250711 AS dt 
                                           JOIN oal_rep_20250711.works AS oal
                                                ON dt.openalex_id = oal.id
                                           WHERE oal.publication_year BETWEEN 2014 AND 2025
                                           LIMIT {limit}
                                           """,
                                           con=self.engine)

        logging.info('Query completed.')

        document_type_schema.validate(document_type_export)

        if export_format == 'jsonl':

            OpenBibDataRelease.export_to_jsonl(export_directory=self.export_directory,
                                               export_file_name='document_types.jsonl',
                                               dataframe=document_type_export)

        if export_format == 'csv':

            OpenBibDataRelease.export_to_csv(export_directory=self.export_directory,
                                             export_file_name='document_types.csv',
                                             dataframe=document_type_export)

    def export_address_information_a(self, limit: str | int='NULL', export_format: str='csv') -> None:

        logging.info('Query table: add_institution_kb_a_oal_b_20250711')

        kb_a_addr_inst_export = pd.read_sql(sql=
                                            f"""
                                            SELECT inst_id_top, 
                                                   CASE
                                                    WHEN item_id IS NOT NULL THEN CONCAT('https://openalex.org/', item_id)
                                                    ELSE NULL
                                                   END AS openalex_id,
                                                   address_full, 
                                                   sector_id, 
                                                   doi,
                                                   identifier
                                            FROM kb_project_openbib.add_institution_kb_a_oal_b_20250711
                                            LIMIT {limit}
                                            """,
                                            con=self.engine)

        logging.info('Query completed.')

        kb_a_addr_inst_sec_schema_nested.validate(kb_a_addr_inst_export)

        if export_format == 'jsonl':

            OpenBibDataRelease.export_to_jsonl(export_directory=self.export_directory,
                                               export_file_name='kb_a_addr_inst.jsonl',
                                               dataframe=kb_a_addr_inst_export)

        if export_format == 'csv':

            logging.info('Start exporting: CSV')

            normalized_kb_a_addr_inst_export = pd.json_normalize(
                kb_a_addr_inst_export.to_dict(orient='records'),
                record_path='sector_id',
                meta=['inst_id_top', 'openalex_id', 'address_full', 'doi', 'identifier'])
            normalized_kb_a_addr_inst_export.columns = ['sector_id',
                                                        'inst_id_top',
                                                        'openalex_id',
                                                        'address_full',
                                                        'doi',
                                                        'identifier']
            normalized_kb_a_addr_inst_export = normalized_kb_a_addr_inst_export[['inst_id_top',
                                                                                 'openalex_id',
                                                                                 'address_full',
                                                                                 'sector_id',
                                                                                 'doi',
                                                                                 'identifier']]

            normalized_kb_a_addr_inst_export.to_csv(path_or_buf=os.path.join(
                self.export_directory, 'kb_a_addr_inst.csv'), index=False)

            logging.info('Finish exporting: CSV')

    def export_address_information_s(self, limit: str | int='NULL', export_format: str='csv') -> None:

        logging.info('Query table: add_institution_kb_s_oal_b_20250711')

        kb_s_addr_inst_export = pd.read_sql(sql=
                                            f"""
                                            SELECT inst_id_top,
                                                   CASE
                                                    WHEN item_id IS NOT NULL THEN CONCAT('https://openalex.org/', item_id)
                                                    ELSE NULL
                                                   END AS openalex_id,
                                                   address_full, 
                                                   sector_id, 
                                                   doi,
                                                   identifier
                                            FROM kb_project_openbib.add_institution_kb_s_oal_b_20250711
                                            LIMIT {limit}
                                            """,
                                            con=self.engine)

        logging.info('Query completed.')

        kb_s_addr_inst_sec_schema_nested.validate(kb_s_addr_inst_export)

        if export_format == 'jsonl':

            OpenBibDataRelease.export_to_jsonl(export_directory=self.export_directory,
                                               export_file_name='kb_s_addr_inst.jsonl',
                                               dataframe=kb_s_addr_inst_export)

        if export_format == 'csv':

            logging.info('Start exporting: CSV')

            normalized_kb_s_addr_inst_export = pd.json_normalize(
                kb_s_addr_inst_export.to_dict(orient='records'),
                record_path='sector_id',
                meta=['inst_id_top', 'openalex_id', 'address_full', 'doi', 'identifier'])
            normalized_kb_s_addr_inst_export.columns = ['sector_id',
                                                        'inst_id_top',
                                                        'openalex_id',
                                                        'address_full',
                                                        'doi',
                                                        'identifier']
            normalized_kb_s_addr_inst_export = normalized_kb_s_addr_inst_export[['inst_id_top',
                                                                                 'openalex_id',
                                                                                 'address_full',
                                                                                 'sector_id',
                                                                                 'doi',
                                                                                 'identifier']]

            normalized_kb_s_addr_inst_export.to_csv(path_or_buf=os.path.join(
                self.export_directory, 'kb_s_addr_inst.csv'), index=False)

            logging.info('Finish exporting: CSV')

    def export_kb_inst_name_lookup(self, limit: str | int='NULL', export_format: str='csv') -> None:

        logging.info('Query table: add_institution_lookup_kb_oal_b_20250711')

        kb_inst_name_lookup_export = pd.read_sql(sql=
                                        f"""
                                        SELECT inst_id,
                                               name
                                        FROM kb_project_openbib.add_institution_lookup_kb_oal_b_20250711
                                        LIMIT {limit}
                                        """,
                                        con=self.engine)

        logging.info('Query completed.')

        kb_inst_name_lookup_schema.validate(kb_inst_name_lookup_export)

        if export_format == 'jsonl':

            OpenBibDataRelease.export_to_jsonl(export_directory=self.export_directory,
                                               export_file_name='kb_inst_name_lookup.jsonl',
                                               dataframe=kb_inst_name_lookup_export)

        if export_format == 'csv':
            OpenBibDataRelease.export_to_csv(export_directory=self.export_directory,
                                             export_file_name='kb_inst_name_lookup.csv',
                                             dataframe=kb_inst_name_lookup_export)

    def export_kb_sector_name_lookup(self, limit: str | int='NULL', export_format: str='csv') -> None:

        logging.info('Query table: add_sector_lookup_kb_oal_b_20250711')

        kb_sector_name_lookup_export = pd.read_sql(sql=
                                        f"""
                                        SELECT sector_id,
                                               name
                                        FROM kb_project_openbib.add_sector_lookup_kb_oal_b_20250711
                                        LIMIT {limit}
                                        """,
                                        con=self.engine)

        logging.info('Query completed.')

        kb_sector_name_lookup_schema.validate(kb_sector_name_lookup_export)

        if export_format == 'jsonl':

            OpenBibDataRelease.export_to_jsonl(export_directory=self.export_directory,
                                               export_file_name='kb_sector_name_lookup.jsonl',
                                               dataframe=kb_sector_name_lookup_export)

        if export_format == 'csv':
            OpenBibDataRelease.export_to_csv(export_directory=self.export_directory,
                                             export_file_name='kb_sector_name_lookup.csv',
                                             dataframe=kb_sector_name_lookup_export)

    def export_kb_sector_lookup(self, limit: str | int='NULL', export_format: str='csv') -> None:

        logging.info('Query table: add_sector_lookup_kb_suppl_oal_b_20250711')

        kb_sector_lookup_export = pd.read_sql(sql=
                                        f"""
                                        SELECT sector_id,
                                               sectorgroup_id,
                                               sectorgroup_name,
                                               remarks
                                        FROM kb_project_openbib.add_sector_lookup_kb_suppl_oal_b_20250711
                                        LIMIT {limit}
                                        """,
                                        con=self.engine)

        logging.info('Query completed.')

        kb_sector_lookup_schema.validate(kb_sector_lookup_export)

        if export_format == 'jsonl':

            OpenBibDataRelease.export_to_jsonl(export_directory=self.export_directory,
                                               export_file_name='kb_sector_lookup.jsonl',
                                               dataframe=kb_sector_lookup_export)

        if export_format == 'csv':
            OpenBibDataRelease.export_to_csv(export_directory=self.export_directory,
                                             export_file_name='kb_sector_lookup.csv',
                                             dataframe=kb_sector_lookup_export)

    def export_kb_inst_lookup(self, limit: str | int='NULL', export_format: str='csv') -> None:

        logging.info('Query table: add_institution_lookup_kb_suppl_oal_b_20250711')

        kb_inst_lookup_export = pd.read_sql(sql=
                                        f"""
                                        SELECT inst_id,
                                               first_year,
                                               last_year,
                                               CASE 
                                                WHEN ror = '' THEN NULL
                                                ELSE ror
                                               END AS ror,
                                               dfg_instituts_id,
                                               current_sectors
                                        FROM kb_project_openbib.add_institution_lookup_kb_suppl_oal_b_20250711
                                        LIMIT {limit}
                                        """,
                                        con=self.engine)

        logging.info('Query completed.')

        kb_inst_lookup_export['dfg_instituts_id'] = kb_inst_lookup_export['dfg_instituts_id'].fillna('0')

        kb_inst_lookup_export['dfg_instituts_id'] = kb_inst_lookup_export['dfg_instituts_id'].astype('int')

        kb_inst_lookup_export['first_year'] = kb_inst_lookup_export['first_year'].astype('int')

        kb_inst_lookup_export['last_year'] = kb_inst_lookup_export['last_year'].astype('int')

        kb_inst_lookup_schema_nested.validate(kb_inst_lookup_export)

        if export_format == 'jsonl':

            OpenBibDataRelease.export_to_jsonl(export_directory=self.export_directory,
                                               export_file_name='kb_inst_lookup.jsonl',
                                               dataframe=kb_inst_lookup_export)

        if export_format == 'csv':

            logging.info('Start exporting: CSV')

            normalized_kb_inst_lookup_export = pd.json_normalize(
                kb_inst_lookup_export.to_dict(orient='records'),
                record_path='current_sectors',
                meta=['inst_id', 'first_year', 'last_year', 'ror', 'dfg_instituts_id'])
            normalized_kb_inst_lookup_export.columns = ['current_sectors',
                                                        'inst_id',
                                                        'first_year',
                                                        'last_year',
                                                        'ror',
                                                        'dfg_instituts_id']

            normalized_kb_inst_lookup_export = normalized_kb_inst_lookup_export[['inst_id',
                                                                                 'first_year',
                                                                                 'last_year',
                                                                                 'ror',
                                                                                 'dfg_instituts_id',
                                                                                 'current_sectors']]

            normalized_kb_inst_lookup_export.to_csv(path_or_buf=os.path.join(
                self.export_directory, 'kb_inst_lookup.csv'), index=False)

            logging.info('Finish exporting: CSV')

    def export_jct_articles(self, limit: str | int='NULL', export_format: str='csv') -> None:

        logging.info('Query table: add_jct_articles_20250711')

        jct_articles_export = pd.read_sql(sql=
                                        f"""
                                        SELECT 
                                            CASE
                                                WHEN id IS NOT NULL THEN CONCAT('https://openalex.org/', id)
                                                ELSE NULL
                                            END AS id, 
                                            doi, 
                                            matching_issn_l, 
                                            matching_ror, 
                                            ror_type, 
                                            esac_id, 
                                            start_date, 
                                            end_date, 
                                            publication_date
                                        FROM kb_project_openbib.add_jct_articles_20250711
                                        LIMIT {limit}
                                        """,
                                        con=self.engine)

        logging.info('Query completed.')

        jct_articles_export['start_date'] = jct_articles_export['start_date'].astype('str')
        jct_articles_export['end_date'] = jct_articles_export['end_date'].astype('str')
        jct_articles_export['publication_date'] = jct_articles_export['publication_date'].astype('str')

        jct_articles_schema.validate(jct_articles_export)

        if export_format == 'jsonl':

            OpenBibDataRelease.export_to_jsonl(export_directory=self.export_directory,
                                               export_file_name='jct_articles.jsonl',
                                               dataframe=jct_articles_export)

        if export_format == 'csv':
            OpenBibDataRelease.export_to_csv(export_directory=self.export_directory,
                                             export_file_name='jct_articles.csv',
                                             dataframe=jct_articles_export)

    def export_jct_esac(self, limit: str | int='NULL', export_format: str='csv') -> None:

        logging.info('Query table: add_jct_esac')

        jct_esac_export = pd.read_sql(sql=
                                        f"""
                                        SELECT publisher, 
                                               country, 
                                               organization, 
                                               annual_publications, 
                                               start_date, 
                                               end_date, 
                                               id, 
                                               url, 
                                               jct_jn, 
                                               jct_inst
                                        FROM kb_project_openbib.add_jct_esac
                                        LIMIT {limit}
                                        """,
                                        con=self.engine)

        logging.info('Query completed.')

        jct_esac_schema.validate(jct_esac_export)

        if export_format == 'jsonl':

            OpenBibDataRelease.export_to_jsonl(export_directory=self.export_directory,
                                               export_file_name='jct_esac.jsonl',
                                               dataframe=jct_esac_export)

        if export_format == 'csv':
            OpenBibDataRelease.export_to_csv(export_directory=self.export_directory,
                                             export_file_name='jct_esac.csv',
                                             dataframe=jct_esac_export)

    def export_jct_institutions(self, limit: str | int='NULL', export_format: str='csv') -> None:

        logging.info('Query table: add_jct_institutions')

        jct_institutions_export = pd.read_sql(sql=
                                                f"""
                                                SELECT 
                                                    esac_id, 
                                                    inst_name,
                                                    ror_id, 
                                                    time_last_seen, 
                                                    commit_hash
                                                FROM kb_project_openbib.add_jct_institutions
                                                LIMIT {limit}
                                                """,
                                                con=self.engine)

        logging.info('Query completed.')

        jct_institutions_schema.validate(jct_institutions_export)

        if export_format == 'jsonl':

            OpenBibDataRelease.export_to_jsonl(export_directory=self.export_directory,
                                               export_file_name='jct_institutions.jsonl',
                                               dataframe=jct_institutions_export)

        if export_format == 'csv':
            OpenBibDataRelease.export_to_csv(export_directory=self.export_directory,
                                             export_file_name='jct_institutions.csv',
                                             dataframe=jct_institutions_export)

    def export_jct_journals(self, limit: str | int='NULL', export_format: str='csv') -> None:

        logging.info('Query table: add_jct_journals')

        jct_journals_export = pd.read_sql(sql=
                                            f"""
                                            SELECT 
                                                esac_id, 
                                                issn_l, 
                                                time_last_seen, 
                                                commit_hash
                                            FROM kb_project_openbib.add_jct_journals
                                            LIMIT {limit}
                                            """,
                                            con=self.engine)

        logging.info('Query completed.')

        jct_journals_schema.validate(jct_journals_export)

        if export_format == 'jsonl':

            OpenBibDataRelease.export_to_jsonl(export_directory=self.export_directory,
                                               export_file_name='jct_journals.jsonl',
                                               dataframe=jct_journals_export)

        if export_format == 'csv':
            OpenBibDataRelease.export_to_csv(export_directory=self.export_directory,
                                             export_file_name='jct_journals.csv',
                                             dataframe=jct_journals_export)

    def make_archive(self, limit: str | int='NULL', export_format: str='csv') -> None:

        self.export_publishers(limit=limit, export_format=export_format)
        self.export_publishers_relations(limit=limit, export_format=export_format)
        self.export_funding_information(limit=limit, export_format=export_format)
        self.export_document_types(limit=limit, export_format=export_format)
        self.export_address_information_a(limit=limit, export_format=export_format)
        self.export_address_information_s(limit=limit, export_format=export_format)
        self.export_kb_inst_lookup(limit=limit, export_format=export_format)
        self.export_kb_inst_name_lookup(limit=limit, export_format=export_format)
        self.export_kb_sector_lookup(limit=limit, export_format=export_format)
        self.export_kb_sector_name_lookup(limit=limit, export_format=export_format)
        self.export_jct_articles(limit=limit, export_format=export_format)
        self.export_jct_esac(limit=limit, export_format=export_format)
        self.export_jct_institutions(limit=limit, export_format=export_format)
        self.export_jct_journals(limit=limit, export_format=export_format)

        logging.info('Start compressing archive.')

        shutil.make_archive(base_name=self.export_file_name,
                            format='zip',
                            root_dir=self.export_directory)

        logging.info('Finish compressing archive.')

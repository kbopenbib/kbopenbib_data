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
                                        kb_a_inst_sec_schema,
                                        kb_s_inst_sec_schema,
                                        kb_sectors_schema,
                                        kb_inst_schema,
                                        kb_inst_trans_schema)
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

        if Path(self.export_directory).exists() and Path(self.export_directory).is_dir():
            shutil.rmtree(self.export_directory)

        os.makedirs(self.export_directory, exist_ok=False)

        if overwrite_snapshot:
            if Path(self.export_file_name).exists() and Path(self.export_file_name).is_file():
                os.remove(self.export_file_name)

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

        logging.info('Query table: add_publishers_20240831')

        publishers_export = pd.read_sql(sql=
                                           f"""
                                           SELECT publisher_id, 
                                                  CASE
                                                    WHEN publisher_id_orig IS NOT NULL THEN CONCAT('https://openalex.org/', publisher_id_orig)
                                                    ELSE NULL
                                                  END AS publisher_id_orig, 
                                                  publisher_name,
                                                  standard_name, 
                                                  unit_pk, 
                                                  CASE 
                                                    WHEN wikidata IS NOT NULL THEN CONCAT('https://wikidata.org/wiki/', wikidata)
                                                    ELSE NULL
                                                  END AS wikidata,
                                                  CASE 
                                                    WHEN ror IS NOT NULL THEN CONCAT('https://ror.org/', ror)
                                                    ELSE NULL
                                                  END AS ror,
                                                  url
                                           FROM kb_project_openbib.add_publishers_20240831
                                           LIMIT {limit}
                                           """,
                                           con=self.engine)

        logging.info('Query completed.')

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

        logging.info('Query table: add_publishers_relations_20240831')

        publishers_relation_export = pd.read_sql(sql=
                                           f"""
                                           SELECT p_relation_id, 
                                                  child_name, 
                                                  CASE
                                                    WHEN child_id IS NOT NULL THEN CONCAT('https://openalex.org/', child_id)
                                                    ELSE NULL
                                                  END AS child_id, 
                                                  child_unit, 
                                                  parent_name, 
                                                  CASE
                                                    WHEN parent_id IS NOT NULL THEN CONCAT('https://openalex.org/', parent_id)
                                                    ELSE NULL
                                                  END AS parent_id, 
                                                  parent_unit, 
                                                  first_date, 
                                                  last_date
                                           FROM kb_project_openbib.add_publishers_relations_20240831
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

        logging.info('Query table: add_funding_information_20240831')

        funding_information_export = pd.read_sql(sql=
                                                 f"""
                                                 SELECT 
                                                    CASE
                                                        WHEN item_id_oal IS NOT NULL THEN CONCAT('https://openalex.org/', item_id_oal)
                                                        ELSE NULL
                                                    END AS openalex_id, 
                                                    doi, 
                                                    funding_id
                                                 FROM kb_project_openbib.add_funding_information_20240831
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

        logging.info('Query table: add_document_types_20240831')

        document_type_export = pd.read_sql(sql=
                                           f"""
                                           SELECT 
                                            CASE
                                                WHEN openalex_id IS NOT NULL THEN CONCAT('https://openalex.org/', openalex_id)
                                                ELSE NULL
                                            END AS openalex_id, 
                                            doi, 
                                            is_research, 
                                            proba
                                           FROM kb_project_openbib.add_document_types_20240831
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

        logging.info('Query table: add_address_information_a_addr_inst_sec_20240831')

        kb_a_addr_inst_export = pd.read_sql(sql=
                                            f"""
                                            SELECT kb_inst_id, 
                                                   CASE
                                                    WHEN item_id IS NOT NULL THEN CONCAT('https://openalex.org/', item_id)
                                                    ELSE NULL
                                                   END AS openalex_id,
                                                   address_full, 
                                                   kb_sector_id, 
                                                   doi,
                                                   identifier
                                            FROM kb_project_openbib.add_address_information_a_addr_inst_sec_20240831
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
                record_path='kb_sector_id',
                meta=['kb_inst_id', 'openalex_id', 'address_full', 'doi', 'identifier'])
            normalized_kb_a_addr_inst_export.columns = ['kb_sector_id',
                                                        'kb_inst_id',
                                                        'openalex_id',
                                                        'address_full',
                                                        'doi',
                                                        'identifier']
            normalized_kb_a_addr_inst_export = normalized_kb_a_addr_inst_export[['kb_inst_id',
                                                                                 'openalex_id',
                                                                                 'address_full',
                                                                                 'kb_sector_id',
                                                                                 'doi',
                                                                                 'identifier']]

            normalized_kb_a_addr_inst_export.to_csv(path_or_buf=os.path.join(
                self.export_directory, 'kb_a_addr_inst.csv'), index=False)

            logging.info('Finish exporting: CSV')

    def export_address_information_a_sec(self, limit: str | int='NULL', export_format: str='csv') -> None:

        logging.info('Query table: add_address_information_a_inst_sec_20240831')

        kb_a_inst_export = pd.read_sql(sql=
                                        f"""
                                        SELECT kb_inst_id,
                                               kb_sector_id
                                        FROM kb_project_openbib.add_address_information_a_inst_sec_20240831
                                        LIMIT {limit}
                                        """,
                                        con=self.engine)

        logging.info('Query completed.')

        kb_a_inst_sec_schema.validate(kb_a_inst_export)

        if export_format == 'jsonl':

            OpenBibDataRelease.export_to_jsonl(export_directory=self.export_directory,
                                               export_file_name='kb_a_inst.jsonl',
                                               dataframe=kb_a_inst_export)

        if export_format == 'csv':
            OpenBibDataRelease.export_to_csv(export_directory=self.export_directory,
                                             export_file_name='kb_a_inst.csv',
                                             dataframe=kb_a_inst_export)

    def export_address_information_s(self, limit: str | int='NULL', export_format: str='csv') -> None:

        logging.info('Query table: add_address_information_s_addr_inst_sec_20240831')

        kb_s_addr_inst_export = pd.read_sql(sql=
                                            f"""
                                            SELECT kb_inst_id,
                                                   CASE
                                                    WHEN item_id IS NOT NULL THEN CONCAT('https://openalex.org/', item_id)
                                                    ELSE NULL
                                                   END AS openalex_id,
                                                   address_full, 
                                                   kb_sector_id, 
                                                   doi,
                                                   identifier
                                            FROM kb_project_openbib.add_address_information_s_addr_inst_sec_20240831
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
                record_path='kb_sector_id',
                meta=['kb_inst_id', 'openalex_id', 'address_full', 'doi', 'identifier'])
            normalized_kb_s_addr_inst_export.columns = ['kb_sector_id',
                                                        'kb_inst_id',
                                                        'openalex_id',
                                                        'address_full',
                                                        'doi',
                                                        'identifier']
            normalized_kb_s_addr_inst_export = normalized_kb_s_addr_inst_export[['kb_inst_id',
                                                                                 'openalex_id',
                                                                                 'address_full',
                                                                                 'kb_sector_id',
                                                                                 'doi',
                                                                                 'identifier']]

            normalized_kb_s_addr_inst_export.to_csv(path_or_buf=os.path.join(
                self.export_directory, 'kb_s_addr_inst.csv'), index=False)

            logging.info('Finish exporting: CSV')

    def export_address_information_s_sec(self, limit: str | int='NULL', export_format: str='csv') -> None:

        logging.info('Query table: add_address_information_s_inst_sec_20240831')

        kb_s_inst_export = pd.read_sql(sql=
                                        f"""
                                        SELECT kb_inst_id,
                                               kb_sector_id,
                                               first_year,
                                               last_year
                                        FROM kb_project_openbib.add_address_information_s_inst_sec_20240831
                                        LIMIT {limit}
                                        """,
                                        con=self.engine)

        logging.info('Query completed.')

        kb_s_inst_sec_schema.validate(kb_s_inst_export)

        if export_format == 'jsonl':

            OpenBibDataRelease.export_to_jsonl(export_directory=self.export_directory,
                                               export_file_name='kb_s_inst.jsonl',
                                               dataframe=kb_s_inst_export)

        if export_format == 'csv':
            OpenBibDataRelease.export_to_csv(export_directory=self.export_directory,
                                             export_file_name='kb_s_inst.csv',
                                             dataframe=kb_s_inst_export)

    def export_kb_sectors(self, limit: str | int='NULL', export_format: str='csv') -> None:

        logging.info('Query table: add_address_information_sectors_20240831')

        kb_sectors_export = pd.read_sql(sql=
                                        f"""
                                        SELECT kb_sectorgroup_id,
                                               kb_sector_id,
                                               sectorgroup_name,
                                               sector_name,
                                               remarks
                                        FROM kb_project_openbib.add_address_information_sectors_20240831
                                        LIMIT {limit}
                                        """,
                                        con=self.engine)

        logging.info('Query completed.')

        kb_sectors_schema.validate(kb_sectors_export)

        if export_format == 'jsonl':

            OpenBibDataRelease.export_to_jsonl(export_directory=self.export_directory,
                                               export_file_name='kb_sectors.jsonl',
                                               dataframe=kb_sectors_export)

        if export_format == 'csv':
            OpenBibDataRelease.export_to_csv(export_directory=self.export_directory,
                                             export_file_name='kb_sectors.csv',
                                             dataframe=kb_sectors_export)

    def export_kb_inst(self, limit: str | int='NULL', export_format: str='csv') -> None:

        logging.info('Query table: add_address_information_inst_20240831')

        kb_inst_export = pd.read_sql(sql=
                                        f"""
                                        SELECT kb_inst_id,
                                               name,
                                               first_year,
                                               last_year,
                                               CASE 
                                                WHEN ror = '' THEN NULL
                                                ELSE ror
                                               END AS ror,
                                               dfg_instituts_id
                                        FROM kb_project_openbib.add_address_information_inst_20240831
                                        LIMIT {limit}
                                        """,
                                        con=self.engine)

        logging.info('Query completed.')

        kb_inst_export['dfg_instituts_id'] = kb_inst_export['dfg_instituts_id'].fillna('0')

        kb_inst_export['dfg_instituts_id'] = kb_inst_export['dfg_instituts_id'].astype('int')

        kb_inst_schema.validate(kb_inst_export)

        if export_format == 'jsonl':

            OpenBibDataRelease.export_to_jsonl(export_directory=self.export_directory,
                                               export_file_name='kb_inst.jsonl',
                                               dataframe=kb_inst_export)

        if export_format == 'csv':
            OpenBibDataRelease.export_to_csv(export_directory=self.export_directory,
                                             export_file_name='kb_inst.csv',
                                             dataframe=kb_inst_export)

    def export_kb_inst_trans(self, limit: str | int='NULL', export_format: str='csv') -> None:

        logging.info('Query table: add_address_information_inst_trans_20240831')

        kb_inst_trans_export = pd.read_sql(sql=
                                            f"""
                                            SELECT inst_ante, 
                                                   transition_date, 
                                                   inst_post, 
                                                   type
                                            FROM kb_project_openbib.add_address_information_inst_trans_20240831
                                            LIMIT {limit}
                                            """,
                                            con=self.engine)

        logging.info('Query completed.')

        kb_inst_trans_schema.validate(kb_inst_trans_export)

        if export_format == 'jsonl':

            OpenBibDataRelease.export_to_jsonl(export_directory=self.export_directory,
                                               export_file_name='kb_inst_trans.jsonl',
                                               dataframe=kb_inst_trans_export)

        if export_format == 'csv':
            OpenBibDataRelease.export_to_csv(export_directory=self.export_directory,
                                             export_file_name='kb_inst_trans.csv',
                                             dataframe=kb_inst_trans_export)

    def make_archive(self, limit: str | int='NULL', export_format: str='csv') -> None:

        self.export_publishers(limit=limit, export_format=export_format)
        self.export_publishers_relations(limit=limit, export_format=export_format)
        self.export_funding_information(limit=limit, export_format=export_format)
        self.export_document_types(limit=limit, export_format=export_format)
        self.export_address_information_a(limit=limit, export_format=export_format)
        self.export_address_information_a_sec(limit=limit, export_format=export_format)
        self.export_address_information_s(limit=limit, export_format=export_format)
        self.export_address_information_s_sec(limit=limit, export_format=export_format)
        self.export_kb_sectors(limit=limit, export_format=export_format)
        self.export_kb_inst(limit=limit, export_format=export_format)
        self.export_kb_inst_trans(limit=limit, export_format=export_format)

        logging.info('Start compressing archive.')

        shutil.make_archive(base_name=self.export_file_name,
                            format='zip',
                            root_dir=self.export_directory)

        logging.info('Finish compressing archive.')

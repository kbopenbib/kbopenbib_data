import os
import pandas as pd
import json
from sqlalchemy import create_engine
import shutil
from pathlib import Path
from models.document_type import document_type_schema
from models.funding_information import funding_information_schema_nested
from models.publisher import publisher_schema
from models.address_information import kb_a_addr_inst_sec_open_alex_schema_nested
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
                 overwrite_snapshot=True):

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

    def export_publishers(self, limit='NULL', export_format='csv'):

        logging.info('Query table: kb_publisher_standard_relation')

        publishers_export = pd.read_sql(sql=
                                           f"""
                                           SELECT publisher_id, publisher_id_orig, publisher_name,
                                                  standard_name, unit_pk, other_name, wikidata, ror, url, 
                                                  parent_name, parent_id, parent_unit
                                           FROM kb_project_openbib.kb_publisher_standard_relation
                                           LIMIT {limit}
                                           """,
                                           con=self.engine)

        logging.info('Query completed.')

        publisher_schema.validate(publishers_export)

        if export_format == 'jsonl':

            logging.info('Start exporting: JSONL')

            with open(f'{self.export_directory}/publishers.jsonl', 'w') as f:
                result = [json.dumps(record, ensure_ascii=False) for record in
                          publishers_export.to_dict(orient='records')]
                for line in result:
                    f.write(line + '\n')

            logging.info('Finish exporting: JSONL')

        if export_format == 'csv':

            logging.info('Start exporting: CSV')

            normalized_publishers_export = pd.json_normalize(
                publishers_export.to_dict(orient='records'))
            normalized_publishers_export.to_csv(
                path_or_buf=os.path.join(self.export_directory,
                                         'publishers.csv'), index=False)

            logging.info('Finish exporting: CSV')

    def export_funding_information(self, limit='NULL', export_format='csv'):

        logging.info('Query table: dfg_oa')

        funding_information_export = pd.read_sql(sql=
                                                 f"""
                                                 SELECT item_id_oal as openalex_id, doi, funding_id
                                                 FROM kb_project_openbib.dfg_oa
                                                 LIMIT {limit}
                                                 """,
                                                 con=self.engine)

        logging.info('Query completed.')

        funding_information_schema_nested.validate(funding_information_export)

        if export_format == 'jsonl':

            logging.info('Start exporting: JSONL')

            with open(f'{self.export_directory}/funding_information.jsonl', 'w') as f:
                result = [json.dumps(record, ensure_ascii=False) for record in
                          funding_information_export.to_dict(orient='records')]
                for line in result:
                    f.write(line + '\n')

            logging.info('Finish exporting: JSONL')

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

    def export_document_types(self, limit='NULL', export_format='csv'):

        logging.info('Query table: classification_article_reviews_2014_2024_august24')

        document_type_export = pd.read_sql(sql=
                                           f"""
                                           SELECT openalex_id, doi, is_research, proba
                                           FROM kb_project_openbib.classification_article_reviews_2014_2024_august24
                                           LIMIT {limit}
                                           """,
                                           con=self.engine)

        logging.info('Query completed.')

        document_type_schema.validate(document_type_export)

        if export_format == 'jsonl':

            logging.info('Start exporting: JSONL')

            with open(f'{self.export_directory}/document_types.jsonl', 'w') as f:
                result = [json.dumps(record, ensure_ascii=False) for record in
                          document_type_export.to_dict(orient='records')]
                for line in result:
                    f.write(line + '\n')

            logging.info('Finish exporting: JSONL')

        if export_format == 'csv':

            logging.info('Start exporting: CSV')

            normalized_document_type_export = pd.json_normalize(
                document_type_export.to_dict(orient='records'))
            normalized_document_type_export.to_csv(
                path_or_buf=os.path.join(self.export_directory,
                                         'document_types.csv'), index=False)

            logging.info('Finish exporting: CSV')

    def export_address_information(self, limit='NULL', export_format='csv'):

        logging.info('Query table: kb_a_addr_inst_sec_oa_b_20240831')

        kb_a_addr_inst_export = pd.read_sql(sql=
                                            f"""
                                            SELECT kb_inst_id, 
                                                   item_id as openalex_id, 
                                                   address_full, 
                                                   kb_sector_id, 
                                                   doi,
                                                   identifier
                                            FROM kb_project_openbib.kb_a_addr_inst_sec_oa_b_20240831
                                            LIMIT {limit}
                                            """,
                                            con=self.engine)

        logging.info('Query completed.')

        kb_a_addr_inst_sec_open_alex_schema_nested.validate(kb_a_addr_inst_export)

        if export_format == 'jsonl':

            logging.info('Start exporting: JSONL')

            with open(f'{self.export_directory}/kb_a_addr_inst.jsonl', 'w') as f:
                result = [json.dumps(record, ensure_ascii=False) for record in
                          kb_a_addr_inst_export.to_dict(orient='records')]
                for line in result:
                    f.write(line + '\n')

            logging.info('Finish exporting: JSONL')

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

    def make_archive(self, limit='NULL', export_format='csv'):

        self.export_publishers(limit=limit, export_format=export_format)
        self.export_funding_information(limit=limit, export_format=export_format)
        self.export_document_types(limit=limit, export_format=export_format)

        logging.info('Start compressing archive.')

        shutil.make_archive(base_name=self.export_file_name,
                            format='zip',
                            root_dir=self.export_directory)

        logging.info('Finish compressing archive.')

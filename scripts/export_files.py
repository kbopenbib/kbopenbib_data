import os
import pandas as pd
import json
from sqlalchemy import create_engine
import shutil
from pathlib import Path


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

    def export_funding_information(self, limit='NULL', export_format='csv'):

        funding_information_export = pd.read_sql(sql=
                                                 f"""
                                                 SELECT *
                                                 FROM kb_project_openbib.dfg_oa
                                                 LIMIT {limit}
                                                 """,
                                                 con=self.engine)

        if export_format == 'jsonl':

            with open(f'{self.export_directory}/funding_information.jsonl', 'w') as f:
                result = [json.dumps(record, ensure_ascii=False) for record in
                          funding_information_export.to_dict(orient='records')]
                for line in result:
                    f.write(line + '\n')

        if export_format == 'csv':

            normalized_funding_information_export = pd.json_normalize(
                funding_information_export.to_dict(orient='records'),
                record_path='funding_id',
                meta=['doi', 'item_id_oal'])
            normalized_funding_information_export.columns = ['funding_id',
                                                             'doi',
                                                             'item_id_oal']
            normalized_funding_information_export = normalized_funding_information_export[['doi',
                                                                                           'funding_id',
                                                                                           'item_id_oal']]
            normalized_funding_information_export.to_csv(path_or_buf=os.path.join(
                self.export_directory, 'funding_information.csv'), index=False)

    def export_document_types(self, limit='NULL', export_format='csv'):

        document_type_export = pd.read_sql(sql=
                                           f"""
                                           SELECT *
                                           FROM kb_project_openbib.classification_article_reviews_2014_2024_december24
                                           LIMIT {limit}
                                           """,
                                           con=self.engine)

        if export_format == 'jsonl':

            with open(f'{self.export_directory}/document_types.jsonl', 'w') as f:
                result = [json.dumps(record, ensure_ascii=False) for record in
                          document_type_export.to_dict(orient='records')]
                for line in result:
                    f.write(line + '\n')

        if export_format == 'csv':
            normalized_document_type_export = pd.json_normalize(
                document_type_export.to_dict(orient='records'))
            normalized_document_type_export.to_csv(
                path_or_buf=os.path.join(self.export_directory,
                                         'document_types.csv'), index=False)

    def make_archive(self):

        shutil.make_archive(base_name=self.export_file_name,
                            format='zip',
                            root_dir=self.export_directory)

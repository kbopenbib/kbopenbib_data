import os
import pandas as pd
import json
from sqlalchemy import create_engine
import shutil
from pathlib import Path
from dotenv import load_dotenv



class OpenBibDataRelease:

    def __init__(self,
                 export_directory: str,
                 export_file_name: str,
                 env_file: str):

        self.export_directory = export_directory
        self.export_file_name = export_file_name
        self.env_file = env_file


        dotenv_path = Path(self.env_file)
        load_dotenv(dotenv_path=dotenv_path)

        host = os.environ['KB_HOST']
        database = os.environ['KB_DATABASE']
        user = os.environ['KB_USER']
        pw = os.environ['KB_PASSWORD']
        port = os.environ['KB_PORT']
        self.engine = create_engine(f'postgresql://{user}:{pw}@{host}:{port}/{database}')


        if Path(self.export_directory).exists() and Path(self.export_directory).is_dir():
                shutil.rmtree(self.export_directory)

        os.makedirs(self.export_directory, exist_ok=False)

        if Path(self.export_file_name).exists() and Path(self.export_file_name).is_file():
                os.remove(self.export_file_name)

    def export(self, limit='NULL'):

        document_type_export = pd.read_sql(
                             f"""
                                  SELECT *
                                  FROM kb_project_openbib.classification_article_reviews_2014_2024_december24
                                  LIMIT {limit}
                                  """,
                                  con=self.engine)


        with open(f'{self.export_directory}/document_types.jsonl', 'w') as f:
            result = [json.dumps(record, ensure_ascii=False) for record in document_type_export.to_dict(orient='records')]
            for line in result:
                f.write(line + '\n')

        funding_information_export = pd.read_sql(
                                        f"""
                                            SELECT *
                                            FROM kb_project_openbib.dfg_oa
                                            LIMIT {limit}
                                            """,
                                            con=self.engine)

        with open(f'{self.export_directory}/funding_information.jsonl', 'w') as f:
            result = [json.dumps(record, ensure_ascii=False) for record in funding_information_export.to_dict(orient='records')]
            for line in result:
                f.write(line + '\n')


        shutil.make_archive(self.export_file_name,'zip',self.export_directory)

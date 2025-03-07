import pytest
import os
import shutil
import pandas as pd
from dotenv import load_dotenv
from pathlib import Path
import zipfile
from scripts.export_files import OpenBibDataRelease
from models.document_type import document_type_schema
from models.funding_information import funding_information_schema_unnested
from models.publisher import publisher_schema
from models.address_information import kb_a_addr_inst_sec_open_alex_schema_unnested


class TestOpenBibDataRelease:

    test_dir = os.path.abspath(os.path.dirname(__file__))

    dotenv_path = Path('./../.env')
    load_dotenv(dotenv_path=dotenv_path)

    host = os.environ['KB_HOST']
    database = os.environ['KB_DATABASE']
    user = os.environ['KB_USER']
    password = os.environ['KB_PASSWORD']
    port = os.environ['KB_PORT']

    @pytest.fixture
    def openbib_snapshot(self):
        snapshot = OpenBibDataRelease(
            export_directory=os.path.join(self.test_dir, 'openbib_export'),
            export_file_name='kbopenbib_release',
            host=self.host,
            database=self.database,
            port=self.port,
            user=self.user,
            password=self.password
        )
        yield snapshot
        shutil.rmtree(os.path.join(self.test_dir, 'openbib_export'))

    def test_export_publisher_information(self, openbib_snapshot):

        openbib_snapshot.export_publishers(limit=10, export_format='csv')

        assert os.path.exists(os.path.join(self.test_dir, 'openbib_export/publishers.csv'))

        publishers_export = pd.read_csv(
            filepath_or_buffer=os.path.join(self.test_dir, 'openbib_export/publishers.csv'),
            sep=',',
            quotechar='"',
            header=0
        )

        publisher_schema.validate(publishers_export)

    def test_export_funding_information(self, openbib_snapshot):

        openbib_snapshot.export_funding_information(limit=10, export_format='csv')

        assert os.path.exists(os.path.join(self.test_dir, 'openbib_export/funding_information.csv'))

        funding_information_export = pd.read_csv(
            filepath_or_buffer=os.path.join(self.test_dir, 'openbib_export/funding_information.csv'),
            sep=',',
            quotechar='"',
            header=0
        )

        funding_information_schema_unnested.validate(funding_information_export)

    def test_export_document_types(self, openbib_snapshot):

        openbib_snapshot.export_document_types(limit=10, export_format='csv')

        assert os.path.exists(os.path.join(self.test_dir, 'openbib_export/document_types.csv'))

        document_type_export = pd.read_csv(
            filepath_or_buffer=os.path.join(self.test_dir, 'openbib_export/document_types.csv'),
            sep=',',
            quotechar='"',
            header=0
        )

        document_type_schema.validate(document_type_export)

    def test_export_address_information(self, openbib_snapshot):

        openbib_snapshot.export_address_information(limit=10, export_format='csv')

        assert os.path.exists(os.path.join(self.test_dir, 'openbib_export/kb_a_addr_inst.csv'))

        kb_a_addr_inst_sec_open_alex_export = pd.read_csv(
            filepath_or_buffer=os.path.join(self.test_dir, 'openbib_export/kb_a_addr_inst.csv'),
            sep=',',
            quotechar='"',
            header=0
        )

        kb_a_addr_inst_sec_open_alex_schema_unnested.validate(kb_a_addr_inst_sec_open_alex_export)

    def test_make_archive(self, openbib_snapshot):

        openbib_snapshot.make_archive(limit=10, export_format='csv')

        assert os.path.exists(os.path.join(self.test_dir, 'kbopenbib_release.zip'))

        archive = zipfile.ZipFile(file=os.path.join(self.test_dir, 'kbopenbib_release.zip'), mode='r')

        assert len(archive.infolist()) == 3

        os.remove(os.path.join(self.test_dir, 'kbopenbib_release.zip'))
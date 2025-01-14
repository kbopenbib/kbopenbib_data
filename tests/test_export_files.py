import pytest
import os
import shutil
from scripts.export_files import OpenBibDataRelease


class TestOpenBibDataRelease:

    test_dir = os.path.abspath(os.path.dirname(__file__))

    @pytest.fixture
    def openbib_snapshot(self):
        snapshot = OpenBibDataRelease(
            export_directory=os.path.join(self.test_dir, 'openbib_export'),
            export_file_name='kbopenbib_release',
            env_file=os.path.join('./../.env'),
        )
        yield snapshot
        shutil.rmtree(os.path.join(self.test_dir, 'openbib_export'))

    def test_export_funding_information(self, openbib_snapshot):

        openbib_snapshot.export_funding_information(limit=10, export_format='csv')

        assert os.path.exists(os.path.join(self.test_dir, 'openbib_export/funding_information.csv'))

    def test_export_document_types(self, openbib_snapshot):

        openbib_snapshot.export_document_types(limit=10, export_format='csv')

        assert os.path.exists(os.path.join(self.test_dir, 'openbib_export/document_types.csv'))

    def test_make_archive(self, openbib_snapshot):

        openbib_snapshot.export_funding_information(limit=10, export_format='csv')
        openbib_snapshot.export_document_types(limit=10, export_format='csv')

        openbib_snapshot.make_archive()

        assert os.path.exists(os.path.join(self.test_dir, 'kbopenbib_release.zip'))

        os.remove(os.path.join(self.test_dir, 'kbopenbib_release.zip'))
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
        os.remove(os.path.join(self.test_dir, 'kbopenbib_release.zip'))

    def test_export(self, openbib_snapshot):

        openbib_snapshot.export(limit=10)

        assert os.path.exists(os.path.join(self.test_dir, 'kbopenbib_release.zip'))
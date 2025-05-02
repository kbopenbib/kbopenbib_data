import pytest
import os
import shutil
import pandas as pd
from dotenv import load_dotenv
import zipfile
from scripts.export_files import OpenBibDataRelease
from models.document_type import document_type_schema
from models.funding_information import funding_information_schema_unnested
from models.publisher import publisher_schema, publisher_relation_schema
from models.address_information import (kb_a_addr_inst_sec_schema_unnested,
                                        kb_a_addr_inst_sec_schema_nested,
                                        kb_s_addr_inst_sec_schema_unnested,
                                        kb_s_addr_inst_sec_schema_nested,
                                        kb_a_inst_sec_schema,
                                        kb_s_inst_sec_schema,
                                        kb_sectors_schema,
                                        kb_inst_schema,
                                        kb_inst_trans_schema)
from models.transformative_agreements import (jct_institutions_schema,
                                              jct_journals_schema,
                                              jct_articles_schema,
                                              jct_esac_schema)


class TestOpenBibDataRelease:

    test_dir = os.path.abspath(os.path.dirname(__file__))

    dotenv_path = os.path.join(test_dir, '.env')
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
            export_file_name=os.path.join(self.test_dir, 'kbopenbib_release'),
            host=self.host,
            database=self.database,
            port=self.port,
            user=self.user,
            password=self.password,
            overwrite_snapshot=True
        )
        yield snapshot
        shutil.rmtree(os.path.join(self.test_dir, 'openbib_export'))

    def test_export_publisher_information_to_csv(self, openbib_snapshot: OpenBibDataRelease) -> None:

        openbib_snapshot.export_publishers(limit=10, export_format='csv')

        assert os.path.exists(os.path.join(self.test_dir, 'openbib_export/publishers.csv.gz'))

        publishers_export = pd.read_csv(
            filepath_or_buffer=os.path.join(self.test_dir, 'openbib_export/publishers.csv.gz'),
            compression='gzip',
            sep=',',
            quotechar='"',
            header=0
        )

        publisher_schema.validate(publishers_export)

    def test_export_publisher_information_to_jsonl(self, openbib_snapshot: OpenBibDataRelease) -> None:

        openbib_snapshot.export_publishers(limit=10, export_format='jsonl')

        assert os.path.exists(os.path.join(self.test_dir, 'openbib_export/publishers.jsonl.gz'))

        publishers_export = pd.read_json(path_or_buf=os.path.join(self.test_dir,
                                                                  'openbib_export/publishers.jsonl.gz'),
                                         compression='gzip',
                                         lines=True)

        publisher_schema.validate(publishers_export)

    def test_export_publisher_relation_information_to_csv(self, openbib_snapshot: OpenBibDataRelease) -> None:

        openbib_snapshot.export_publishers_relations(limit=10, export_format='csv')

        assert os.path.exists(os.path.join(self.test_dir, 'openbib_export/publishers_relation.csv.gz'))

        publishers_export = pd.read_csv(
            filepath_or_buffer=os.path.join(self.test_dir, 'openbib_export/publishers_relation.csv.gz'),
            compression='gzip',
            sep=',',
            quotechar='"',
            header=0
        )

        publisher_relation_schema.validate(publishers_export)

    def test_export_publisher_relation_information_to_jsonl(self, openbib_snapshot: OpenBibDataRelease) -> None:

        openbib_snapshot.export_publishers_relations(limit=10, export_format='jsonl')

        assert os.path.exists(os.path.join(self.test_dir, 'openbib_export/publishers_relation.jsonl.gz'))

        publishers_export = pd.read_json(path_or_buf=os.path.join(self.test_dir,
                                                                  'openbib_export/publishers_relation.jsonl.gz'),
                                         compression='gzip',
                                         lines=True)

        publisher_relation_schema.validate(publishers_export)

    def test_export_funding_information_to_csv(self, openbib_snapshot: OpenBibDataRelease) -> None:

        openbib_snapshot.export_funding_information(limit=10, export_format='csv')

        assert os.path.exists(os.path.join(self.test_dir, 'openbib_export/funding_information.csv.gz'))

        funding_information_export = pd.read_csv(
            filepath_or_buffer=os.path.join(self.test_dir, 'openbib_export/funding_information.csv.gz'),
            compression='gzip',
            sep=',',
            quotechar='"',
            header=0
        )

        funding_information_schema_unnested.validate(funding_information_export)

    def test_export_funding_information_to_jsonl(self, openbib_snapshot: OpenBibDataRelease) -> None:

        openbib_snapshot.export_funding_information(limit=10, export_format='jsonl')

        assert os.path.exists(os.path.join(self.test_dir, 'openbib_export/funding_information.jsonl.gz'))

        funding_information_export = pd.read_json(path_or_buf=os.path.join(self.test_dir,
                                                                        'openbib_export/funding_information.jsonl.gz'),
                                                  compression='gzip',
                                                  lines=True)

        funding_information_schema_unnested.validate(funding_information_export)

    def test_export_document_types_to_csv(self, openbib_snapshot: OpenBibDataRelease) -> None:

        openbib_snapshot.export_document_types(limit=10, export_format='csv')

        assert os.path.exists(os.path.join(self.test_dir, 'openbib_export/document_types.csv.gz'))

        document_type_export = pd.read_csv(
            filepath_or_buffer=os.path.join(self.test_dir, 'openbib_export/document_types.csv.gz'),
            compression='gzip',
            sep=',',
            quotechar='"',
            header=0
        )

        document_type_schema.validate(document_type_export)

    def test_export_document_types_to_jsonl(self, openbib_snapshot: OpenBibDataRelease) -> None:

        openbib_snapshot.export_document_types(limit=10, export_format='jsonl')

        assert os.path.exists(os.path.join(self.test_dir, 'openbib_export/document_types.jsonl.gz'))

        document_type_export = pd.read_json(path_or_buf=os.path.join(self.test_dir,
                                                                     'openbib_export/document_types.jsonl.gz'),
                                            compression='gzip',
                                            lines=True)

        document_type_schema.validate(document_type_export)

    def test_export_address_information_a_to_csv(self, openbib_snapshot: OpenBibDataRelease) -> None:

        openbib_snapshot.export_address_information_a(limit=10, export_format='csv')

        assert os.path.exists(os.path.join(self.test_dir, 'openbib_export/kb_a_addr_inst.csv.gz'))

        kb_a_addr_inst_sec_export = pd.read_csv(
            filepath_or_buffer=os.path.join(self.test_dir, 'openbib_export/kb_a_addr_inst.csv.gz'),
            compression='gzip',
            sep=',',
            quotechar='"',
            header=0
        )

        kb_a_addr_inst_sec_schema_unnested.validate(kb_a_addr_inst_sec_export)

    def test_export_address_information_a_to_jsonl(self, openbib_snapshot: OpenBibDataRelease) -> None:

        openbib_snapshot.export_address_information_a(limit=10, export_format='jsonl')

        assert os.path.exists(os.path.join(self.test_dir, 'openbib_export/kb_a_addr_inst.jsonl.gz'))

        kb_a_addr_inst_sec_export = pd.read_json(path_or_buf=os.path.join(self.test_dir,
                                                                          'openbib_export/kb_a_addr_inst.jsonl.gz'),
                                                 compression='gzip',
                                                 lines=True)

        kb_a_addr_inst_sec_schema_nested.validate(kb_a_addr_inst_sec_export)

    def test_export_address_information_a_sec_to_csv(self, openbib_snapshot: OpenBibDataRelease) -> None:

        openbib_snapshot.export_address_information_a_sec(limit=10, export_format='csv')

        assert os.path.exists(os.path.join(self.test_dir, 'openbib_export/kb_a_inst.csv.gz'))

        kb_a_inst_sec_export = pd.read_csv(
            filepath_or_buffer=os.path.join(self.test_dir, 'openbib_export/kb_a_inst.csv.gz'),
            compression='gzip',
            sep=',',
            quotechar='"',
            header=0
        )

        kb_a_inst_sec_schema.validate(kb_a_inst_sec_export)

    def test_export_address_information_a_sec_to_jsonl(self, openbib_snapshot: OpenBibDataRelease) -> None:

        openbib_snapshot.export_address_information_a_sec(limit=10, export_format='jsonl')

        assert os.path.exists(os.path.join(self.test_dir, 'openbib_export/kb_a_inst.jsonl.gz'))

        kb_a_inst_sec_export = pd.read_json(path_or_buf=os.path.join(self.test_dir,
                                                                     'openbib_export/kb_a_inst.jsonl.gz'),
                                            compression='gzip',
                                            lines=True)

        kb_a_inst_sec_schema.validate(kb_a_inst_sec_export)

    def test_export_address_information_s_to_csv(self, openbib_snapshot: OpenBibDataRelease) -> None:

        openbib_snapshot.export_address_information_s(limit=10, export_format='csv')

        assert os.path.exists(os.path.join(self.test_dir, 'openbib_export/kb_s_addr_inst.csv.gz'))

        kb_s_addr_inst_sec_open_alex_export = pd.read_csv(
            filepath_or_buffer=os.path.join(self.test_dir, 'openbib_export/kb_s_addr_inst.csv.gz'),
            compression='gzip',
            sep=',',
            quotechar='"',
            header=0
        )

        kb_s_addr_inst_sec_schema_unnested.validate(kb_s_addr_inst_sec_open_alex_export)

    def test_export_address_information_s_to_jsonl(self, openbib_snapshot: OpenBibDataRelease) -> None:

        openbib_snapshot.export_address_information_s(limit=10, export_format='jsonl')

        assert os.path.exists(os.path.join(self.test_dir, 'openbib_export/kb_s_addr_inst.jsonl.gz'))

        kb_s_addr_inst_sec_open_alex_export = pd.read_json(path_or_buf=os.path.join(self.test_dir,
                                                                            'openbib_export/kb_s_addr_inst.jsonl.gz'),
                                                           compression='gzip',
                                                           lines=True)

        kb_s_addr_inst_sec_schema_nested.validate(kb_s_addr_inst_sec_open_alex_export)

    def test_export_address_information_s_sec_to_csv(self, openbib_snapshot: OpenBibDataRelease) -> None:

        openbib_snapshot.export_address_information_s_sec(limit=10, export_format='csv')

        assert os.path.exists(os.path.join(self.test_dir, 'openbib_export/kb_s_inst.csv.gz'))

        kb_s_inst_sec_export = pd.read_csv(
            filepath_or_buffer=os.path.join(self.test_dir, 'openbib_export/kb_s_inst.csv.gz'),
            compression='gzip',
            sep=',',
            quotechar='"',
            header=0
        )

        kb_s_inst_sec_schema.validate(kb_s_inst_sec_export)

    def test_export_address_information_s_sec_to_jsonl(self, openbib_snapshot: OpenBibDataRelease) -> None:

        openbib_snapshot.export_address_information_s_sec(limit=10, export_format='jsonl')

        assert os.path.exists(os.path.join(self.test_dir, 'openbib_export/kb_s_inst.jsonl.gz'))

        kb_s_inst_sec_export = pd.read_json(path_or_buf=os.path.join(self.test_dir,
                                                                     'openbib_export/kb_s_inst.jsonl.gz'),
                                            compression='gzip',
                                            lines=True)

        kb_s_inst_sec_schema.validate(kb_s_inst_sec_export)

    def test_export_sectors_to_csv(self, openbib_snapshot: OpenBibDataRelease) -> None:

        openbib_snapshot.export_kb_sectors(limit=10, export_format='csv')

        assert os.path.exists(os.path.join(self.test_dir, 'openbib_export/kb_sectors.csv.gz'))

        kb_sectors_export = pd.read_csv(
            filepath_or_buffer=os.path.join(self.test_dir, 'openbib_export/kb_sectors.csv.gz'),
            compression='gzip',
            sep=',',
            quotechar='"',
            header=0
        )

        kb_sectors_schema.validate(kb_sectors_export)

    def test_export_kb_sectors_to_jsonl(self, openbib_snapshot: OpenBibDataRelease) -> None:

        openbib_snapshot.export_kb_sectors(limit=10, export_format='jsonl')

        assert os.path.exists(os.path.join(self.test_dir, 'openbib_export/kb_sectors.jsonl.gz'))

        kb_sectors_export = pd.read_json(path_or_buf=os.path.join(self.test_dir,
                                                                  'openbib_export/kb_sectors.jsonl.gz'),
                                         compression='gzip',
                                         lines=True)

        kb_sectors_schema.validate(kb_sectors_export)

    def test_export_kb_inst_to_csv(self, openbib_snapshot: OpenBibDataRelease) -> None:

        openbib_snapshot.export_kb_inst(limit=10, export_format='csv')

        assert os.path.exists(os.path.join(self.test_dir, 'openbib_export/kb_inst.csv.gz'))

        kb_inst_export = pd.read_csv(
            filepath_or_buffer=os.path.join(self.test_dir, 'openbib_export/kb_inst.csv.gz'),
            compression='gzip',
            sep=',',
            quotechar='"',
            header=0
        )

        kb_inst_schema.validate(kb_inst_export)

    def test_export_kb_inst_to_jsonl(self, openbib_snapshot: OpenBibDataRelease) -> None:

        openbib_snapshot.export_kb_inst(limit=10, export_format='jsonl')

        assert os.path.exists(os.path.join(self.test_dir, 'openbib_export/kb_inst.jsonl.gz'))

        kb_inst_export = pd.read_json(path_or_buf=os.path.join(self.test_dir,
                                                               'openbib_export/kb_inst.jsonl.gz'),
                                      compression='gzip',
                                      lines=True)

        kb_inst_schema.validate(kb_inst_export)

    def test_export_kb_inst_trans_to_csv(self, openbib_snapshot: OpenBibDataRelease) -> None:

        openbib_snapshot.export_kb_inst_trans(limit=10, export_format='csv')

        assert os.path.exists(os.path.join(self.test_dir, 'openbib_export/kb_inst_trans.csv.gz'))

        kb_inst_trans_export = pd.read_csv(
            filepath_or_buffer=os.path.join(self.test_dir, 'openbib_export/kb_inst_trans.csv.gz'),
            compression='gzip',
            sep=',',
            quotechar='"',
            header=0
        )

        kb_inst_trans_schema.validate(kb_inst_trans_export)

    def test_export_kb_inst_trans_to_jsonl(self, openbib_snapshot: OpenBibDataRelease) -> None:

        openbib_snapshot.export_kb_inst_trans(limit=10, export_format='jsonl')

        assert os.path.exists(os.path.join(self.test_dir, 'openbib_export/kb_inst_trans.jsonl.gz'))

        kb_inst_trans_export = pd.read_json(path_or_buf=os.path.join(self.test_dir,
                                                                     'openbib_export/kb_inst_trans.jsonl.gz'),
                                            compression='gzip',
                                            lines=True)

        kb_inst_trans_schema.validate(kb_inst_trans_export)

    def test_export_jct_articles_to_csv(self, openbib_snapshot: OpenBibDataRelease) -> None:

        openbib_snapshot.export_jct_articles(limit=10, export_format='csv')

        assert os.path.exists(os.path.join(self.test_dir, 'openbib_export/jct_articles.csv.gz'))

        jct_articles_export = pd.read_csv(
            filepath_or_buffer=os.path.join(self.test_dir, 'openbib_export/jct_articles.csv.gz'),
            compression='gzip',
            sep=',',
            quotechar='"',
            header=0
        )

        jct_articles_schema.validate(jct_articles_export)

    def test_export_jct_articles_to_jsonl(self, openbib_snapshot: OpenBibDataRelease) -> None:

        openbib_snapshot.export_jct_articles(limit=10, export_format='jsonl')

        assert os.path.exists(os.path.join(self.test_dir, 'openbib_export/jct_articles.jsonl.gz'))

        jct_articles_export = pd.read_json(path_or_buf=os.path.join(self.test_dir,
                                                                'openbib_export/jct_articles.jsonl.gz'),
                                           compression='gzip',
                                           lines=True)

        jct_articles_schema.validate(jct_articles_export)

    def test_export_jct_esac_to_csv(self, openbib_snapshot: OpenBibDataRelease) -> None:

        openbib_snapshot.export_jct_esac(limit=10, export_format='csv')

        assert os.path.exists(os.path.join(self.test_dir, 'openbib_export/jct_esac.csv.gz'))

        jct_esac_export = pd.read_csv(
            filepath_or_buffer=os.path.join(self.test_dir, 'openbib_export/jct_esac.csv.gz'),
            compression='gzip',
            sep=',',
            quotechar='"',
            header=0
        )

        jct_esac_schema.validate(jct_esac_export)

    def test_export_jct_esac_to_jsonl(self, openbib_snapshot: OpenBibDataRelease) -> None:

        openbib_snapshot.export_jct_esac(limit=10, export_format='jsonl')

        assert os.path.exists(os.path.join(self.test_dir, 'openbib_export/jct_esac.jsonl.gz'))

        jct_esac_export = pd.read_json(path_or_buf=os.path.join(self.test_dir,
                                                                'openbib_export/jct_esac.jsonl.gz'),
                                       compression='gzip',
                                       lines=True)

        jct_esac_schema.validate(jct_esac_export)

    def test_export_jct_institutions_to_csv(self, openbib_snapshot: OpenBibDataRelease) -> None:

        openbib_snapshot.export_jct_institutions(limit=10, export_format='csv')

        assert os.path.exists(os.path.join(self.test_dir, 'openbib_export/jct_institutions.csv.gz'))

        jct_institutions_export = pd.read_csv(
            filepath_or_buffer=os.path.join(self.test_dir, 'openbib_export/jct_institutions.csv.gz'),
            compression='gzip',
            sep=',',
            quotechar='"',
            header=0
        )

        jct_institutions_schema.validate(jct_institutions_export)

    def test_export_jct_institutions_to_jsonl(self, openbib_snapshot: OpenBibDataRelease) -> None:

        openbib_snapshot.export_jct_institutions(limit=10, export_format='jsonl')

        assert os.path.exists(os.path.join(self.test_dir, 'openbib_export/jct_institutions.jsonl.gz'))

        jct_institutions_export = pd.read_json(path_or_buf=os.path.join(self.test_dir,
                                                                        'openbib_export/jct_institutions.jsonl.gz'),
                                               compression='gzip',
                                               lines=True)

        jct_institutions_schema.validate(jct_institutions_export)

    def test_export_jct_journals_to_csv(self, openbib_snapshot: OpenBibDataRelease) -> None:

        openbib_snapshot.export_jct_journals(limit=10, export_format='csv')

        assert os.path.exists(os.path.join(self.test_dir, 'openbib_export/jct_journals.csv.gz'))

        jct_journals_export = pd.read_csv(
            filepath_or_buffer=os.path.join(self.test_dir, 'openbib_export/jct_journals.csv.gz'),
            compression='gzip',
            sep=',',
            quotechar='"',
            header=0
        )

        jct_journals_schema.validate(jct_journals_export)

    def test_export_jct_journals_to_jsonl(self, openbib_snapshot: OpenBibDataRelease) -> None:

        openbib_snapshot.export_jct_journals(limit=10, export_format='jsonl')

        assert os.path.exists(os.path.join(self.test_dir, 'openbib_export/jct_journals.jsonl.gz'))

        jct_journals_export = pd.read_json(path_or_buf=os.path.join(self.test_dir,
                                                                    'openbib_export/jct_journals.jsonl.gz'),
                                           compression='gzip',
                                           lines=True)

        jct_journals_schema.validate(jct_journals_export)

    def test_make_archive_to_csv(self, openbib_snapshot: OpenBibDataRelease) -> None:

        openbib_snapshot.make_archive(limit=10, export_format='csv')

        assert os.path.exists(os.path.join(self.test_dir, 'kbopenbib_release.zip'))

        archive = zipfile.ZipFile(file=os.path.join(self.test_dir, 'kbopenbib_release.zip'), mode='r')

        assert len(archive.infolist()) == 15

        os.remove(os.path.join(self.test_dir, 'kbopenbib_release.zip'))

    def test_make_archive_to_jsonl(self, openbib_snapshot: OpenBibDataRelease) -> None:

        openbib_snapshot.make_archive(limit=10, export_format='jsonl')

        assert os.path.exists(os.path.join(self.test_dir, 'kbopenbib_release.zip'))

        archive = zipfile.ZipFile(file=os.path.join(self.test_dir, 'kbopenbib_release.zip'), mode='r')

        assert len(archive.infolist()) == 15

        os.remove(os.path.join(self.test_dir, 'kbopenbib_release.zip'))
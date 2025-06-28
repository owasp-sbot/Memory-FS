import pytest
from osbot_utils.utils.Env                                      import not_in_github_action
from osbot_utils.helpers.duration.decorators.capture_duration   import capture_duration
from osbot_utils.helpers.Safe_Id                                import Safe_Id
from tests.unit.Base_Test__File_FS                              import Base_Test__File_FS
from memory_fs.schemas.Schema__Memory_FS__File__Config          import Schema__Memory_FS__File__Config
from osbot_utils.utils.Objects                                  import __
from memory_fs.file_fs.File_FS                                  import File_FS


class test_File_FS(Base_Test__File_FS):                                                # Tests for File_FS class

    def test__init__(self):                                                             # Test File_FS initialization
        with self.file as _:
            assert type(_)         is File_FS
            assert type(_.config()) is Schema__Memory_FS__File__Config

            expected_obj = __(file_config = __(exists_strategy = 'FIRST'                  ,
                                               file_id         = _.file_config.file_id    ,
                                               file_paths      = []                       ,
                                               file_type       = __(name           = 'json'   ,
                                                                    content_type   = 'JSON'    ,
                                                                    file_extension = 'json'    ,
                                                                    encoding       = 'UTF_8'   ,
                                                                    serialization  = 'JSON'    )),
                              storage_fs   = __(content_data = __()           ))
            assert _.obj() == expected_obj

    def test_create(self):                                                              # Test file creation
        with self.file as _:
            assert _.exists() is False
            assert _.create() == [f"{_.file_id()}.json.config"]
            assert _.exists() is True

    def test_create__content(self):                                                     # Test content creation
        test_content = b'test data'

        with self.file as _:
            assert _.exists__content() is False
            assert _.create__content(test_content) == [f'{_.file_id()}.json']
            assert _.exists__content() is True

    def test_create__both(self):                                                        # Test creating both config and content
        test_data = "test string data"

        with self.file as _:
            files_created = _.create__both(test_data)
            assert sorted(files_created) == sorted([f'{_.file_id()}.json'        ,
                                                   f'{_.file_id()}.json.config' ])
            assert _.exists()          is True
            assert _.exists__content() is True

    def test_content(self):                                                             # Test raw content retrieval
        test_bytes = b'raw bytes'

        with self.file as _:
            _.create__content(test_bytes)
            assert _.content() != test_bytes
            assert _.content() == b'"raw bytes"'

    def test_data(self):                                                                # Test deserialized data retrieval
        test_dict = {"key": "value", "list": [1, 2, 3]}

        with self.file as _:
            _.save(test_dict)
            assert _.data() == test_dict

    def test_delete(self):                                                              # Test file deletion
        with self.file as _:
            _.create()
            assert _.exists() is True

            deleted_files = _.delete()
            assert deleted_files == [f'{_.file_id()}.json.config']
            assert _.exists()    is False

    def test_delete__content(self):                                                     # Test content deletion
        with self.file as _:
            _.create__content(b'content')
            assert _.exists__content() is True

            deleted_files = _.delete__content()
            assert deleted_files       == [f'{_.file_id()}.json']
            assert _.exists__content() is False

    def test_info(self):                                                                # Test file info
        with self.file as _:
            assert _.info() is None                                                     # No file yet

            _.create__both("test data")
            info = _.info()

            assert info is not None
            assert info[Safe_Id('exists'      )]       is True
            assert info[Safe_Id('content_type')] == 'application/json; charset=utf-8'

    def test_metadata(self):                                                            # Test metadata
        test_content = b'content for metadata'

        with self.file as _:
            _.create__content(test_content)
            metadata = _.metadata()

            assert metadata.content__hash is not None
            # Note: Known bug with content__size

    def test_save(self):                                                                # Test save method
        test_data = {"saved": "data"}

        with self.file as _:
            saved_files = _.save(test_data)
            assert saved_files == [f'{_.file_id()}.json']
            assert _.data()    == test_data


    def test__performance__create(self):
        if not_in_github_action:
            pytest.skip("Only run in GH actions (significant % of test execution)")
        items_to_create = 1000
        with capture_duration(precision=5) as duration:
            with self.file as _:
                for i in range(0, items_to_create):
                    _.create()

                    # full .create()           is ~0.01624      # the prob seems to be inside the self.file_fs__exists().config() method
                    # just .file_fs__create()  is ~0.00105

        #pprint(duration.seconds)
        #assert duration.seconds < 0.002                    # should be low like this
        assert duration.seconds < 0.03                      # but at the moment is big

    def test__performance__file_fs__exists__config(self):
        if not_in_github_action:
            pytest.skip("Only run in GH actions (significant % of test execution)")
        items_to_create = 1000
        file_fs_exists__config = self.file.file_fs__exists().config
        with capture_duration(precision=5) as duration:
            with self.file as _:
                for i in range(0, items_to_create):
                    file_fs_exists__config()                # still quite expensive

        #pprint(duration.seconds)
        #assert duration.seconds < 0.002                    # should be low like this
        assert duration.seconds < 0.03                      # but at the moment is big

    def test__performance__file_fs__create(self):
        if not_in_github_action:
            pytest.skip("Only run in GH actions (significant % of test execution)")
        items_to_create = 100
        with capture_duration(precision=4) as duration:
            with self.file as _:
                for i in range(0, items_to_create):
                    _.file_fs__create()
        assert duration.seconds < 0.001                                             # confirms the minium performance impact of @cache_on_self

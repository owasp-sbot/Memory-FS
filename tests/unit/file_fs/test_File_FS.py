import pytest
from osbot_utils.type_safe.primitives.domains.identifiers.safe_str.Safe_Str__Id import Safe_Str__Id
from memory_fs.schemas.Schema__Memory_FS__File__Metadata                        import Schema__Memory_FS__File__Metadata
from osbot_utils.utils.Env                                                      import not_in_github_action
from osbot_utils.helpers.duration.decorators.capture_duration                   import capture_duration
from tests.unit.Base_Test__File_FS                                              import Base_Test__File_FS
from memory_fs.schemas.Schema__Memory_FS__File__Config                          import Schema__Memory_FS__File__Config
from osbot_utils.utils.Objects                                                  import __
from memory_fs.file_fs.File_FS                                                  import File_FS


class test_File_FS(Base_Test__File_FS):                                                # Tests for File_FS class

    def test__init__(self):                                                             # Test File_FS initialization
        with self.file as _:
            assert type(_)         is File_FS
            assert type(_.config()) is Schema__Memory_FS__File__Config

            expected_obj = __(file__config = __(exists_strategy = 'first'                   ,
                                                file_id         = _.file__config.file_id    ,
                                                file_paths      = []                        ,
                                                file_type       = __(name           = 'json'   ,
                                                                     content_type   = 'application/json; charset=utf-8'    ,
                                                                     file_extension = 'json'    ,
                                                                     encoding       = 'utf-8'   ,
                                                                     serialization  = 'json'    )),
                              storage_fs   = __(content_data = __()           ))
            assert _.obj() == expected_obj

    def test_create(self):                                                              # Test file creation
        with self.file as _:
            assert _.exists()                     is False
            assert _.file_fs__config  ().exists() is False
            assert _.file_fs__content ().exists() is False
            assert _.file_fs__metadata().exists() is False

            assert _.create(self.default_content) == [f"{_.file_id()}.json"         ,
                                                      f"{_.file_id()}.json.config"  ,
                                                      f"{_.file_id()}.json.metadata"]

            assert _.exists()                     is True
            assert _.file_fs__config  ().exists() is True
            assert _.file_fs__content ().exists() is True
            assert _.file_fs__metadata().exists() is True

    def test_content(self):                                                             # Test raw content retrieval
        test_bytes = 'raw bytes'

        with self.file as _:
            _.update(test_bytes)
            assert _.content() == test_bytes

        test_dict = {"key": "value", "list": [1, 2, 3]}

        with self.file as _:
            _.update(test_dict)
            assert _.content() == test_dict

    def test_delete(self):                                                              # Test file deletion
        with self.file as _:
            _.create(file_data=self.default_content)
            assert _.exists() is True

            deleted_files = _.delete()
            assert deleted_files == [f'{_.file_id()}.json'         ,
                                     f'{_.file_id()}.json.config'  ,
                                     f'{_.file_id()}.json.metadata']
            assert _.exists()    is False

    def test_info(self):                                                                # Test file info
        with self.file as _:
            assert _.info() is None                                                     # No file yet

            _.create(self.default_content)
            info = _.info()

            assert info is not None
            assert info[Safe_Str__Id('exists'      )]       is True
            assert info[Safe_Str__Id('content_type')] == 'application/json; charset=utf-8'

    def test_metadata(self):                                                            # Test metadata
        test_content = 'content for metadata'

        with self.file as _:
            _.create(test_content)
            metadata = _.metadata()
            assert type(metadata) == Schema__Memory_FS__File__Metadata
            assert metadata.obj() == __(content__hash         ='58a28b6f67'       ,
                                        chain_hash            = None              ,
                                        data                  = __()              ,
                                        previous_version_path = None              ,
                                        content__size         = 22                ,
                                        tags                  = []                ,
                                        timestamp             = metadata.timestamp)

    def test_update(self):                                                                # Test save method
        test_data = {"saved": "data"}

        with self.file as _:
            saved_files = _.update(test_data)
            assert saved_files == [f'{_.file_id()}.json'         ,
                                   f'{_.file_id()}.json.metadata']
            assert _.content()    == test_data


    def test__performance__create(self):
        if not_in_github_action:
            pytest.skip("Only run in GH actions (significant % of test execution)")
        items_to_create = 1000
        with capture_duration(precision=5) as duration:
            with self.file as _:
                for i in range(0, items_to_create):
                    _.create()
        #pprint(duration.seconds)
        #assert duration.seconds < 0.002                    # should be low like this
        assert duration.seconds < 0.10                      # but at the moment is big

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

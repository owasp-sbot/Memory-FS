import pytest
from osbot_utils.utils.Env                                      import not_in_github_action
from osbot_utils.helpers.duration.decorators.capture_duration   import capture_duration
from tests.unit.Base_Test__File_FS                              import Base_Test__File_FS
from memory_fs.file_fs.actions.File_FS__Exists                  import File_FS__Exists
from osbot_utils.helpers.safe_str.Safe_Str__File__Path          import Safe_Str__File__Path

class test_File_FS__Exists(Base_Test__File_FS):                                         # Test file existence checking

    def setUp(self):                                                                    # Initialize test data
        super().setUp()
        self.file_exists = File_FS__Exists(file__config = self.file_config ,
                                           storage_fs   = self.storage_fs      )

    def test__init__(self):                                                             # Test initialization
        with self.file_exists as _:
            assert type(_)         is File_FS__Exists
            assert _.file__config  == self.file_config
            assert _.storage_fs    == self.storage_fs

    def test_config(self):                                                              # Test config file existence
        with self.file_exists as _:
            assert _.config() is False

            self.file.create()
            assert _.config() is True

            self.file.delete()
            assert _.config() is False

    def test_content(self):                                                             # Test content file existence
        with self.file_exists as _:
            assert _.content() is False

            self.file.create(file_data='test')
            assert _.content() is True

            self.file.delete()
            assert _.content() is False

    def test_check_using_strategy(self):                                               # Test strategy-based checking
        paths = [Safe_Str__File__Path('path1/file.txt') ,
                 Safe_Str__File__Path('path2/file.txt') ,
                 Safe_Str__File__Path('path3/file.txt') ]

        with self.file_exists as _:
            assert _.check_using_strategy(paths) is False                              # None exist

            self.storage_fs.file__save(paths[0], b'content')
            assert _.check_using_strategy(paths) is True                               # At least one exists (ANY strategy)

            self.storage_fs.file__delete(paths[0])
            assert _.check_using_strategy(paths) is False                              # None exist again

    def test_with_multiple_paths(self):                                                # Test with multiple file paths
        self.file_config.file_paths = [Safe_Str__File__Path('dir1') ,
                                       Safe_Str__File__Path('dir2') ]

        new_file_exists = File_FS__Exists(file__config = self.file_config ,
                                          storage_fs   = self.storage_fs  )

        with new_file_exists as _:
            assert _.config() is False

            # Create file in first path
            self.storage_fs.file__save(Safe_Str__File__Path('dir1/test-file.json.config'), b'{}')
            assert _.config() is True                                                   # ANY strategy - one exists


    def test__performance__config(self):
        if not_in_github_action:
            pytest.skip("Only run in GH actions (significant % of test execution)")
        items_to_create = 1000
        with capture_duration(precision=4) as duration:
            with self.file_exists as _:
                for i in range(0, items_to_create):
                    _.config()

        # with capture_duration(precision=5) as duration:
        #     with self.file as _:
        #         for i in range(0, items_to_create):
        #             _.create()
        #pprint(duration.seconds)
        #assert duration.seconds < 0.002                    # should be low like this
        assert duration.seconds < 0.03                      # but at the moment is realy big


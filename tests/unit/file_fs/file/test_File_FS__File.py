from osbot_utils.helpers.safe_str.Safe_Str__File__Path    import Safe_Str__File__Path
from tests.unit.Base_Test__File_FS                        import Base_Test__File_FS
from memory_fs.file_fs.file.File_FS__File                 import File_FS__File
from memory_fs.file_fs.actions.File_FS__Exists            import File_FS__Exists
from memory_fs.file_fs.actions.File_FS__Name              import File_FS__Name
from memory_fs.file_fs.actions.File_FS__Paths             import File_FS__Paths
from memory_fs.schemas.Schema__Memory_FS__File__Config    import Schema__Memory_FS__File__Config


class test_File_FS__File(Base_Test__File_FS):                                          # Test file file operations

    def setUp(self):                                                                    # Initialize test data
        super().setUp()
        self.file_fs_file = File_FS__File(file__config = self.file_config ,
                                           storage_fs   = self.storage_fs      )

    def test__init__(self):                                                             # Test initialization
        with self.file_fs_file as _:
            assert type(_)                  is File_FS__File
            assert type(_.file__config)     is Schema__Memory_FS__File__Config
            assert type(_.storage_fs)       is type(self.storage_fs)
            assert _.file__config           == self.file_config
            assert _.storage_fs             == self.storage_fs

    def test_file_fs__exists(self):                                                     # Test file_fs__exists cached method
        with self.file_fs_file as _:
            file_fs_exists_1 = _.file_fs__exists()
            file_fs_exists_2 = _.file_fs__exists()
            assert type(file_fs_exists_1) is File_FS__Exists
            assert file_fs_exists_1       is file_fs_exists_2                          # Verify caching works

    def test_file_fs__name(self):                                                       # Test file_fs__name cached method
        with self.file_fs_file as _:
            file_fs_name_1 = _.file_fs__name()
            file_fs_name_2 = _.file_fs__name()
            assert type(file_fs_name_1) is File_FS__Name
            assert file_fs_name_1       is file_fs_name_2                              # Verify caching works

    def test_file_fs__paths(self):                                                      # Test file_fs__paths cached method
        with self.file_fs_file as _:
            file_fs_paths_1 = _.file_fs__paths()
            file_fs_paths_2 = _.file_fs__paths()
            assert type(file_fs_paths_1) is File_FS__Paths
            assert file_fs_paths_1       is file_fs_paths_2                            # Verify caching works

    def test_delete(self):                                                              # Test delete method
        with self.file_fs_file as _:
            # Override paths method to return test paths
            test_paths = [Safe_Str__File__Path('test-file.json.config'),
                          Safe_Str__File__Path('test-file.json'       )]
            _.paths = lambda: test_paths

            # Create files to delete
            for path in test_paths:
                self.storage_fs.file__save(path=path, data=b'test content')

            # Verify files exist
            for path in test_paths:
                assert self.storage_fs.file__exists(path) is True

            # Delete files
            deleted_files = _.delete()
            assert deleted_files == test_paths

            # Verify files no longer exist
            for path in test_paths:
                assert self.storage_fs.file__exists(path) is False

    def test_delete_partial(self):                                                      # Test delete with partial success
        with self.file_fs_file as _:
            test_paths = [Safe_Str__File__Path('existing.json'    ),
                          Safe_Str__File__Path('non-existing.json')]
            _.paths = lambda: test_paths

            # Only create first file
            self.storage_fs.file__save(path=test_paths[0], data=b'test content')

            deleted_files = _.delete()
            assert deleted_files == [test_paths[0]]                                    # Only existing file deleted

    def test_data(self):                                                                # Test data method
        with self.file_fs_file as _:
            assert _.data() is None                                                     # Base implementation returns None

    def test_file_id(self):                                                             # Test file_id method
        with self.file_fs_file as _:
            assert _.file_id() == self.file_config.file_id

    def test_file_name(self):                                                           # Test file_name method
        with self.file_fs_file as _:
            expected_name = f'{self.file_config.file_id}.json.config'
            assert _.file_name() == expected_name

    def test_exists(self):                                                              # Test exists method
        with self.file_fs_file as _:
            assert _.exists() is False                                                  # Default should be False

    def test_not_exists(self):                                                          # Test not_exists method
        with self.file_fs_file as _:
            assert _.not_exists() is True                                               # Should be opposite of exists()

    def test_paths(self):                                                               # Test paths method
        with self.file_fs_file as _:
            assert _.paths() == []                                                      # Base implementation returns empty list

    def test_update(self):                                                              # Test update method
        with self.file_fs_file as _:
            test_paths = [Safe_Str__File__Path('file1.json'),
                          Safe_Str__File__Path('file2.json')]
            _.paths = lambda: test_paths

            test_data = b'updated content'
            updated_files = _.update(test_data)

            assert updated_files == test_paths

            # Verify content was saved
            for path in test_paths:
                assert self.storage_fs.file__bytes(path) == test_data

    def test_update_partial_failure(self):                                              # Test update with partial failure
        with self.file_fs_file as _:
            test_paths = [Safe_Str__File__Path('success.json'),
                          Safe_Str__File__Path('fail.json'   )]
            _.paths = lambda: test_paths

            # Mock storage to fail on second file
            original_save = self.storage_fs.file__save
            def mock_save(path, data):
                if path == test_paths[1]:
                    return False
                return original_save(path, data)

            self.storage_fs.file__save = mock_save

            test_data = b'test content'
            updated_files = _.update(test_data)

            assert updated_files == [test_paths[0]]                                    # Only successful save returned
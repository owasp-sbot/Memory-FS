from osbot_utils.utils.Json                                 import json_to_str
from tests.unit.Base_Test__File_FS                          import Base_Test__File_FS
from memory_fs.target_fs.Target_FS__Create                  import Target_FS__Create
from memory_fs.target_fs.Target_FS                          import Target_FS
from memory_fs.file_fs.File_FS                              import File_FS
from memory_fs.file_fs.actions.File_FS__Name                import FILE_EXTENSION__MEMORY_FS__FILE__CONFIG
from osbot_utils.helpers.safe_str.Safe_Str__File__Path      import Safe_Str__File__Path


class test_Target_FS__Create(Base_Test__File_FS):                                      # Test target FS create factory

    def setUp(self):                                                                    # Initialize test data
        super().setUp()
        self.target_fs_create = Target_FS__Create   (storage_fs=self.storage_fs)
        self.test_path        = Safe_Str__File__Path(f"{self.file_config.file_id}.json.{FILE_EXTENSION__MEMORY_FS__FILE__CONFIG}")

    def test__init__(self):                                                             # Test initialization
        with self.target_fs_create as _:
            assert type(_)    is Target_FS__Create
            assert _.storage_fs  == self.storage_fs

    def test_from_path__config_no_file(self):                                          # Test loading from path when file doesn't exist
        with self.target_fs_create as _:
            result = _.from_path__config(self.test_path)
            assert result is None

    def test_from_path__config_with_file(self):                                        # Test loading from path when file exists
        # Create and save a file
        self.file.create()

        with self.target_fs_create as _:
            target_fs = _.from_path__config(self.test_path)
            assert type(target_fs)               is Target_FS
            assert target_fs.file_config.file_id == self.file_config.file_id
            assert target_fs.storage_fs          == self.storage_fs

            # Verify we can use the loaded target_fs
            file_fs = target_fs.file_fs()
            assert type(file_fs) is File_FS
            assert file_fs.exists() is True

    def test_from_path__config_invalid_json(self):                                     # Test loading from path with invalid JSON
        # Save invalid JSON to the path
        self.storage_fs.file__save(self.test_path, b"invalid json")

        with self.target_fs_create as _:
            try:
                _.from_path__config(self.test_path)
                assert False, "Should raise exception for invalid JSON"
            except:
                pass                                                                    # Expected - TODO: should handle gracefully

    def test_from_path__config_different_paths(self):                                  # Test loading from different paths
        # Create files with different paths
        path1 = Safe_Str__File__Path("dir1/file.json.config")
        path2 = Safe_Str__File__Path("dir2/file.json.config")

        config1 = self.create_file_config(file_id="file1")
        config2 = self.create_file_config(file_id="file2")

        file_1_bytes = json_to_str(config1.json()).encode()
        file_2_bytes = json_to_str(config2.json()).encode()
        self.storage_fs.file__save(path1, file_1_bytes)
        self.storage_fs.file__save(path2, file_2_bytes)

        with self.target_fs_create as _:
            target_fs_1 = _.from_path__config(path1)
            target_fs_2 = _.from_path__config(path2)

            assert target_fs_1.file_config.file_id == "file1"
            assert target_fs_2.file_config.file_id == "file2"
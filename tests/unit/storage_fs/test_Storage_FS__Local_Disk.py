import re
import pytest
import tempfile
from json                                                                       import JSONDecodeError
from unittest                                                                   import TestCase
from osbot_utils.type_safe.primitives.domains.files.safe_str.Safe_Str__File__Path  import Safe_Str__File__Path
from osbot_utils.utils.Json                                                     import json_to_bytes
from osbot_utils.utils.Files                                                    import file_exists, folder_exists, folder_create, file_bytes, path_combine, folder_delete_all, parent_folder
from memory_fs.storage_fs.providers.Storage_FS__Local_Disk                      import Storage_FS__Local_Disk


class test_Storage_FS__Local_Disk(TestCase):                                           # Test local disk storage operations

    def setUp(self):                                                                    # Initialize test data
        self.temp_dir = tempfile.mkdtemp()
        self.storage  = Storage_FS__Local_Disk(root_path=self.temp_dir)

        # Test data
        self.test_path    = Safe_Str__File__Path("test/file.txt")
        self.test_content = b"test content"
        self.test_json    = {"key": "value", "number": 42}

    def tearDown(self):                                                                 # Clean up temp directory
        assert folder_delete_all(self.temp_dir) is True

    def test__init__(self):                                                             # Test initialization
        with self.storage as _:
            assert type(_)           is Storage_FS__Local_Disk
            assert type(_.root_path) is Safe_Str__File__Path
            assert folder_exists(str(_.root_path))

    def test__init__with_string_path(self):                                            # Test initialization with string path
        string_path = path_combine(self.temp_dir, "subfolder")
        storage     = Storage_FS__Local_Disk(root_path=string_path)

        assert type(storage.root_path) is Safe_Str__File__Path
        assert folder_exists(storage.root_path)      is False                           # folder should not exist until it is used
        assert str(storage.root_path) == string_path

    def test__full_path(self):                                                         # Test full path generation
        with self.storage as _:
            path      = Safe_Str__File__Path("folder/file.txt")
            full_path = _.full_path(path)

            assert type(full_path) is str
            assert full_path       == path_combine(str(_.root_path), "folder/file.txt")

    def test__ensure_parent_dirs(self):                                                # Test parent directory creation
        with self.storage as _:
            deep_path = _.full_path(Safe_Str__File__Path("a/b/c/d/file.txt"))
            parent_dir = path_combine(str(_.root_path), "a/b/c/d")

            assert folder_exists(parent_dir) is False
            _.ensure_parent_dirs(deep_path)
            assert folder_exists(parent_dir) is True

    def test_file__save(self):                                                         # Test file saving
        with self.storage as _:
            assert _.file__exists(self.test_path) is False
            assert _.file__save(self.test_path, self.test_content) is True
            assert _.file__exists(self.test_path) is True

            # Verify content
            saved_path = _.full_path(self.test_path)
            assert file_bytes(saved_path) == self.test_content

    def test_file__save_with_deep_path(self):                                          # Test saving with nested directories
        deep_path = Safe_Str__File__Path("level1/level2/level3/file.txt")

        with self.storage as _:
            assert _.file__save(deep_path, self.test_content) is True
            assert _.file__exists(deep_path) is True
            assert _.file__bytes(deep_path) == self.test_content
            assert file_exists(_.full_path(deep_path))                   is True
            assert folder_exists(parent_folder(_.full_path(deep_path))) is True

    def test_file__bytes(self):                                                        # Test reading file as bytes
        with self.storage as _:
            assert _.file__bytes(self.test_path) is None                               # File doesn't exist yet

            _.file__save(self.test_path, self.test_content)
            result = _.file__bytes(self.test_path)

            assert result == self.test_content
            assert type(result) is bytes

    def test_file__str(self):                                                          # Test reading file as string
        string_content = "Hello, World! 文字"
        bytes_content  = string_content.encode('utf-8')

        with self.storage as _:
            assert _.file__str(self.test_path) is None                                 # File doesn't exist yet

            _.file__save(self.test_path, bytes_content)
            result = _.file__str(self.test_path)

            assert result == string_content
            assert type(result) is str

    def test_file__str_with_invalid_utf8(self):                                        # Test reading invalid UTF-8
        invalid_bytes = b'\x80\x81\x82\x83'

        with self.storage as _:
            _.file__save(self.test_path, invalid_bytes)
            assert _.file__bytes(self.test_path) == invalid_bytes                       # we should be able to get the bytes ok from the file, but

            error_message = "'utf-8' codec can't decode byte 0x80 in position 0: invalid start byte"
            with pytest.raises(UnicodeDecodeError, match=error_message):
                _.file__str(self.test_path)                                             # it should raise when trying to go into a string

    def test_file__json(self):                                                         # Test reading file as JSON
        json_bytes = json_to_bytes(self.test_json)

        with self.storage as _:
            assert _.file__json(self.test_path) is None                                # File doesn't exist yet

            _.file__save(self.test_path, json_bytes)
            result = _.file__json(self.test_path)

            assert result == self.test_json
            assert type(result) is dict

    def test_file__json_with_invalid_json(self):                                       # Test reading invalid JSON
        invalid_json = b"not valid json"

        with self.storage as _:
            _.file__save(self.test_path, invalid_json)
            assert _.file__bytes(self.test_path) == invalid_json
            error_message = "Expecting value: line 1 column 1 (char 0)"
            with pytest.raises(JSONDecodeError, match=re.escape(error_message)):
                _.file__json(self.test_path)

    def test_file__exists(self):                                                       # Test file existence check
        with self.storage as _:
            assert _.file__exists(self.test_path) is False

            _.file__save(self.test_path, self.test_content)
            assert _.file__exists(self.test_path) is True

            # Test with directory (should return False)
            dir_path = Safe_Str__File__Path("test_dir")
            folder_create(_.full_path(dir_path))
            assert _.file__exists(dir_path) is False                                   # Directories are not files

    def test_file__delete(self):                                                       # Test file deletion
        with self.storage as _:
            assert _.file__delete(self.test_path) is False                             # Can't delete non-existent file

            _.file__save(self.test_path, self.test_content)
            assert _.file__exists(self.test_path) is True
            assert _.file__delete(self.test_path) is True
            assert _.file__exists(self.test_path) is False
            assert _.file__delete(self.test_path) is False                             # Already deleted

    def test_file__delete_with_cleanup(self):                                          # Test directory cleanup after deletion
        deep_path = Safe_Str__File__Path("a/b/c/file.txt")

        with self.storage as _:
            _.file__save(deep_path, self.test_content)

            # Verify directories exist
            full_path = _.full_path(deep_path)
            parent_dir = path_combine(str(_.root_path), "a/b/c")
            assert folder_exists(parent_dir) is True

            _.file__delete(deep_path)

            assert folder_exists(parent_dir) is True                                    # Empty directories are NOT cleaned up
            assert folder_exists(path_combine(str(_.root_path), "a/b")) is True

    def test_file__delete_with_non_empty_dir(self):                                    # Test deletion doesn't remove non-empty dirs
        path1 = Safe_Str__File__Path("shared/file1.txt")
        path2 = Safe_Str__File__Path("shared/file2.txt")

        with self.storage as _:
            _.file__save(path1, b"content1")
            _.file__save(path2, b"content2")

            _.file__delete(path1)

            # Directory should still exist (has file2.txt)
            shared_dir = path_combine(str(_.root_path), "shared")
            assert folder_exists(shared_dir) is True
            assert _.file__exists(path2) is True

    def test_files__paths(self):                                                       # Test listing all file paths
        with self.storage as _:
            assert _.files__paths() == []                                              # Empty initially

            # Create multiple files
            paths = [Safe_Str__File__Path("file1.txt")       ,
                     Safe_Str__File__Path("dir/file2.txt")   ,
                     Safe_Str__File__Path("dir/sub/file3.txt")]

            for path in paths:
                _.file__save(path, b"content")

            result = _.files__paths()
            assert len(result) == 3
            assert set(result) == set(paths)                                           # Order may vary

    def test_files__paths_with_mixed_content(self):                                    # Test listing ignores directories
        with self.storage as _:
            # Create files
            _.file__save(Safe_Str__File__Path("file.txt"), b"content")

            # Create directory
            dir_path = path_combine(str(_.root_path), "empty_dir")
            folder_create(dir_path)

            result = _.files__paths()
            assert len(result) == 1
            assert result == [Safe_Str__File__Path("file.txt")]

    def test_clear(self):                                                              # Test clearing all storage
        with self.storage as _:
            # Create multiple files and directories
            _.file__save(Safe_Str__File__Path("file1.txt"), b"content1")
            _.file__save(Safe_Str__File__Path("dir/file2.txt"), b"content2")
            _.file__save(Safe_Str__File__Path("dir/sub/file3.txt"), b"content3")

            assert len(_.files__paths()) == 3
            assert _.clear() is True
            assert len(_.files__paths()) == 0

            # Root directory should still exist
            assert folder_exists(str(_.root_path)) is True

    def test_concurrent_operations(self):                                              # Test multiple operations
        with self.storage as _:
            paths = [Safe_Str__File__Path(f"file{i}.txt") for i in range(10)]

            # Save all files
            for i, path in enumerate(paths):
                assert _.file__save(path, f"content{i}".encode()) is True

            # Verify all exist
            for path in paths:
                assert _.file__exists(path) is True

            # Delete even-numbered files
            for i in range(0, 10, 2):
                assert _.file__delete(paths[i]) is True

            # Verify correct files remain
            remaining = _.files__paths()
            assert len(remaining) == 5

            for i in range(1, 10, 2):
                assert paths[i] in remaining

    def test_error_handling(self):                                                     # Test error handling
        with self.storage as _:
            # Test with invalid path characters (should be handled by Safe_Str__File__Path)
            # Most errors should be silently handled, returning False or None

            # Try to read non-existent file
            assert _.file__bytes(Safe_Str__File__Path("nonexistent")) is None
            assert _.file__str(Safe_Str__File__Path("nonexistent")) is None
            assert _.file__json(Safe_Str__File__Path("nonexistent")) is None

            # Try to delete non-existent file
            assert _.file__delete(Safe_Str__File__Path("nonexistent")) is False

    def test_special_filenames(self):                                                  # Test special filenames
        special_names = [Safe_Str__File__Path(".hidden")              ,
                         Safe_Str__File__Path("file.multiple.dots")   ,
                         Safe_Str__File__Path("file-with-dashes")     ,
                         Safe_Str__File__Path("file_with_underscores")]

        with self.storage as _:
            for name in special_names:
                assert _.file__save(name, b"content") is True
                assert _.file__exists(name) is True

            assert len(_.files__paths()) == len(special_names)
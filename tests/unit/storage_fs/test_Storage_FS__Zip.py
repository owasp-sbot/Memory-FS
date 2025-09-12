import pytest
import re
from json                                                                       import JSONDecodeError
from unittest                                                                   import TestCase
from zipfile                                                                    import BadZipFile
from osbot_utils.type_safe.primitives.domains.files.safe_str.Safe_Str__File__Path  import Safe_Str__File__Path
from osbot_utils.utils.Json                                                     import json_to_bytes
from osbot_utils.utils.Zip                                                      import zip_bytes__file_list
from memory_fs.storage_fs.providers.Storage_FS__Zip                             import Storage_FS__Zip


class test_Storage_FS__Zip(TestCase):                                                  # Test Zip storage operations

    def setUp(self):                                                                    # Initialize test data
        self.storage = Storage_FS__Zip()

        # Test data
        self.test_path    = Safe_Str__File__Path("test/file.txt")
        self.test_content = b"test content"
        self.test_json    = {"key": "value", "number": 42}

    def test__init__(self):                                                             # Test initialization
        with self.storage as _:
            assert type(_)           is Storage_FS__Zip
            assert type(_.zip_bytes) is bytes
            assert _.zip_bytes       == b""                                            # Should start with empty zip
            assert _.file_count()    == 0

    def test__init__with_existing_zip(self):                                           # Test initialization with existing zip bytes
        # Create a zip with content
        storage_temp = Storage_FS__Zip()
        storage_temp.file__save(Safe_Str__File__Path("existing.txt"), b"existing content")
        existing_zip_bytes = storage_temp.zip_bytes

        # Initialize new storage with existing zip
        storage = Storage_FS__Zip(zip_bytes=existing_zip_bytes)

        assert storage.file_count() == 1
        assert storage.file__exists(Safe_Str__File__Path("existing.txt")) is True
        assert storage.file__bytes(Safe_Str__File__Path("existing.txt")) == b"existing content"

    def test_file__save(self):                                                         # Test file saving to zip
        with self.storage as _:
            assert _.file__exists(self.test_path) is False
            assert _.file__save(self.test_path, self.test_content) is True
            assert _.file__exists(self.test_path) is True

            # Verify in zip structure
            files_in_zip = zip_bytes__file_list(_.zip_bytes)
            assert str(self.test_path) in files_in_zip

    def test_file__save_nested_path(self):                                             # Test saving with nested directories
        nested_path = Safe_Str__File__Path("folder1/folder2/folder3/file.txt")

        with self.storage as _:
            assert _.file__save(nested_path, self.test_content) is True
            assert _.file__exists(nested_path) is True
            assert _.file__bytes(nested_path) == self.test_content

    def test_file__save_update(self):                                                  # Test updating existing file
        with self.storage as _:
            _.file__save(self.test_path, b"original")
            assert _.file__bytes(self.test_path) == b"original"

            _.file__save(self.test_path, b"updated")
            assert _.file__bytes(self.test_path) == b"updated"

            # Should still only have one file
            assert _.file_count() == 1

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
            assert _.file__bytes(self.test_path) == invalid_bytes
            expected_error = "'utf-8' codec can't decode byte 0x80 in position 0: invalid start byte"
            with pytest.raises(UnicodeDecodeError, match=re.escape(expected_error)):
                _.file__str(self.test_path)

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
            expected_error = "Expecting value: line 1 column 1 (char 0)"
            with pytest.raises(JSONDecodeError, match=re.escape(expected_error)):
                _.file__json(self.test_path)

    def test_file__exists(self):                                                       # Test file existence check
        with self.storage as _:
            assert _.file__exists(self.test_path) is False

            _.file__save(self.test_path, self.test_content)
            assert _.file__exists(self.test_path) is True

    def test_file__delete(self):                                                       # Test file deletion
        with self.storage as _:
            assert _.file__delete(self.test_path) is False                             # Can't delete non-existent file

            _.file__save(self.test_path, self.test_content)
            assert _.file__exists(self.test_path) is True
            assert _.file__delete(self.test_path) is True
            assert _.file__exists(self.test_path) is False
            assert _.file__delete(self.test_path) is False                             # Already deleted

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
            assert result == sorted(paths)                                             # Should be sorted

    def test_clear(self):                                                              # Test clearing all storage
        with self.storage as _:
            # Create multiple files
            for i in range(5):
                _.file__save(Safe_Str__File__Path(f"file{i}.txt"), f"content{i}".encode())

            assert _.file_count() == 5
            assert _.clear() is True
            assert _.file_count() == 0
            assert _.files__paths() == []

            # Zip should be empty
            assert _.zip_bytes == b""

    def test_get_all_files(self):                                                      # Test getting all files with contents
        with self.storage as _:
            files_data = {
                "file1.txt": b"content1",
                "file2.txt": b"content2",
                "dir/file3.txt": b"content3"
            }

            for path, content in files_data.items():
                _.file__save(Safe_Str__File__Path(path), content)

            all_files = _.get_all_files()
            assert len(all_files) == 3

            for path, content in files_data.items():
                assert all_files[path] == content

    def test_size_bytes(self):                                                         # Test getting zip size in bytes
        with self.storage as _:
            initial_size = _.size_bytes()
            assert initial_size == 0                                                    # Empty zip is 0

            # Add content and check size increases
            _.file__save(self.test_path, b"x" * 1000)
            new_size = _.size_bytes()
            assert new_size > initial_size

    def test_file_count(self):                                                         # Test file counting
        with self.storage as _:
            assert _.file_count() == 0

            for i in range(10):
                _.file__save(Safe_Str__File__Path(f"file{i}.txt"), b"content")
                assert _.file_count() == i + 1

    def test_export_bytes(self):                                                       # Test exporting zip as bytes
        with self.storage as _:
            _.file__save(self.test_path, self.test_content)

            exported = _.export_bytes()
            assert type(exported) is bytes
            assert exported == _.zip_bytes

            # Verify exported bytes are valid zip
            files_in_export = zip_bytes__file_list(exported)
            assert str(self.test_path) in files_in_export

    def test_import_bytes(self):                                                       # Test importing zip from bytes
        # Create a zip with content
        source_storage = Storage_FS__Zip()
        source_storage.file__save(Safe_Str__File__Path("imported.txt"), b"imported content")
        zip_to_import = source_storage.export_bytes()

        # Import into new storage
        with self.storage as _:
            assert _.file_count() == 0
            assert _.import_bytes(zip_to_import) is True
            assert _.file_count() == 1
            assert _.file__exists(Safe_Str__File__Path("imported.txt")) is True
            assert _.file__bytes(Safe_Str__File__Path("imported.txt")) == b"imported content"

    def test_import_bytes_invalid(self):                                               # Test importing invalid zip bytes
        with self.storage as _:
            expected_error ="File is not a zip file"
            with pytest.raises(BadZipFile, match=expected_error):
                _.import_bytes(b"not a valid zip")
                assert _.file_count() == 0                                                 # Should remain unchanged

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

    def test_large_content(self):                                                      # Test with large content
        large_content = b"x" * (1024 * 1024)                                           # 1MB
        path = Safe_Str__File__Path("large_file.bin")

        with self.storage as _:
            assert _.file__save(path, large_content) is True
            assert _.file__bytes(path) == large_content

    def test_binary_data(self):                                                        # Test with binary data
        binary_data = bytes(range(256))                                                # All byte values
        path = Safe_Str__File__Path("binary.bin")

        with self.storage as _:
            assert _.file__save(path, binary_data) is True
            assert _.file__bytes(path) == binary_data

    def test_empty_file(self):                                                         # Test empty file handling
        empty_path = Safe_Str__File__Path("empty.txt")

        with self.storage as _:
            assert _.file__save(empty_path, b"") is True
            assert _.file__exists(empty_path   ) is True
            assert _.file__bytes(empty_path    ) == b""
            assert _.file__str(empty_path      ) == ""

    def test_special_characters_in_path(self):                                         # Test paths with special characters
        special_paths = [Safe_Str__File__Path("file with spaces.txt")   ,
                         Safe_Str__File__Path("file-with-dashes.txt")   ,
                         Safe_Str__File__Path("file_with_underscores.txt")]

        with self.storage as _:
            for path in special_paths:
                assert _.file__save(path, b"content") is True
                assert _.file__exists(path) is True

            assert _.file_count() == len(special_paths)

    def test_path_with_leading_slash(self):                                            # Test path normalization
        # Zip helper should handle leading slashes
        path_with_slash    = Safe_Str__File__Path("/folder/file.txt")
        path_without_slash = Safe_Str__File__Path("folder/file.txt")

        with self.storage as _:
            _.file__save(path_with_slash, b"content")

            # Should be accessible without leading slash (normalized)
            assert _.file__exists(path_without_slash) is True
            assert _.file__bytes(path_without_slash) == b"content"

    def test_replace_vs_add_behavior(self):                                            # Test replace vs add logic
        with self.storage as _:
            # First save (should use add)
            _.file__save(self.test_path, b"version1")
            version1_size = _.size_bytes()

            # Second save (should use replace)
            _.file__save(self.test_path, b"version2_longer_content")
            version2_size = _.size_bytes()

            # Verify content was replaced, not added
            assert _.file__bytes(self.test_path) == b"version2_longer_content"
            assert _.file_count() == 1                                                 # Still only one file

            # Size should have changed appropriately
            assert version2_size != version1_size

    def test_roundtrip_export_import(self):                                            # Test export and re-import
        with self.storage as _:
            # Create complex structure
            files = {
                "root.txt": b"root content",
                "folder1/file1.txt": b"file1 content",
                "folder1/folder2/file2.txt": b"file2 content",
                "folder3/file3.json": json_to_bytes({"data": "value"})
            }

            for path, content in files.items():
                _.file__save(Safe_Str__File__Path(path), content)

            # Export
            exported = _.export_bytes()

            # Clear and re-import
            _.clear()
            assert _.file_count() == 0

            _.import_bytes(exported)
            assert _.file_count() == len(files)

            # Verify all files restored correctly
            for path, content in files.items():
                assert _.file__bytes(Safe_Str__File__Path(path)) == content
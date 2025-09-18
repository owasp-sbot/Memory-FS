import re
import tempfile
import pytest
from json import JSONDecodeError
from unittest                                                                       import TestCase
from osbot_utils.type_safe.primitives.domains.files.safe_str.Safe_Str__File__Path   import Safe_Str__File__Path
from osbot_utils.type_safe.primitives.domains.identifiers.safe_str.Safe_Str__Id     import Safe_Str__Id
from osbot_utils.utils.Json                                                         import json_to_bytes
from osbot_utils.utils.Files                                                        import folder_delete_all, file_exists, file_size
from osbot_utils.helpers.sqlite.Sqlite__Database                                    import Sqlite__Database
from memory_fs.storage_fs.providers.Storage_FS__Sqlite                              import Storage_FS__Sqlite


class test_Storage_FS__Sqlite(TestCase):                                               # Test SQLite storage operations

    @classmethod
    def setUpClass(cls):                                                                    # Initialize test data
        cls.temp_dir     = tempfile.mkdtemp()
        cls.db_path      = Safe_Str__File__Path(cls.temp_dir) + "/test.db"
        cls.in_memory    = False
        cls.storage      = Storage_FS__Sqlite(db_path=cls.db_path, in_memory=cls.in_memory).setup()

        cls.test_path    = Safe_Str__File__Path("test/file.txt")                            # Test data
        cls.test_content = b"test content"
        cls.test_json    = {"key": "value", "number": 42}

    @classmethod
    def tearDownClass(cls):                                                                 # Clean up temp directory
        cls.storage.database.close()
        folder_delete_all(cls.temp_dir)

    def test__init__(self):                                                             # Test initialization
        with self.storage as _:
            assert type(_)            is Storage_FS__Sqlite
            assert type(_.db_path)    is Safe_Str__File__Path
            assert type(_.table_name) is Safe_Str__Id
            assert type(_.database)   is Sqlite__Database
            assert file_exists(str(_.db_path)) is True
            assert _.table_name       == Safe_Str__Id("memory_fs_files")

    def test__init__with_string_path(self):                                            # Test initialization with string path
        string_path = f"{self.temp_dir}/subfolder/test.db"
        storage     = Storage_FS__Sqlite(db_path=string_path, in_memory=False).setup()
        assert type(storage.db_path)             is Safe_Str__File__Path
        assert file_exists(str(storage.db_path)) is True
        assert str(storage.db_path) == string_path
        storage.database.close()

    def test__init_database(self):                                                     # Test database initialization
        with self.storage as _:
            # Check table exists
            assert _.table.exists() is True

            # Check schema is correct
            schema = _.table.schema__by_name_type()
            assert 'path' in schema
            assert 'data' in schema
            assert 'created_at' in schema
            assert 'updated_at' in schema

            # Check index exists
            indexes = _.table.indexes()
            assert f'idx__{_.table_name}__path' in indexes

    def test_database_connection(self):                                                # Test database connection
        with self.storage as _:
            assert _.database.connected is True
            connection = _.database.connection()
            assert connection is not None

    def test_file__save(self):                                                         # Test file saving
        with self.storage as _:
            assert _.file__exists(self.test_path) is False
            assert _.file__save(self.test_path, self.test_content) is True
            assert _.file__exists(self.test_path) is True

            # Verify in database
            row = _.table.select_row_where(path=str(self.test_path))
            assert row is not None
            assert row['data'] == self.test_content

    def test_file__save_update(self):                                                  # Test updating existing file
        with self.storage as _:
            _.file__save(self.test_path, b"original")
            assert _.file__bytes(self.test_path) == b"original"

            _.file__save(self.test_path, b"updated")
            assert _.file__bytes(self.test_path) == b"updated"

            # Should only have one row
            rows = _.table.select_rows_where(path=str(self.test_path))
            assert len(rows) == 1
            assert _.file__delete(self.test_path) is True

    def test_file__bytes(self):                                                        # Test reading file as bytes
        with self.storage as _:
            assert _.file__bytes(self.test_path) is None                               # File doesn't exist yet

            _.file__save(self.test_path, self.test_content)
            result = _.file__bytes(self.test_path)

            assert result == self.test_content
            assert type(result) is bytes
            assert _.file__delete(self.test_path) is True

    def test_file__str(self):                                                          # Test reading file as string
        string_content = "Hello, World! 文字"
        bytes_content  = string_content.encode('utf-8')

        with self.storage as _:
            assert _.file__str(self.test_path) is None                                 # File doesn't exist yet

            _.file__save(self.test_path, bytes_content)
            result = _.file__str(self.test_path)

            assert result == string_content
            assert type(result) is str
            assert _.file__delete(self.test_path) is True

    def test_file__str_with_invalid_utf8(self):                                        # Test reading invalid UTF-8
        invalid_bytes = b'\x80\x81\x82\x83'

        with self.storage as _:
            _.file__save(self.test_path, invalid_bytes)
            assert _.file__bytes(self.test_path) == invalid_bytes
            error_message = "'utf-8' codec can't decode byte 0x80 in position 0: invalid start byte"
            with pytest.raises(UnicodeDecodeError, match=error_message):
                _.file__str(self.test_path)
            assert _.file__delete(self.test_path) is True


    def test_file__json(self):                                                         # Test reading file as JSON
        json_bytes = json_to_bytes(self.test_json)

        with self.storage as _:
            assert _.file__json(self.test_path) is None                                # File doesn't exist yet

            _.file__save(self.test_path, json_bytes)
            result = _.file__json(self.test_path)

            assert result == self.test_json
            assert type(result) is dict
            assert _.file__delete(self.test_path) is True


    def test_file__json_with_invalid_json(self):                                       # Test reading invalid JSON
        invalid_json = b"not valid json"

        with self.storage as _:
            _.file__save(self.test_path, invalid_json)
            assert _.file__bytes(self.test_path) == invalid_json
            error_message = "Expecting value: line 1 column 1 (char 0)"
            with pytest.raises(JSONDecodeError, match=re.escape(error_message)):
                 _.file__json(self.test_path)
            assert _.file__delete(self.test_path) is True

    def test_file__exists(self):                                                       # Test file existence check
        with self.storage as _:
            assert _.file__exists(self.test_path) is False

            _.file__save(self.test_path, self.test_content)
            assert _.file__exists(self.test_path) is True
            assert _.file__delete(self.test_path) is True

    def test__file__delete(self):                                                      # Test file deletion
        with self.storage as _:
            assert _.file__delete(self.test_path) is False                                  # Can't delete non-existent file

            _.file__save(self.test_path, self.test_content)
            assert _.file__exists(self.test_path) is True
            assert _.file__delete(self.test_path) is True
            assert _.file__exists(self.test_path) is False
            assert _.file__delete(self.test_path) is False                                   # Already deleted

    def test_files__paths(self):                                                       # Test listing all file paths
        with self.storage as _:
            assert _.clear() is True
            assert _.files__paths() == []                                              # Empty initially

            # Create multiple files
            paths = [Safe_Str__File__Path("file1.txt")       ,
                     Safe_Str__File__Path("dir/file2.txt")   ,
                     Safe_Str__File__Path("dir/sub/file3.txt")]

            for path in paths:
                _.file__save(path, b"content")

            result = _.files__paths()
            assert len(result) == 3
            assert result == sorted(paths)                                             # SQLite returns sorted

    def test_clear(self):                                                              # Test clearing all storage
        with self.storage as _:
            # Create multiple files
            for i in range(5):
                _.file__save(Safe_Str__File__Path(f"file{i}.txt"), f"content{i}".encode())

            assert len(_.files__paths()) == 5
            assert _.clear() is True
            assert len(_.files__paths()) == 0

            # Database file should still exist
            assert file_exists(str(_.db_path)) is True

    def test_optimize(self):                                                           # Test database optimization
        with self.storage as _:
            # Add and delete files to create fragmentation
            for i in range(10):
                _.file__save(Safe_Str__File__Path(f"file{i}.txt"), f"content{i}".encode())

            for i in range(0, 10, 2):
                _.file__delete(Safe_Str__File__Path(f"file{i}.txt"))

            # Optimize should succeed
            assert _.optimize() is True
            assert _.clear() is True

    def test_concurrent_operations(self):                                              # Test multiple operations
        with self.storage as _:
            assert _.clear() is True
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

    def test_special_characters_in_path(self):                                         # Test paths with special characters
        special_paths = [Safe_Str__File__Path("file with spaces.txt")   ,
                         Safe_Str__File__Path("file'with'quotes.txt")   ,
                         Safe_Str__File__Path('file"with"dquotes.txt')  ,
                         Safe_Str__File__Path("file;with;semicolon.txt")]

        with self.storage as _:
            for path in special_paths:
                assert _.file__save(path, b"content") is True
                assert _.file__exists(path) is True

            assert len(_.files__paths()) == len(special_paths)
            assert _.clear() is True

    def test_timestamps(self):                                                         # Test timestamp columns
        with self.storage as _:
            _.file__save(self.test_path, self.test_content)

            row = _.table.select_row_where(path=str(self.test_path))
            assert row is not None
            assert row['created_at'] is not None
            assert row['updated_at'] is not None

            original_updated = row['updated_at']

            # Update the file
            _.file__save(self.test_path, b"new content")

            row_updated = _.table.select_row_where(path=str(self.test_path))
            assert row_updated['updated_at'] is not None
            # Note: Can't easily test if updated_at changed due to timing

    def test_error_handling(self):                                                     # Test error handling
        with self.storage as _:
            # Test with non-existent file
            assert _.file__bytes(Safe_Str__File__Path("nonexistent")) is None
            assert _.file__str(Safe_Str__File__Path("nonexistent")) is None
            assert _.file__json(Safe_Str__File__Path("nonexistent")) is None
            assert _.file__delete(Safe_Str__File__Path("nonexistent")) is False

    def test_binary_data(self):                                                        # Test with binary data
        binary_data = bytes(range(256))                                                # All byte values
        path = Safe_Str__File__Path("binary.bin")

        with self.storage as _:
            assert _.file__save(path, binary_data) is True
            assert _.file__bytes(path)             == binary_data
            assert _.file__delete(path)            is True

    def test_empty_file(self):                                                         # Test empty file handling
        empty_path = Safe_Str__File__Path("empty.txt")

        with self.storage as _:
            assert _.file__save  (empty_path, b"") is True
            assert _.file__exists(empty_path     ) is True
            assert _.file__bytes(empty_path      ) == b""
            assert _.file__str  (empty_path      ) == ''

    def test_custom_table_name(self):                                                  # Test with custom table name
        custom_storage = Storage_FS__Sqlite(db_path    = self.db_path              ,
                                            table_name = Safe_Str__Id("custom_table")   ).setup()

        with custom_storage as _:
            _.file__save(self.test_path, self.test_content)
            # Check custom table exists using OSBot_Utils
            assert _.table.table_name == "custom_table"
            assert _.table.exists() is True

            # Verify data is in custom table
            row = _.table.select_row_where(path=str(self.test_path))
            assert row is not None
            assert row['data'] == self.test_content

        custom_storage.database.close()

    def test_table_operations(self):                                                   # Test direct table operations
        with self.storage as _:
            # Test table methods
            assert _.table.exists() is True
            assert _.table.size() == 0

            # Add data
            _.file__save(self.test_path, self.test_content)
            assert _.table.size() == 1

            # Test field values
            paths = _.table.select_field_values('path')
            assert paths == [str(self.test_path)]

            # Test schema
            fields = _.table.fields_names__cached()
            assert 'path' in fields
            assert 'data' in fields
from unittest                                                                       import TestCase
from osbot_utils.type_safe.type_safe_core.collections.Type_Safe__Dict               import Type_Safe__Dict
from memory_fs.storage_fs.providers.Storage_FS__Memory                              import Storage_FS__Memory
from osbot_utils.type_safe.primitives.domains.files.safe_str.Safe_Str__File__Path      import Safe_Str__File__Path
from osbot_utils.utils.Json                                                         import json_to_bytes


class test_Storage_FS__Memory(TestCase):                                                # Test memory storage provider

    def setUp(self):                                                                    # Initialize test data
        self.storage    = Storage_FS__Memory()
        self.test_path  = Safe_Str__File__Path("test/file.txt")
        self.test_data  = b"test content"
        self.test_json  = {"key": "value", "number": 42}

    def test__init__(self):                                                             # Test initialization
        with self.storage as _:
            assert type(_)              is Storage_FS__Memory
            assert type(_.content_data) is Type_Safe__Dict
            assert _.content_data       == {}

    def test_clear(self):                                                               # Test clearing storage
        with self.storage as _:
            assert _.file__save(self.test_path, self.test_data) is True
            assert len(_.content_data)                          == 1
            result = _.clear()
            assert result                                       is True
            assert len(_.content_data)                          == 0

    def test_file__bytes(self):                                                         # Test file bytes retrieval
        with self.storage as _:
            assert _.file__bytes(self.test_path)                is None
            assert _.file__save(self.test_path, self.test_data) is True
            assert _.file__bytes(self.test_path)                == self.test_data

    def test_file__delete(self):                                                        # Test file deletion
        with self.storage as _:
            assert _.file__delete(self.test_path)               is False                # File doesn't exist
            assert _.file__save(self.test_path, self.test_data) is True
            assert _.file__delete(self.test_path)               is True                 # File deleted
            assert _.file__exists(self.test_path)               is False

    def test_file__exists(self):                                                        # Test file existence check
        with self.storage as _:
            assert _.file__exists(self.test_path              ) is False
            assert _.file__save(self.test_path, self.test_data) is True
            assert _.file__exists(self.test_path              ) is True

    def test_file__json(self):                                                          # Test file JSON retrieval
        with self.storage as _:
            json_bytes = json_to_bytes(self.test_json)

            assert _.file__json(self.test_path            ) is None
            assert _.file__save(self.test_path, json_bytes) is True
            assert _.file__json(self.test_path            ) == self.test_json

    def test_file__save(self):                                                          # Test file saving
        with self.storage as _:
            result = _.file__save(self.test_path, self.test_data)
            assert result                        is True
            assert _.content_data[self.test_path] == self.test_data

    def test_file__str(self):                                                           # Test file string retrieval
        with self.storage as _:
            text = "Hello, world!"
            assert _.file__str(self.test_path                ) is None
            assert _.file__save(self.test_path, text.encode()) is True
            assert _.file__str(self.test_path                ) == text

    def test_files__paths(self):                                                        # Test getting all file paths
        with self.storage as _:
            assert list(_.files__paths()) == []

            path1 = Safe_Str__File__Path("file1.txt")
            path2 = Safe_Str__File__Path("dir/file2.txt")

            assert _.file__save(path1, b"data1") is True
            assert _.file__save(path2, b"data2") is True

            paths = sorted(list(_.files__paths()))
            assert paths == [path2, path1]                                              # Note: dict ordering
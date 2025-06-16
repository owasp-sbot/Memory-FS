from unittest                                               import TestCase
from memory_fs.core.Memory_FS__File_System                  import Memory_FS__File_System
from memory_fs.schemas.Schema__Memory_FS__File              import Schema__Memory_FS__File
from osbot_utils.type_safe.Type_Safe__Dict                  import Type_Safe__Dict
from osbot_utils.helpers.safe_str.Safe_Str__File__Path      import Safe_Str__File__Path


class test_Memory_FS__File_System(TestCase):                                            # Test the core file system class

    def setUp(self):                                                                    # Initialize test data
        self.file_system = Memory_FS__File_System()
        self.test_path   = Safe_Str__File__Path("test/file.txt")
        self.test_file   = Schema__Memory_FS__File()
        self.test_bytes  = b"test content"

    def test__init__(self):                                                             # Test initialization
        with self.file_system as _:
            assert type(_)               is Memory_FS__File_System
            assert type(_.files)         is Type_Safe__Dict
            assert type(_.content_data)  is Type_Safe__Dict
            assert len(_.files)          == 0
            assert len(_.content_data)   == 0

    def test_files(self):                                                               # Test files dictionary
        with self.file_system as _:
            assert _.files == {}

            _.files[self.test_path] = self.test_file
            assert len(_.files)                == 1
            assert _.files[self.test_path]     == self.test_file

    def test_content_data(self):                                                        # Test content_data dictionary
        with self.file_system as _:
            assert _.content_data == {}

            _.content_data[self.test_path] = self.test_bytes
            assert len(_.content_data)              == 1
            assert _.content_data[self.test_path]   == self.test_bytes
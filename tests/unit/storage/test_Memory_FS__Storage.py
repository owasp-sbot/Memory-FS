from unittest                                               import TestCase
from memory_fs.storage.Memory_FS__Storage                   import Memory_FS__Storage
from memory_fs.storage_fs.Storage_FS                        import Storage_FS
from osbot_utils.helpers.Safe_Id                            import Safe_Id
from osbot_utils.helpers.safe_str.Safe_Str__File__Path      import Safe_Str__File__Path


class test_Memory_FS__Storage(TestCase):                                                # Test storage class

    def setUp(self):                                                                    # Initialize test data
        self.storage   = Memory_FS__Storage()
        self.test_path = Safe_Str__File__Path("test/file.txt")
        self.test_data = b"test content"

    def test__init__(self):                                                             # Test initialization
        with self.storage as _:
            assert type(_)              is Memory_FS__Storage
            assert type(_.storage_fs)   is Storage_FS
            assert _.storage_type       == Safe_Id('memory')

    def test_file__content(self):                                                       # Test file content retrieval
        with self.storage as _:
            assert _.storage_fs.file__save(self.test_path, self.test_data)  is False    # Storage_FS doesn't save the file
            assert _.file__content(self.test_path)                          is None

    def test_file__delete(self):                                                        # Test file deletion
        with self.storage as _:
            _.storage_fs.file__save(self.test_path, self.test_data)
            assert _.file__delete(self.test_path) is False                              # Storage_FS doesn't delete the file
            assert _.file__exist(self.test_path)  is False

    def test_file__exist(self):                                                         # Test file existence check
        with self.storage as _:
            assert _.file__exist(self.test_path)                           is False
            assert _.storage_fs.file__save(self.test_path, self.test_data) is False     # Storage_FS doesn't create the file
            assert _.file__exist(self.test_path)                           is False

    def test_file__save(self):                                                          # Test file saving
        with self.storage as _:
            assert _.file__save(self.test_path, self.test_data) is False                # Storage_FS doesn't save
            assert _.file__exist(self.test_path)                is False                # which means that the file doesn't exist
            assert _.file__content(self.test_path)              is None                 # and there is no content

    def test_files__paths(self):                                                        # Test getting all file paths
        with self.storage as _:
            path1 = Safe_Str__File__Path("file1.txt")
            path2 = Safe_Str__File__Path("file2.txt")

            assert list(_.files__paths())        == []                                  # there are no files before
            assert _.file__save(path1, b"data1") is False                               # Storage_FS doesn't save
            assert _.file__save(path2, b"data2") is False
            assert _.files__paths()              == []                                  # there are no files after
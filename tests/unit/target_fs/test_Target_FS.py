from tests.unit.Base_Test__File_FS                          import Base_Test__File_FS
from memory_fs.target_fs.Target_FS                          import Target_FS
from memory_fs.file_fs.File_FS                              import File_FS


class test_Target_FS(Base_Test__File_FS):                                               # Test target FS class

    def setUp(self):                                                                    # Initialize test data
        super().setUp()
        self.target_fs = Target_FS(file_config = self.file_config ,
                                   storage_fs  = self.storage_fs     )

    def test__init__(self):                                                             # Test initialization
        with self.target_fs as _:
            assert type(_)         is Target_FS
            assert _.file_config   == self.file_config
            assert _.storage_fs    == self.storage_fs

    def test_file_fs(self):                                                             # Test file_fs method
        with self.target_fs as _:
            file_fs = _.file_fs()
            assert type(file_fs)       is File_FS
            assert file_fs.file_config == self.file_config
            assert file_fs.storage_fs  == self.storage_fs

    def test_file_fs_cached(self):                                                      # Test that file_fs is cached
        with self.target_fs as _:
            file_fs_1 = _.file_fs()
            file_fs_2 = _.file_fs()
            assert file_fs_1 is file_fs_2                                               # Same instance due to @cache_on_self
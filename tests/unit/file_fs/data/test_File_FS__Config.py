from tests.unit.Base_Test__File_FS                          import Base_Test__File_FS
from memory_fs.file_fs.data.File_FS__Config                 import File_FS__Config
from memory_fs.schemas.Schema__Memory_FS__File__Config      import Schema__Memory_FS__File__Config


class test_File_FS__Config(Base_Test__File_FS):                                        # Test file config operations

    def setUp(self):                                                                    # Initialize test data
        super().setUp()
        self.file_fs_config = File_FS__Config(file__config = self.file_config ,
                                              storage_fs   = self.storage_fs      )

    def test__init__(self):                                                             # Test initialization
        with self.file_fs_config as _:
            assert type(_)                  is File_FS__Config
            assert type(_.file__config)     is Schema__Memory_FS__File__Config
            assert type(_.storage_fs)       is type(self.storage_fs)
            assert _.storage_fs             == self.storage_fs                             # confirm the storage is correctly setup

    def test_config(self):                                                              # Test config method
        with self.file_fs_config as _:
            assert _.config() == self.file_config

    def test_file_id(self):                                                             # Test file_id method
        with self.file_fs_config as _:
            assert _.file_id() == self.file_config.file_id

    def test_file_name(self):                                                           # Test file_name method
        with self.file_fs_config as _:
            assert _.file_name() == f'{_.file_id()}.json.config'

    def test_exists(self):                                                              # Test exists method
        with self.file_fs_config as _:
            assert _.exists() is False
            assert _.create() == [f'{self.file_config.file_id}.json.config']
            assert _.exists() is True
from unittest                                           import TestCase
from memory_fs.file_fs.data.File_FS__Config             import File_FS__Config
from memory_fs.schemas.Schema__Memory_FS__File__Config  import Schema__Memory_FS__File__Config
from memory_fs.storage_fs.Storage_FS                    import Storage_FS


class test_Memory_FS__File__Config(TestCase):

    @classmethod
    def setUpClass(cls):
        cls.file_config                    = File_FS__Config()
        # cls.storage_fs                     = Storage_FS__Memory()
        # cls.file_config.storage.storage_fs = cls.storage_fs  # todo: find a better way to do this assigment (especially for tests)

    def test__init__(self):
        with self.file_config as _:
            assert type(_             ) is File_FS__Config
            assert type(_.file__config)  is Schema__Memory_FS__File__Config
            assert type(_.storage_fs  ) is Storage_FS

    def test_exists(self):
        with self.file_config as _:
            assert _.exists() is False

    def test_file_name(self):
        with self.file_config as _:
            assert _.file_fs__name().config() == f'{_.file_id()}.config'

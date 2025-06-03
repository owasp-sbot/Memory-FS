from unittest                                           import TestCase
from memory_fs.file.actions.Memory_FS__File__Config     import Memory_FS__File__Config
from memory_fs.schemas.Schema__Memory_FS__File__Config  import Schema__Memory_FS__File__Config
from memory_fs.storage.Memory_FS__Storage               import Memory_FS__Storage

class test_Memory_FS__File__Config(TestCase):

    @classmethod
    def setUpClass(cls):
        cls.file_config = Memory_FS__File__Config()

    def test__init__(self):
        with self.file_config as _:
            assert type(_             ) is Memory_FS__File__Config
            assert type(_.file__config)  is Schema__Memory_FS__File__Config
            assert type(_.storage     ) is Memory_FS__Storage

    def test_exists(self):
        with self.file_config as _:
            assert _.exists() is False

    def test_file_name(self):
        with self.file_config as _:
            assert _.file_name() == f'{_.file_id()}.config'

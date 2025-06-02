from unittest                                           import TestCase

from osbot_utils.helpers.safe_str.Safe_Str__File__Name import Safe_Str__File__Name

from osbot_utils.helpers.safe_str.Safe_Str__File__Path  import Safe_Str__File__Path
from memory_fs.actions.Memory_FS__File_Name             import Memory_FS__File_Name, FILE_EXTENSION__MEMORY_FS__FILE__CONFIG
from memory_fs.schemas.Schema__Memory_FS__File__Config  import Schema__Memory_FS__File__Config


class test_Memory_FS__File_Name(TestCase):

    @classmethod
    def setUpClass(cls):
        cls.file_config = Schema__Memory_FS__File__Config()
        cls.file_name   = Memory_FS__File_Name(file__config=cls.file_config)

    def test__init__(self):
        with self.file_name as _:
            assert type(_) is Memory_FS__File_Name
            assert _.file__config == self.file_config

    def test_config(self):
        with self.file_name as _:
            config_file_name = _.config()
            assert type(config_file_name)   is Safe_Str__File__Name
            assert config_file_name         == f'{self.file_config.file_id}.None.{FILE_EXTENSION__MEMORY_FS__FILE__CONFIG}'
            assert config_file_name         == f'{self.file_config.file_id}.None.fs.json'       # BUG: should just be .config

    def test_content(self):
        with self.file_name as _:
            config_file_name = _.content()
            assert type(config_file_name)   is Safe_Str__File__Name
            assert config_file_name         == f'{self.file_config.file_id}.None'
from unittest                                           import TestCase
from osbot_utils.helpers.safe_str.Safe_Str__File__Name  import Safe_Str__File__Name
from memory_fs.file_fs.actions.File_FS__Name            import File_FS__Name, FILE_EXTENSION__MEMORY_FS__FILE__CONFIG, FILE_EXTENSION__MEMORY_FS__FILE__METADATA
from memory_fs.schemas.Schema__Memory_FS__File__Config  import Schema__Memory_FS__File__Config

# todo: see if we still need these tests, or if they are already covered by the File_FS__Name tests
class test_Memory_FS__File_Name(TestCase):

    @classmethod
    def setUpClass(cls):
        cls.file_config = Schema__Memory_FS__File__Config()
        cls.file_name   = File_FS__Name(file__config=cls.file_config)

    def test__init__(self):
        with self.file_name as _:
            assert type(_) is File_FS__Name
            assert _.file__config == self.file_config

    def test_config(self):
        with self.file_name as _:
            config_file_name = _.config()
            assert type(config_file_name)   is Safe_Str__File__Name
            assert config_file_name         == f'{self.file_config.file_id}.{FILE_EXTENSION__MEMORY_FS__FILE__CONFIG}'
            assert config_file_name         == f'{self.file_config.file_id}.config'

    def test_content(self):
        with self.file_name as _:
            config_file_name = _.content()
            assert type(config_file_name)   is Safe_Str__File__Name
            assert config_file_name         == f'{self.file_config.file_id}'

    def test_metadata(self):
        with self.file_name as _:
            config_file_name = _.metadata()
            assert type(config_file_name)   is Safe_Str__File__Name
            assert config_file_name         == f'{self.file_config.file_id}.{FILE_EXTENSION__MEMORY_FS__FILE__METADATA}'
            assert config_file_name         == f'{self.file_config.file_id}.metadata'

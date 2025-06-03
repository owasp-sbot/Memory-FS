from unittest                                          import TestCase
from memory_fs.actions.Memory_FS__File_Name            import FILE_EXTENSION__MEMORY_FS__FILE__CONFIG
from osbot_utils.helpers.safe_str.Safe_Str__File__Path import Safe_Str__File__Path

from osbot_utils.utils.Dev import pprint

from memory_fs.file.Memory_FS__File import Memory_FS__File

class test_Memory_FS__File__Data(TestCase):

    @classmethod
    def setUpClass(cls):
        cls.file        = Memory_FS__File()
        cls.file_config = cls.file.file_config
        cls.file_id   = cls.file_config.file_id
        cls.file_edit   = cls.file.edit()
        cls.file_data   = cls.file.data()

    def test_load__content(self):
        with self.file_edit as _:
            content = b'this is some content'
            result  = _.save__content(content)
            assert result == [f'{self.file_id}']
            assert _.load__content() == content

    def test_load__paths(self):
        with self.file_data as _:
            paths = _.paths()
            assert paths == [Safe_Str__File__Path(f'{self.file_config.file_id}.{FILE_EXTENSION__MEMORY_FS__FILE__CONFIG}')]  # BUG: this should be
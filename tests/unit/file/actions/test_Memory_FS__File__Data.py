from unittest                       import TestCase
from memory_fs.file.Memory_FS__File import Memory_FS__File

class test_Memory_FS__File__Data(TestCase):

    @classmethod
    def setUpClass(cls):
        cls.file        = Memory_FS__File()
        cls.file_config = cls.file.file_config
        cls.file_name   = cls.file_config.file_name
        cls.file_edit   = cls.file.edit()
        cls.file_data   = cls.file.data()

    def test_load__content(self):
        with self.file_edit as _:
            content = b'this is some content'
            result  = _.save__content(content)
            assert result == [f'{self.file_name}.None']
            assert _.load__content() == content
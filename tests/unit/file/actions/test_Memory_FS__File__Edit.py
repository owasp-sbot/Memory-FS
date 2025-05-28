from unittest                                       import TestCase
from memory_fs.actions.Memory_FS__Edit              import Memory_FS__Edit
from memory_fs.file.Memory_FS__File                 import Memory_FS__File
from memory_fs.file.actions.Memory_FS__File__Edit   import Memory_FS__File__Edit

class test_Memory_FS__File__Edit(TestCase):

    @classmethod
    def setUpClass(cls):
        cls.file        = Memory_FS__File()
        cls.file_config = cls.file.file_config
        cls.file_name   = cls.file_config.file_name
        cls.file_edit   = cls.file.edit()

    def test__init__(self):
        with self.file_edit as _:
            assert type(_               ) is Memory_FS__File__Edit
            assert type(_.storage_edit()) is Memory_FS__Edit

    def test_save__content(self):
        with self.file_edit as _:
            content = b'this is some content'
            result  = _.save__content(content)
            assert result == [f'{self.file_name}.None']
            assert _.load__content() == content


    def test__bug__save__is_not_handling_null_extensions(self):
        with self.file_edit as _:
            assert _.save__content(b'') == [f'{self.file_name}.None']  # BUG but we are not handling ok when file_type.file_extension is not set

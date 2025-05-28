from unittest import TestCase

from osbot_utils.utils.Dev import pprint

from memory_fs.actions.Memory_FS__Edit import Memory_FS__Edit
from memory_fs.file.Memory_FS__File import Memory_FS__File
from memory_fs.file.actions.Memory_FS__File__Edit import Memory_FS__File__Edit


class test_Memory_FS__File__Edit(TestCase):

    @classmethod
    def setUpClass(cls):
        cls.file      = Memory_FS__File()
        cls.file_edit = cls.file.edit()

    def test__init__(self):
        with self.file_edit as _:
            assert type(_               ) is Memory_FS__File__Edit
            assert type(_.storage_edit()) is Memory_FS__Edit

    def test_save(self):
        with self.file_edit as _:
            content = b'this is some content'
            result = _.save(content)
            #pprint(result)             # todo:

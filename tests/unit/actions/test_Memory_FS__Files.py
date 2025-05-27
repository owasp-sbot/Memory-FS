from unittest import TestCase

from osbot_utils.utils.Dev import pprint

from memory_fs.Memory_FS import Memory_FS
from memory_fs.actions.Memory_FS__Files import Memory_FS__Files


class test_Memory_FS__Files(TestCase):
    @classmethod
    def setUpClass(cls):
        cls.memory_fs        = Memory_FS()
        cls.memory_fs__files = cls.memory_fs.files()

    def test__init__(self):
        with self.memory_fs__files as _:
            assert type(_) is Memory_FS__Files

    def test_txt(self):
        file_name = 'an-text-file'
        with self.memory_fs__files.txt(file_name=file_name) as _:
            #pprint(_.obj())
            pass
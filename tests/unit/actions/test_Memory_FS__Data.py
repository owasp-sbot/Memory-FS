from unittest                           import TestCase
from memory_fs.Memory_FS                import Memory_FS
from memory_fs.actions.Memory_FS__Data  import Memory_FS__Data
from memory_fs.actions.Memory_FS__Edit  import Memory_FS__Edit


class test_Memory_FS__Data(TestCase):

    @classmethod
    def setUpClass(cls):
        cls.memory_fs = Memory_FS()
        cls.data      = cls.memory_fs.data()
        cls.edit      = cls.memory_fs.edit()

    def test__init__(self):
        assert type(self.data) is Memory_FS__Data
        assert type(self.edit) is Memory_FS__Edit
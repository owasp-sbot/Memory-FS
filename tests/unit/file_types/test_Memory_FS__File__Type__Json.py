from unittest                                         import TestCase
from memory_fs.file_types.Memory_FS__File__Type__Json import Memory_FS__File__Type__Json


class test_Memory_FS__File__Type__Json(TestCase):

    def test__init__(self):
        with Memory_FS__File__Type__Json() as _:
            assert type(_) is Memory_FS__File__Type__Json
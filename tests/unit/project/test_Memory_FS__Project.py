from unittest import TestCase

from memory_fs.storage.Memory_FS__Storage import Memory_FS__Storage
from osbot_utils.utils.Objects import __, type_full_name

from memory_fs.project.Memory_FS__Project import Memory_FS__Project


class test_Memory_FS__Project(TestCase):

    @classmethod
    def setUpClass(cls):
        cls.project = Memory_FS__Project()

    def test__init__(self):
        with self.project as _:
            assert type(_) is Memory_FS__Project
            assert _.obj() == __(config=__(storage       = type_full_name(Memory_FS__Storage),
                                           path_handlers = [],
                                           name          = None))
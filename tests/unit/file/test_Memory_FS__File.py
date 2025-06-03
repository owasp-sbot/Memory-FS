from unittest                                     import TestCase
from memory_fs.file.storage_fs.Storage_FS__Memory import Storage_FS__Memory
from osbot_utils.utils.Objects                    import __
from memory_fs.file.Memory_FS__File               import Memory_FS__File


class test_Memory_FS__File(TestCase):

    @classmethod
    def setUpClass(cls):
        cls.storage_fs              = Storage_FS__Memory()
        cls.file                    = Memory_FS__File()
        cls.file.storage.storage_fs = cls.storage_fs

    def test__init__(self):
        with self.file as _:
            assert type(_) is Memory_FS__File
            assert _.obj() == __(file_config =__(file_id       = _.file_config.file_id,
                                                   file_paths      = [],
                                                   file_type       = __(name          = None,
                                                                       content_type   = None,
                                                                       file_extension = None,
                                                                       encoding       = None,
                                                                       serialization  = None)),

                                 storage     =  __(storage_type = 'memory'                         ,
                                                   file_system  = __(files=__(), content_data=__()),
                                                   storage_fs   =  __(content_data=__())                            ))

    def test_create(self):
        with self.file as _:
            assert _.create() is not True                    # BUG: Should be true
            assert _.exists() is     False                   # BUG: Should be false

    def test_exists(self):
        with self.file as _:
            assert _.exists() is False

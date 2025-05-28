from unittest                       import TestCase
from osbot_utils.utils.Objects      import __
from memory_fs.file.Memory_FS__File import Memory_FS__File


class test_Memory_FS__File(TestCase):

    @classmethod
    def setUpClass(cls):
        cls.file = Memory_FS__File()

    def test__init__(self):
        with self.file as _:
            assert type(_) is Memory_FS__File
            assert _.obj() == __(file_config   =__(file_id         = _.file_config.file_id,
                                                   file_name       = None,
                                                   file_paths      = []  ,
                                                   file_type       = __(name          = None,
                                                                       content_type   = None,
                                                                       file_extension = None,
                                                                       encoding       = None,
                                                                       serialization  = None)),

                                 storage=__(storage_type='memory',
                                            file_system=__(files=__(), content_data=__())))

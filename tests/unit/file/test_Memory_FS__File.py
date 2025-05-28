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
            assert _.obj() == __(file     = __(config   =__(content_path    = None,
                                                            default_handler = None,
                                                            file_type       = __(name           = None,
                                                                                 content_type   = None,
                                                                                 file_extension = None,
                                                                                 encoding       = None,
                                                                                 serialization  = None),
                                                            file_name       = None,
                                                            file_paths      = []  ,
                                                            path_handlers   = []  ,
                                                            tags            = []  ),
                                               file_id  = _.file.file_id   ,
                                               metadata = __(content_hash          = None ,
                                                             chain_hash            = None ,
                                                             previous_version_path = None ,
                                                             paths                 = __() ,
                                                             content_paths         = __() ,
                                                             size                  = 0    ,
                                                             timestamp             = _.file.metadata.timestamp )))

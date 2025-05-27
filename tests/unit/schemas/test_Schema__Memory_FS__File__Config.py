from unittest                                         import TestCase
from osbot_utils.utils.Objects                        import __
from memory_fs.schemas.Schema__Memory_FS__File__Config import Schema__Memory_FS__File__Config


class test_Schema__Memory_FS__File__Config(TestCase):

    def test__init__(self):
        with Schema__Memory_FS__File__Config() as _:
            assert type(_) is Schema__Memory_FS__File__Config
            assert _.obj() ==__(default_handler = None ,
                                file_type       = None ,
                                path_handlers   = []   ,
                                tags            = []   )
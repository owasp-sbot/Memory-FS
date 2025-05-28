from unittest                                              import TestCase
from osbot_utils.utils.Objects                             import __
from memory_fs.schemas.Schema__Memory_FS__File__Metadata   import Schema__Memory_FS__File__Metadata


class test_Schema__Memory_FS__File__Metadata(TestCase):

    def test__init__(self):
        with Schema__Memory_FS__File__Metadata() as _:
            assert type(_) is Schema__Memory_FS__File__Metadata
            assert _.obj() == __(content__hash         = None       ,
                                 content__size         = 0          ,
                                 chain_hash            = None       ,
                                 previous_version_path = None       ,
                                 tags                  = []         ,
                                 timestamp             = _.timestamp)


from unittest                                               import TestCase
from osbot_utils.utils.Objects                              import __
from memory_fs.schemas.Schema__Memory_FS__File              import Schema__Memory_FS__File
from memory_fs.schemas.Schema__Memory_FS__File__Config      import Schema__Memory_FS__File__Config
from memory_fs.schemas.Schema__Memory_FS__File__Metadata    import Schema__Memory_FS__File__Metadata


class test_Schema__Memory_FS__File(TestCase):                                          # Test file schema

    def test__init__(self):                                                             # Test initialization
        config   = Schema__Memory_FS__File__Config()
        metadata = Schema__Memory_FS__File__Metadata()

        with Schema__Memory_FS__File(config   = config   ,
                                     metadata = metadata ) as _:
            assert type(_)          is Schema__Memory_FS__File
            assert type(_.config)   is Schema__Memory_FS__File__Config
            assert type(_.metadata) is Schema__Memory_FS__File__Metadata
            assert _.config         is config
            assert _.metadata       is metadata

    def test__default_values(self):                                                     # Test default initialization
        with Schema__Memory_FS__File() as _:
            assert type(_.config)   is Schema__Memory_FS__File__Config
            assert type(_.metadata) is Schema__Memory_FS__File__Metadata
            assert _.obj()          == __(config=__( file_id         = _.config.file_id ,
                                                     exists_strategy = 'first'          ,
                                                     file_paths      = []               ,
                                                     file_type       = __(name           = None,
                                                                          content_type   = None,
                                                                          file_extension = None,
                                                                          encoding       = None,
                                                                          serialization  =None)),
                                           metadata=__(content__hash         = None                 ,
                                                       chain_hash            = None                 ,
                                                       data                  = __()                 ,
                                                       previous_version_path = None                 ,
                                                       content__size         = 0                    ,
                                                       tags                  = []                   ,
                                                       timestamp             = _.metadata.timestamp))

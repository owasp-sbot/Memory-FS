from unittest                                        import TestCase
from osbot_utils.utils.Objects                       import __
from memory_fs.file.Memory_FS__File__Storage         import Schema__Memory_FS__File__Storage__Config, Memory_FS__File__Storage
from memory_fs.path_handlers.Path__Handler__Latest   import Path__Handler__Latest
from memory_fs.path_handlers.Path__Handler__Temporal import Path__Handler__Temporal
from memory_fs.Memory_FS                             import Memory_FS
from memory_fs.actions.Memory_FS__File__New          import Memory_FS__File__New
from osbot_utils.utils.Dev                           import pprint


class test_Memory_FS__File__New(TestCase):
    @classmethod
    def setUpClass(cls):
        cls.memory_fs            = Memory_FS()
        cls.path_handlers        = [Path__Handler__Latest, Path__Handler__Temporal]
        cls.file_storage__config = Schema__Memory_FS__File__Storage__Config(path_handlers = cls.path_handlers       )
        cls.file_storage         = Memory_FS__File__Storage                (config        = cls.file_storage__config)
        cls.memory_fs__new     = cls.memory_fs.new                     (file_storage  = cls.file_storage)
        cls.path_now             = Path__Handler__Temporal().path_now()

    def test__init__(self):
        with self.memory_fs__new as _:
            assert type(_) is Memory_FS__File__New

    def test_txt(self):
        file_name = 'an-text-file'
        with self.memory_fs__new.txt(file_name=file_name) as _:
            assert _.obj() == __(file=__(config  =__(content_path    = None                         ,
                                                     default_handler = None                         ,
                                                     file_name       = 'an-text-file'               ,
                                                     path_handlers   = []                           ,
                                                     file_type       = __(name           = 'text'   ,
                                                                          content_type   = 'TXT'    ,
                                                                          file_extension = 'txt'    ,
                                                                          encoding       = 'UTF_8'  ,
                                                                          serialization  = 'STRING' ),
                                                     file_paths=['latest', self.path_now],
                                                     tags=[]),
                                         file_id  = _.file.file_id,
                                         metadata = __(content_hash          = None                 ,
                                                       chain_hash            = None                 ,
                                                       previous_version_path = None                 ,
                                                       paths                 = __()                 ,
                                                       content_paths         = __()                 ,
                                                       size                  = 0                    ,
                                                       timestamp             =_.file.metadata.timestamp)))
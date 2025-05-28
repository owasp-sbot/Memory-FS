from typing                                             import Type
from unittest                                           import TestCase
from memory_fs.path_handlers                            import Path__Handler__Latest
from memory_fs.path_handlers.Path__Handler__Temporal    import Path__Handler__Temporal
from memory_fs.schemas.Schema__Memory_FS__Path__Handler import Schema__Memory_FS__Path__Handler
from osbot_utils.type_safe.Type_Safe__List              import Type_Safe__List
from osbot_utils.utils.Objects                          import __, type_full_name
from memory_fs.file.actions.Memory_FS__File__Storage    import Memory_FS__File__Storage, Schema__Memory_FS__File__Storage__Config


class test_Memory_FS__File__Storage(TestCase):

    @classmethod
    def setUpClass(cls):
        cls.path_handlers = [Path__Handler__Latest, Path__Handler__Temporal]
        cls.file_storage__config = Schema__Memory_FS__File__Storage__Config(path_handlers=cls.path_handlers)
        cls.file_storage  = Memory_FS__File__Storage(config=cls.file_storage__config)

    def test___init__(self):
        with self.file_storage as _:
            assert type(_)                              is Memory_FS__File__Storage
            assert _.obj()                              == __(config=__(path_handlers=[type_full_name(Path__Handler__Latest   ),
                                                                                       type_full_name(Path__Handler__Temporal)],))
            assert type(_.config.path_handlers)         is Type_Safe__List
            assert _.config.path_handlers.expected_type == Type[Schema__Memory_FS__Path__Handler]
            assert _.config.path_handlers               == [Path__Handler__Latest, Path__Handler__Temporal]

    def test_file__paths(self):
        with self.file_storage as _:
            file_paths = _.file__paths()
            assert len(file_paths) > 0
            #pprint(file_paths)

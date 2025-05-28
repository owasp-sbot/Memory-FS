from typing                                             import Type
from unittest                                           import TestCase
from osbot_utils.helpers.safe_str.Safe_Str__File__Path import Safe_Str__File__Path
from memory_fs.path_handlers.Path__Handler import Path__Handler
from memory_fs.path_handlers.Path__Handler__Latest      import Path__Handler__Latest
from memory_fs.path_handlers.Path__Handler__Temporal    import Path__Handler__Temporal
from osbot_utils.type_safe.Type_Safe__List              import Type_Safe__List
from osbot_utils.utils.Objects                          import __, type_full_name
from memory_fs.file.Memory_FS__File__Storage    import Memory_FS__File__Storage, Schema__Memory_FS__File__Storage__Config
from osbot_utils.utils.Dev import pprint

class test_Memory_FS__File__Storage(TestCase):

    @classmethod
    def setUpClass(cls):
        cls.path_handlers        = [Path__Handler__Latest, Path__Handler__Temporal]
        cls.file_storage__config = Schema__Memory_FS__File__Storage__Config(path_handlers=cls.path_handlers)
        cls.file_storage         = Memory_FS__File__Storage(config=cls.file_storage__config)
        cls.path_now             = Path__Handler__Temporal().path_now()

    def test___init__(self):
        with self.file_storage as _:
            assert type(_)                              is Memory_FS__File__Storage
            assert _.obj()                              == __(config=__(path_handlers=[type_full_name(Path__Handler__Latest   ),
                                                                                       type_full_name(Path__Handler__Temporal)],))
            assert type(_.config.path_handlers)         is Type_Safe__List
            assert _.config.path_handlers.expected_type == Type[Path__Handler]
            assert _.config.path_handlers               == [Path__Handler__Latest, Path__Handler__Temporal]

    def test_file__paths(self):
        with self.file_storage as _:
            file_paths = _.file__paths()
            assert file_paths == ['latest', self.path_now]
            assert file_paths == [Safe_Str__File__Path('latest'), Safe_Str__File__Path(self.path_now)]

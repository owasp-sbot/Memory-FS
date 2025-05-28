from unittest                                               import TestCase

from memory_fs.file.Memory_FS__File import Memory_FS__File
from memory_fs.file_types.Memory_FS__File__Type__Text       import Memory_FS__File__Type__Text
from osbot_utils.helpers.Safe_Id                            import Safe_Id
from memory_fs.path_handlers.Path__Handler__Latest          import Path__Handler__Latest
from memory_fs.path_handlers.Path__Handler__Temporal        import Path__Handler__Temporal
from memory_fs.project.Schema__Memory_FS__Project__Config   import Schema__Memory_FS__Project__Path_Strategy, Schema__Memory_FS__Project__Config
from memory_fs.Memory_FS                                    import Memory_FS
from memory_fs.storage.Memory_FS__Storage                   import Memory_FS__Storage
from osbot_utils.utils.Objects                              import __, type_full_name
from memory_fs.project.Memory_FS__Project import Memory_FS__Project


class test_Memory_FS__Project(TestCase):

    @classmethod
    def setUpClass(cls):
        cls.path_handlers       = [Path__Handler__Latest, Path__Handler__Temporal]
        cls.path_strategy_name  = Safe_Id('latest-temporal')
        cls.project_name        = 'test-project'
        cls.path_strategy       = Schema__Memory_FS__Project__Path_Strategy(name   = cls.path_strategy_name, path_handlers   = cls.path_handlers  )
        cls.path_strategies     = { cls.path_strategy_name: cls.path_strategy}
        cls.project_config      = Schema__Memory_FS__Project__Config       (name   = cls.project_name      , path_strategies = cls.path_strategies)
        cls.project             = Memory_FS__Project                       (config = cls.project_config                                           )

    def test__init__(self):
        with self.project as _:
            assert type(_) is Memory_FS__Project

            assert _.json() == {'config': {'name'           : 'test-project',
                                           'path_strategies': { Safe_Id('latest-temporal'): { 'name'         : 'latest-temporal'                                                           ,
                                                                                             'path_handlers': ['memory_fs.path_handlers.Path__Handler__Latest.Path__Handler__Latest'      ,
                                                                                                               'memory_fs.path_handlers.Path__Handler__Temporal.Path__Handler__Temporal']}},
                                           'storage'        : 'memory_fs.storage.Memory_FS__Storage.Memory_FS__Storage'}}



    def test_file(self):
        with self.project as _:
            kwargs = dict(file_name     = "an-file"                              ,
                          path_strategy = _.path_strategy(self.path_strategy_name),
                          file_type     = Memory_FS__File__Type__Text()          )
            file = _.file(**kwargs)
            assert type(file) is Memory_FS__File

    def test_memory_fs(self):
        with self.project.memory_fs() as _:
            assert type(_)         is Memory_FS
            assert type(_.storage) == Memory_FS__Storage
            #_.print()

    def test_path_strategies(self):
        with self.project as _:
            assert _.path_strategy(self.path_strategy_name) == self.path_strategy
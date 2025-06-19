from unittest                                               import TestCase
from osbot_utils.utils.Objects                              import __
from memory_fs.file_fs.File_FS                              import File_FS
from memory_fs.file_types.Memory_FS__File__Type__Text       import Memory_FS__File__Type__Text
from osbot_utils.helpers.Safe_Id                            import Safe_Id
from memory_fs.path_handlers.Path__Handler__Latest          import Path__Handler__Latest
from memory_fs.path_handlers.Path__Handler__Temporal        import Path__Handler__Temporal
from memory_fs.project.Schema__Memory_FS__Project__Config   import Schema__Memory_FS__Project__Path_Strategy, Schema__Memory_FS__Project__Config
from memory_fs.storage.Memory_FS__Storage                   import Memory_FS__Storage
from memory_fs.project.Memory_FS__Project                   import Memory_FS__Project


class test_Memory_FS__Project(TestCase):                                                # Test memory FS project

    @classmethod
    def setUpClass(cls):                                                                # Setup test data
        cls.path_handlers       = [Path__Handler__Latest, Path__Handler__Temporal]
        cls.path_strategy_name  = Safe_Id('latest-temporal')
        cls.project_name        = Safe_Id('test-project')
        cls.path_strategy       = Schema__Memory_FS__Project__Path_Strategy(name          = cls.path_strategy_name ,
                                                                           path_handlers = cls.path_handlers     )
        cls.path_strategies     = {cls.path_strategy_name: cls.path_strategy}
        cls.project_config      = Schema__Memory_FS__Project__Config(name            = cls.project_name  ,
                                                                     path_strategies = cls.path_strategies)
        cls.project             = Memory_FS__Project(config = cls.project_config)
        cls.path_now            = Path__Handler__Temporal().path_now()

    def test__init__(self):                                                             # Test initialization
        with self.project as _:
            assert type(_) is Memory_FS__Project

            expected_json = {'config': {'name'           : 'test-project',
                                       'path_strategies': {Safe_Id('latest-temporal'): {'name'         : 'latest-temporal'                                                         ,
                                                                                        'path_handlers': ['memory_fs.path_handlers.Path__Handler__Latest.Path__Handler__Latest'    ,
                                                                                                          'memory_fs.path_handlers.Path__Handler__Temporal.Path__Handler__Temporal']}},
                                       'storage'        : 'memory_fs.storage.Memory_FS__Storage.Memory_FS__Storage'},
                             'storage': {'storage_fs': {}, 'storage_type': 'memory'}}
            assert _.json() == expected_json

    def test_file(self):                                                                # Test file creation
        with self.project as _:
            file = _.file(file_id      = Safe_Id("an-file")                   ,
                          path_strategy = _.path_strategy(self.path_strategy_name),
                          file_type     = Memory_FS__File__Type__Text()          )

            assert type(file) is File_FS
            assert file.obj() == __(file_config = __(exists_strategy = 'FIRST'            ,
                                                     file_id         = 'an-file'          ,
                                                     file_paths      = ['latest', self.path_now],
                                                     file_type       = __(name           = 'text'  ,
                                                                          content_type   = 'TXT'    ,
                                                                          file_extension = 'txt'    ,
                                                                          encoding       = 'UTF_8'  ,
                                                                          serialization  = 'STRING' )),
                                    storage    = __(storage_type = 'memory'                       ,
                                                    storage_fs   = __()                            ))


    def test_path_strategy(self):                                                       # Test path strategy retrieval
        with self.project as _:
            strategy = _.path_strategy(self.path_strategy_name)
            assert strategy == self.path_strategy

    def test_path_strategy_not_found(self):                                             # Test invalid path strategy
        with self.project as _:
            strategy = _.path_strategy(Safe_Id('non-existent'))
            assert strategy is None
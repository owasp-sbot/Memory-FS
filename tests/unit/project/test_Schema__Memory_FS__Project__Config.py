from unittest                                               import TestCase
from memory_fs.storage.Memory_FS__Storage                   import Memory_FS__Storage
from osbot_utils.helpers.Safe_Id                            import Safe_Id
from memory_fs.path_handlers.Path__Handler__Latest          import Path__Handler__Latest
from memory_fs.project.Schema__Memory_FS__Project__Config   import Schema__Memory_FS__Project__Path_Strategy, Schema__Memory_FS__Project__Config


class test_Schema__Memory_FS__Project__Config(TestCase):                               # Test project configuration schemas

    def test_Schema__Memory_FS__Project__Path_Strategy(self):                          # Test path strategy schema
        path_handlers = [Path__Handler__Latest]
        strategy      = Schema__Memory_FS__Project__Path_Strategy(name          = Safe_Id('test-strategy') ,
                                                                  path_handlers = path_handlers            )

        with strategy as _:
            assert type(_)          is Schema__Memory_FS__Project__Path_Strategy
            assert _.name           == Safe_Id('test-strategy')
            assert _.path_handlers  == path_handlers

    def test_Schema__Memory_FS__Project__Path_Strategy_defaults(self):                  # Test path strategy defaults
        strategy = Schema__Memory_FS__Project__Path_Strategy()

        with strategy as _:
            assert _.name          is None
            assert _.path_handlers == []

    def test_Schema__Memory_FS__Project__Config(self):                                 # Test project config schema
        path_strategy   = Schema__Memory_FS__Project__Path_Strategy(name = Safe_Id('strategy1'))
        path_strategies = {Safe_Id('strategy1'): path_strategy}

        config = Schema__Memory_FS__Project__Config(storage         = Memory_FS__Storage   ,
                                                    path_strategies = path_strategies      ,
                                                    name            = Safe_Id('my-project'))

        with config as _:
            assert type(_)           is Schema__Memory_FS__Project__Config
            assert _.storage         == Memory_FS__Storage
            assert _.path_strategies == path_strategies
            assert _.name            == Safe_Id('my-project')

    def test_Schema__Memory_FS__Project__Config_defaults(self):                        # Test project config defaults
        config = Schema__Memory_FS__Project__Config(storage         = Memory_FS__Storage ,
                                                    path_strategies = {}                 )

        with config as _:
            assert _.storage         == Memory_FS__Storage
            assert _.path_strategies == {}
            assert _.name            is None
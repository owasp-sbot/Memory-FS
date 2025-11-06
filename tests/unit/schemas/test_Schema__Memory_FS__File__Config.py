from unittest                                                                       import TestCase
from osbot_utils.testing.__                                                         import __
from memory_fs.schemas.Schema__Memory_FS__File__Config                              import Schema__Memory_FS__File__Config
from memory_fs.schemas.Enum__Memory_FS__File__Exists_Strategy                       import Enum__Memory_FS__File__Exists_Strategy
from osbot_utils.type_safe.primitives.domains.identifiers.safe_str.Safe_Str__Id     import Safe_Str__Id
from osbot_utils.type_safe.primitives.domains.files.safe_str.Safe_Str__File__Path   import Safe_Str__File__Path


class test_Schema__Memory_FS__File__Config(TestCase):                                  # Test file config schema

    def test__init__(self):                                                             # Test initialization with defaults
        with Schema__Memory_FS__File__Config() as _:
            assert type(_) is Schema__Memory_FS__File__Config
            assert _.obj() == __(exists_strategy = 'first'      ,
                                 file_id         = _.file_id    ,
                                 file_key        = ''           ,
                                 file_paths      = []           ,
                                 file_type       = __(name           = None ,
                                                      content_type   = None ,
                                                      file_extension = None ,
                                                      encoding       = None ,
                                                      serialization  = None ))

    def test__with_values(self):                                                        # Test initialization with values
        from memory_fs.file_types.Memory_FS__File__Type__Json import Memory_FS__File__Type__Json

        file_id    = Safe_Str__Id('my-file')
        file_paths = [Safe_Str__File__Path('path1'), Safe_Str__File__Path('path2')]
        file_type  = Memory_FS__File__Type__Json()

        config = Schema__Memory_FS__File__Config(file_id    = file_id    ,
                                                 file_paths = file_paths ,
                                                 file_type  = file_type  )

        with config as _:
            assert _.file_id          == file_id
            assert _.file_paths       == file_paths
            assert _.file_type        == file_type
            assert _.exists_strategy  == Enum__Memory_FS__File__Exists_Strategy.FIRST

    def test__file_id_generation(self):                                                # Test random file_id generation
        config1 = Schema__Memory_FS__File__Config()
        config2 = Schema__Memory_FS__File__Config()

        assert config1.file_id != config2.file_id                                      # Should be different
        assert config1.file_id.startswith('file-id')
        assert config2.file_id.startswith('file-id')
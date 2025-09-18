from unittest                                                                   import TestCase
from memory_fs.file_types.Memory_FS__File__Type__Data                           import Memory_FS__File__Type__Data
from memory_fs.schemas.Enum__Memory_FS__File__Content_Type                      import Enum__Memory_FS__File__Content_Type
from memory_fs.schemas.Enum__Memory_FS__File__Encoding                          import Enum__Memory_FS__File__Encoding
from memory_fs.schemas.Enum__Memory_FS__Serialization                           import Enum__Memory_FS__Serialization
from osbot_utils.type_safe.primitives.domains.identifiers.safe_str.Safe_Str__Id import Safe_Str__Id
from osbot_utils.type_safe.Type_Safe                                            import Type_Safe


class test_Memory_FS__File__Type__Data(TestCase):                                      # Test Data file type definition

    def test__init__(self):                                                             # Test initialization and attributes
        with Memory_FS__File__Type__Data() as _:
            assert type(_)           is Memory_FS__File__Type__Data
            assert _.name           == Safe_Str__Id('json')                                 # Note: same as JSON type
            assert _.content_type   == Enum__Memory_FS__File__Content_Type.JSON
            assert _.data_type      == type(Type_Safe)
            assert _.file_extension == Safe_Str__Id('json')
            assert _.encoding       == Enum__Memory_FS__File__Encoding.UTF_8
            assert _.serialization  == Enum__Memory_FS__Serialization.JSON
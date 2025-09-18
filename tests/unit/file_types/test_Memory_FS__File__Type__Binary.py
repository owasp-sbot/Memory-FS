from unittest                                                                    import TestCase
from memory_fs.file_types.Memory_FS__File__Type__Binary                          import Memory_FS__File__Type__Binary
from memory_fs.schemas.Enum__Memory_FS__File__Content_Type                       import Enum__Memory_FS__File__Content_Type
from memory_fs.schemas.Enum__Memory_FS__Serialization                            import Enum__Memory_FS__Serialization
from osbot_utils.type_safe.primitives.domains.identifiers.safe_str.Safe_Str__Id  import Safe_Str__Id


class test_Memory_FS__File__Type__Binary(TestCase):                                     # Test binary file type definition

    def test__init__(self):                                                             # Test initialization and attributes
        with Memory_FS__File__Type__Binary() as _:
            assert type(_)           is Memory_FS__File__Type__Binary
            assert _.name           == Safe_Str__Id('binary')
            assert _.content_type   == Enum__Memory_FS__File__Content_Type.BINARY
            assert _.file_extension == Safe_Str__Id('bin')
            assert _.encoding       is None                                             # No encoding for raw binary
            assert _.serialization  == Enum__Memory_FS__Serialization.BINARY
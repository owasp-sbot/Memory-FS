from unittest                                               import TestCase
from memory_fs.file_types.Memory_FS__File__Type__Jpeg       import Memory_FS__File__Type__Jpeg
from memory_fs.schemas.Enum__Memory_FS__File__Content_Type  import Enum__Memory_FS__File__Content_Type
from memory_fs.schemas.Enum__Memory_FS__File__Encoding      import Enum__Memory_FS__File__Encoding
from memory_fs.schemas.Enum__Memory_FS__Serialization       import Enum__Memory_FS__Serialization
from osbot_utils.helpers.Safe_Id                            import Safe_Id


class test_Memory_FS__File__Type__Jpeg(TestCase):                                      # Test JPEG file type definition

    def test__init__(self):                                                             # Test initialization and attributes
        with Memory_FS__File__Type__Jpeg() as _:
            assert type(_)           is Memory_FS__File__Type__Jpeg
            assert _.name           == Safe_Id('jpeg')
            assert _.content_type   == Enum__Memory_FS__File__Content_Type.JPEG
            assert _.file_extension == Safe_Id('jpg')
            assert _.alt_extensions == [Safe_Id('jpeg')]
            assert _.encoding       == Enum__Memory_FS__File__Encoding.BINARY
            assert _.serialization  == Enum__Memory_FS__Serialization.BINARY
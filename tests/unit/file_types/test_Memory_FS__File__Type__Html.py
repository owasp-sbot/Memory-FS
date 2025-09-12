from unittest                                               import TestCase
from memory_fs.file_types.Memory_FS__File__Type__Html       import Memory_FS__File__Type__Html
from memory_fs.schemas.Enum__Memory_FS__File__Content_Type  import Enum__Memory_FS__File__Content_Type
from memory_fs.schemas.Enum__Memory_FS__File__Encoding      import Enum__Memory_FS__File__Encoding
from memory_fs.schemas.Enum__Memory_FS__Serialization       import Enum__Memory_FS__Serialization
from osbot_utils.type_safe.primitives.domains.identifiers.Safe_Id                            import Safe_Id

class test_Memory_FS__File__Type__Html(TestCase):                                      # Test HTML file type definition

    def test__init__(self):                                                             # Test initialization and attributes
        with Memory_FS__File__Type__Html() as _:
            assert type(_)           is Memory_FS__File__Type__Html
            assert _.name           == Safe_Id('html')
            assert _.content_type   == Enum__Memory_FS__File__Content_Type.HTML
            assert _.file_extension == Safe_Id('html')
            assert _.encoding       == Enum__Memory_FS__File__Encoding.UTF_8
            assert _.serialization  == Enum__Memory_FS__Serialization.STRING
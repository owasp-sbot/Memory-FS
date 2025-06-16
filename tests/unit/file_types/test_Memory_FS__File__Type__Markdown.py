from unittest                                               import TestCase
from memory_fs.file_types.Memory_FS__File__Type__Markdown   import Memory_FS__File__Type__Markdown
from memory_fs.schemas.Enum__Memory_FS__File__Content_Type  import Enum__Memory_FS__File__Content_Type
from memory_fs.schemas.Enum__Memory_FS__File__Encoding      import Enum__Memory_FS__File__Encoding
from memory_fs.schemas.Enum__Memory_FS__Serialization       import Enum__Memory_FS__Serialization
from osbot_utils.helpers.Safe_Id                            import Safe_Id


class test_Memory_FS__File__Type__Markdown(TestCase):                                  # Test Markdown file type definition

    def test__init__(self):                                                             # Test initialization and attributes
        with Memory_FS__File__Type__Markdown() as _:
            assert type(_)           is Memory_FS__File__Type__Markdown
            assert _.name           == Safe_Id('markdown')
            assert _.content_type   == Enum__Memory_FS__File__Content_Type.MARKDOWN
            assert _.file_extension == Safe_Id('md')
            assert _.alt_extensions == [Safe_Id('markdown')]
            assert _.encoding       == Enum__Memory_FS__File__Encoding.UTF_8
            assert _.serialization  == Enum__Memory_FS__Serialization.STRING
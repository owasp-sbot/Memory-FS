from unittest                                               import TestCase
from memory_fs.schemas.Schema__Memory_FS__File__Type        import Schema__Memory_FS__File__Type
from memory_fs.schemas.Enum__Memory_FS__File__Content_Type  import Enum__Memory_FS__File__Content_Type
from memory_fs.schemas.Enum__Memory_FS__File__Encoding      import Enum__Memory_FS__File__Encoding
from memory_fs.schemas.Enum__Memory_FS__Serialization       import Enum__Memory_FS__Serialization
from osbot_utils.helpers.Safe_Id                            import Safe_Id


class test_Schema__Memory_FS__File__Type(TestCase):                                    # Test file type schema

    def test__init__(self):                                                             # Test initialization with defaults
        with Schema__Memory_FS__File__Type() as _:
            assert type(_)           is Schema__Memory_FS__File__Type
            assert _.name           is None
            assert _.content_type   is None
            assert _.file_extension is None
            assert _.encoding       is None
            assert _.serialization  is None

    def test__with_values(self):                                                        # Test initialization with values
        file_type = Schema__Memory_FS__File__Type(name           = Safe_Id('custom')                           ,
                                                   content_type   = Enum__Memory_FS__File__Content_Type.JSON   ,
                                                   file_extension = Safe_Id('json')                            ,
                                                   encoding       = Enum__Memory_FS__File__Encoding.UTF_8      ,
                                                   serialization  = Enum__Memory_FS__Serialization.JSON        )

        with file_type as _:
            assert _.name           == Safe_Id('custom')
            assert _.content_type   == Enum__Memory_FS__File__Content_Type.JSON
            assert _.file_extension == Safe_Id('json')
            assert _.encoding       == Enum__Memory_FS__File__Encoding.UTF_8
            assert _.serialization  == Enum__Memory_FS__Serialization.JSON
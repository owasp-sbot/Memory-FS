from unittest                                               import TestCase
from enum                                                   import Enum
from memory_fs.schemas.Enum__Memory_FS__File__Content_Type  import Enum__Memory_FS__File__Content_Type


class test_Enum__Memory_FS__File__Content_Type(TestCase):                              # Test content type enumeration

    def test__enum_type(self):                                                         # Test it's an enum
        assert issubclass(Enum__Memory_FS__File__Content_Type, Enum)

    def test__enum_values(self):                                                        # Test enum values
        assert Enum__Memory_FS__File__Content_Type.HTML.value      == 'text/html; charset=utf-8'
        assert Enum__Memory_FS__File__Content_Type.JSON.value      == 'application/json; charset=utf-8'
        assert Enum__Memory_FS__File__Content_Type.JPEG.value      == 'image/jpeg'
        assert Enum__Memory_FS__File__Content_Type.MARKDOWN.value  == 'text/markdown; charset=utf-8'
        assert Enum__Memory_FS__File__Content_Type.DOT.value       == 'text/vnd.graphviz; charset=utf-8'
        assert Enum__Memory_FS__File__Content_Type.PNG.value       == 'image/png'
        assert Enum__Memory_FS__File__Content_Type.TXT.value       == 'text/plain; charset=utf-8'

    def test__enum_members(self):                                                       # Test all members present
        expected_members = ['BINARY', 'HTML', 'GZIP', 'JSON', 'JPEG', 'MARKDOWN', 'DOT', 'PNG', 'TXT','ZIP']
        actual_members   = [member.name for member in Enum__Memory_FS__File__Content_Type]
        assert actual_members == expected_members
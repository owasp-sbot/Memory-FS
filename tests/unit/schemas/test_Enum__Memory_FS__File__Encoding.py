from unittest                                               import TestCase
from enum                                                   import Enum
from memory_fs.schemas.Enum__Memory_FS__File__Encoding      import Enum__Memory_FS__File__Encoding


class test_Enum__Memory_FS__File__Encoding(TestCase):                                  # Test file encoding enumeration

    def test__enum_type(self):                                                         # Test it's an enum
        assert issubclass(Enum__Memory_FS__File__Encoding, Enum)

    def test__enum_values(self):                                                        # Test enum values
        assert Enum__Memory_FS__File__Encoding.UTF_8.value        == "utf-8"
        assert Enum__Memory_FS__File__Encoding.UTF_16.value       == "utf-16"
        assert Enum__Memory_FS__File__Encoding.UTF_16_BE.value    == "utf-16-be"
        assert Enum__Memory_FS__File__Encoding.UTF_16_LE.value    == "utf-16-le"
        assert Enum__Memory_FS__File__Encoding.UTF_32.value       == "utf-32"
        assert Enum__Memory_FS__File__Encoding.ASCII.value        == "ascii"
        assert Enum__Memory_FS__File__Encoding.LATIN_1.value      == "latin-1"
        assert Enum__Memory_FS__File__Encoding.WINDOWS_1252.value == "windows-1252"
        assert Enum__Memory_FS__File__Encoding.BINARY.value       is None

    def test__enum_members(self):                                                       # Test all members present
        expected_members = ['UTF_8', 'UTF_16', 'UTF_16_BE', 'UTF_16_LE', 'UTF_32',
                           'ASCII', 'LATIN_1', 'WINDOWS_1252', 'BINARY']
        actual_members   = [member.name for member in Enum__Memory_FS__File__Encoding]
        assert actual_members == expected_members
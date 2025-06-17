from unittest                                               import TestCase
from enum                                                   import Enum
from memory_fs.schemas.Enum__Memory_FS__Serialization       import Enum__Memory_FS__Serialization


class test_Enum__Memory_FS__Serialization(TestCase):                                   # Test serialization enumeration

    def test__enum_type(self):                                                         # Test it's an enum
        assert issubclass(Enum__Memory_FS__Serialization, Enum)

    def test__enum_values(self):                                                        # Test enum values
        assert Enum__Memory_FS__Serialization.STRING.value    == "string"
        assert Enum__Memory_FS__Serialization.JSON.value      == "json"
        assert Enum__Memory_FS__Serialization.BINARY.value    == "binary"
        assert Enum__Memory_FS__Serialization.BASE64.value    == "base64"
        assert Enum__Memory_FS__Serialization.TYPE_SAFE.value == "type_safe"

    def test__enum_members(self):                                                       # Test all members present
        expected_members = ['STRING', 'JSON', 'BINARY', 'BASE64', 'TYPE_SAFE']
        actual_members   = [member.name for member in Enum__Memory_FS__Serialization]
        assert actual_members == expected_members
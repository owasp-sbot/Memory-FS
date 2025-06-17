from unittest                                                 import TestCase
from enum                                                     import Enum
from memory_fs.schemas.Enum__Memory_FS__File__Exists_Strategy import Enum__Memory_FS__File__Exists_Strategy


class test_Enum__Memory_FS__File__Exists_Strategy(TestCase):                           # Test exists strategy enumeration

    def test__enum_type(self):                                                         # Test it's an enum
        assert issubclass(Enum__Memory_FS__File__Exists_Strategy, Enum)

    def test__enum_values(self):                                                        # Test enum values
        assert Enum__Memory_FS__File__Exists_Strategy.ALL.value   == 'all'
        assert Enum__Memory_FS__File__Exists_Strategy.ANY.value   == 'any'
        assert Enum__Memory_FS__File__Exists_Strategy.FIRST.value == 'first'

    def test__enum_members(self):                                                       # Test all members present
        expected_members = ['ALL', 'ANY', 'FIRST']
        actual_members   = [member.name for member in Enum__Memory_FS__File__Exists_Strategy]
        assert actual_members == expected_members
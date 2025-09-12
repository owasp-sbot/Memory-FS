from unittest                                               import TestCase
from memory_fs.schemas.Schema__Memory_FS__Path__Handler     import Schema__Memory_FS__Path__Handler
from osbot_utils.type_safe.primitives.domains.identifiers.Safe_Id                            import Safe_Id


class test_Schema__Memory_FS__Path__Handler(TestCase):                                 # Test path handler schema

    def test__init__(self):                                                             # Test initialization with defaults
        with Schema__Memory_FS__Path__Handler() as _:
            assert type(_)      is Schema__Memory_FS__Path__Handler
            assert type(_.name) is Safe_Id
            assert _.enabled    is True

    def test__with_values(self):                                                        # Test initialization with values
        handler = Schema__Memory_FS__Path__Handler(name    = Safe_Id('custom-handler') ,
                                                   enabled = False                     )

        with handler as _:
            assert _.name    == Safe_Id('custom-handler')
            assert _.enabled is False
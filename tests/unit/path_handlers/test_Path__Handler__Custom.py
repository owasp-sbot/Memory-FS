from unittest                                               import TestCase
from memory_fs.path_handlers.Path__Handler__Custom          import Path__Handler__Custom
from osbot_utils.type_safe.primitives.domains.identifiers.Safe_Id                            import Safe_Id
from osbot_utils.type_safe.primitives.domains.files.safe_str.Safe_Str__File__Path      import Safe_Str__File__Path


class test_Path__Handler__Custom(TestCase):                                             # Test custom path handler

    def setUp(self):                                                                    # Initialize test data
        self.custom_path = Safe_Str__File__Path("custom/path/location")
        self.handler     = Path__Handler__Custom(custom_path=self.custom_path)

    def test__init__(self):                                                             # Test initialization
        with self.handler as _:
            assert type(_)        is Path__Handler__Custom
            assert _.name         == Safe_Id("custom")
            assert _.custom_path  == self.custom_path

    def test_generate_path(self):                                                       # Test path generation
        with self.handler as _:
            result = _.generate_path()
            assert result == self.custom_path                                           # Always returns custom path

from unittest                                               import TestCase
from memory_fs.path_handlers.Path__Handler__Latest          import Path__Handler__Latest
from osbot_utils.type_safe.primitives.safe_str.identifiers.Safe_Id                            import Safe_Id
from osbot_utils.type_safe.primitives.safe_str.filesystem.Safe_Str__File__Path      import Safe_Str__File__Path


class test_Path__Handler__Latest(TestCase):                                             # Test latest path handler

    def setUp(self):                                                                    # Initialize test data
        self.handler = Path__Handler__Latest()

    def test__init__(self):                                                             # Test initialization
        with self.handler as _:
            assert type(_) is Path__Handler__Latest
            assert _.name  == Safe_Id("latest")

    def test_generate_path(self):                                                       # Test path generation
        with self.handler as _:
            result = _.generate_path()
            assert result         == Safe_Str__File__Path("latest")
            assert type(result)   is Safe_Str__File__Path
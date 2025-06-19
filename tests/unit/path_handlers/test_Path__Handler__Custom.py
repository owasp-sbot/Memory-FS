from unittest                                               import TestCase
from memory_fs.path_handlers.Path__Handler__Custom          import Path__Handler__Custom
from osbot_utils.helpers.Safe_Id                            import Safe_Id
from osbot_utils.helpers.safe_str.Safe_Str__File__Path      import Safe_Str__File__Path


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
            result = _.generate_path(file_id     = "test-file"  ,
                                     file_ext    = "json"        ,
                                     is_metadata = True          )
            assert result == self.custom_path                                           # Always returns custom path

    def test_generate_path_different_params(self):                                      # Test that params don't affect result
        with self.handler as _:
            result1 = _.generate_path(file_id     = "file1"     ,
                                      file_ext    = "txt"        ,
                                      is_metadata = False        )
            result2 = _.generate_path(file_id     = "file2"     ,
                                      file_ext    = "json"       ,
                                      is_metadata = True         )
            assert result1 == self.custom_path
            assert result2 == self.custom_path
            assert result1 == result2                                                   # All return same custom path
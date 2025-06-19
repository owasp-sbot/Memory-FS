from unittest                                               import TestCase
from memory_fs.path_handlers.Path__Handler__Versioned       import Path__Handler__Versioned
from osbot_utils.helpers.Safe_Id                            import Safe_Id
from osbot_utils.helpers.safe_str.Safe_Str__File__Path      import Safe_Str__File__Path


class test_Path__Handler__Versioned(TestCase):                                          # Test versioned path handler

    def setUp(self):                                                                    # Initialize test data
        self.handler = Path__Handler__Versioned()

    def test__init__(self):                                                             # Test initialization
        with self.handler as _:
            assert type(_) is Path__Handler__Versioned
            assert _.name  == Safe_Id("versioned")

    def test_generate_path_metadata(self):                                              # Test metadata path generation
        with self.handler as _:
            result = _.generate_path(file_id     = "test-file"  ,
                                     file_ext    = "txt"         ,
                                     is_metadata = True          ,
                                     version     = 1             )
            assert result == Safe_Str__File__Path("v1/test-file.json")

    def test_generate_path_content(self):                                               # Test content path generation
        with self.handler as _:
            result = _.generate_path(file_id     = "test-file"  ,
                                     file_ext    = "txt"         ,
                                     is_metadata = False         ,
                                     version     = 1             )
            assert result == Safe_Str__File__Path("v1/test-file.txt")

    def test_generate_path_different_versions(self):                                    # Test different version numbers
        with self.handler as _:
            result_v1 = _.generate_path(file_id     = "file"    ,
                                        file_ext    = "json"     ,
                                        is_metadata = False      ,
                                        version     = 1          )
            result_v5 = _.generate_path(file_id     = "file"    ,
                                        file_ext    = "json"     ,
                                        is_metadata = False      ,
                                        version     = 5          )
            assert result_v1 == Safe_Str__File__Path("v1/file.json")
            assert result_v5 == Safe_Str__File__Path("v5/file.json")
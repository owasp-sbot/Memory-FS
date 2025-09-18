from unittest                                                                      import TestCase
from memory_fs.path_handlers.Path__Handler__Versioned                              import Path__Handler__Versioned
from osbot_utils.type_safe.primitives.domains.identifiers.safe_str.Safe_Str__Id    import Safe_Str__Id
from osbot_utils.type_safe.primitives.domains.files.safe_str.Safe_Str__File__Path  import Safe_Str__File__Path


class test_Path__Handler__Versioned(TestCase):                                          # Test versioned path handler

    def setUp(self):                                                                    # Initialize test data
        self.handler = Path__Handler__Versioned()

    def test__init__(self):                                                             # Test initialization
        with self.handler as _:
            assert type(_)           is Path__Handler__Versioned
            assert _.name            == Safe_Str__Id("versioned")
            assert _.current_version == 1
            assert _.version_prefix  == "v"

    def test_generate_path_default(self):                                              # Test default path generation
        with self.handler as _:
            result = _.generate_path()
            assert result == Safe_Str__File__Path("v1")

    def test_generate_path_with_prefix_suffix(self):                                   # Test with prefix and suffix
        with self.handler as _:
            _.prefix_path = Safe_Str__File__Path("releases")
            _.suffix_path = Safe_Str__File__Path("stable")
            result = _.generate_path()
            assert result == Safe_Str__File__Path("releases/v1/stable")

    def test_increment_version(self):                                                  # Test version increment
        with self.handler as _:
            assert _.generate_path() == Safe_Str__File__Path("v1")

            _.increment_version()
            assert _.current_version == 2
            assert _.generate_path() == Safe_Str__File__Path("v2")

            _.increment_version()
            assert _.current_version == 3
            assert _.generate_path() == Safe_Str__File__Path("v3")

    def test_set_version(self):                                                        # Test setting specific version
        with self.handler as _:
            _.set_version(5)
            assert _.current_version == 5
            assert _.generate_path() == Safe_Str__File__Path("v5")

            _.set_version(10)
            assert _.current_version == 10
            assert _.generate_path() == Safe_Str__File__Path("v10")

    def test_custom_version_prefix(self):                                              # Test custom version prefix
        with self.handler as _:
            _.version_prefix = "version-"
            _.set_version(3)
            result = _.generate_path()
            assert result == Safe_Str__File__Path("version-3")
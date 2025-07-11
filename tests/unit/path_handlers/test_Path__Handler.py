from unittest                                               import TestCase
from memory_fs.path_handlers.Path__Handler                  import Path__Handler
from osbot_utils.helpers.Safe_Id                            import Safe_Id


class test_Path__Handler(TestCase):                                                     # Test base path handler class

    def test__init__(self):                                                             # Test initialization
        with Path__Handler() as _:
            assert type(_)     is Path__Handler
            assert _.name      is None

    def test_generate_path(self):                                                      # Test abstract method
        with Path__Handler() as _:
            try:
                _.generate_path()
                assert False, "Should raise NotImplementedError"
            except NotImplementedError:
                pass                                                                    # Expected
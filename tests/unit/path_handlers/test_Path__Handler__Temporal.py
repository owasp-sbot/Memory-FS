from unittest                                               import TestCase
from datetime                                               import datetime
from memory_fs.path_handlers.Path__Handler__Temporal        import Path__Handler__Temporal
from osbot_utils.helpers.Safe_Id                            import Safe_Id
from osbot_utils.helpers.safe_str.Safe_Str__File__Path      import Safe_Str__File__Path


class test_Path__Handler__Temporal(TestCase):                                           # Test temporal path handler

    def setUp(self):                                                                    # Initialize test data
        self.handler = Path__Handler__Temporal()

    def test__init__(self):                                                             # Test initialization
        with self.handler as _:
            assert type(_) is Path__Handler__Temporal
            assert _.name  == Safe_Id("temporal")
            assert _.areas == []

    def test_generate_path(self):                                                       # Test path generation
        with self.handler as _:
            result    = _.generate_path()
            time_path = _.path_now()

            assert result         == Safe_Str__File__Path(time_path)
            assert type(result)   is Safe_Str__File__Path

    def test_generate_path_with_areas(self):                                            # Test path generation with areas
        areas = [Safe_Id("area1"), Safe_Id("area2")]
        handler_with_areas = Path__Handler__Temporal(areas=areas)

        with handler_with_areas as _:
            result    = _.generate_path()
            time_path = _.path_now()
            expected  = Safe_Str__File__Path(f"{time_path}/area1/area2")

            assert result == expected

    def test_path_now(self):                                                           # Test time path generation
        with self.handler as _:
            path_now = _.path_now()
            now      = datetime.now()
            expected = now.strftime("%Y/%m/%d/%H")

            assert path_now == expected
            assert "/" in path_now
            assert len(path_now.split("/")) == 4                                        # Year/month/day/hour
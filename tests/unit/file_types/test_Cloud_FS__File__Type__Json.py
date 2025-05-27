from unittest                                                  import TestCase
from memory_fs.file_types.Cloud_FS__File__Type__Json import Cloud_FS__File__Type__Json


class test_Cloud_FS__File__Type__Json(TestCase):

    def test__init__(self):
        with Cloud_FS__File__Type__Json() as _:
            assert type(_) is Cloud_FS__File__Type__Json
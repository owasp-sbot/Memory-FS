from osbot_utils.helpers.safe_str.Safe_Str__File__Path      import Safe_Str__File__Path
from memory_fs.file_types.Memory_FS__File__Type__Json       import Memory_FS__File__Type__Json
from memory_fs.schemas.Schema__Memory_FS__File__Config      import Schema__Memory_FS__File__Config
from osbot_utils.helpers.Safe_Id                            import Safe_Id
from tests.unit.Base_Test__File_FS                          import Base_Test__File_FS
from memory_fs.target_fs.Target_FS                          import Target_FS
from memory_fs.file_fs.File_FS                              import File_FS


class test_Target_FS(Base_Test__File_FS):                                               # Test target FS class

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.target_fs = Target_FS(storage_fs = cls.storage_fs)

    def setUp(self):                                                                    # Initialize test data
        super().setUp()
        self.target_fs.path__handlers = []                                              # reset the path__handlers since they are often modified by the individual tests

    def test__init__(self):
        with self.target_fs as _:
            assert type(_)          is Target_FS
            assert _.storage_fs     == self.storage_fs
            assert _.path__handlers == []

    def test_file_fs(self):                                                             # Test file_fs method

        file_id   = Safe_Id()
        file_type = Memory_FS__File__Type__Json()
        with self.target_fs.file_fs(file_id=file_id, file_type=file_type) as _:
            assert type(_)                   is File_FS
            assert type(_.file__config)      is Schema__Memory_FS__File__Config
            assert _.storage_fs              == self.storage_fs
            assert _.file__config.file_id    == file_id
            assert _.file__config.file_type  == file_type
            assert _.file__config.file_paths == []
            assert _.paths()                 == [Safe_Str__File__Path(f'{file_id}.json.config'  ),
                                                 Safe_Str__File__Path(f'{file_id}.json'         ),
                                                 Safe_Str__File__Path(f'{file_id}.json.metadata')]


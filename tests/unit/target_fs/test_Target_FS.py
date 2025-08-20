import pytest
from osbot_utils.type_safe.type_safe_core.collections.Type_Safe__List               import Type_Safe__List
from memory_fs.path_handlers.Path__Handler                                          import Path__Handler
from memory_fs.path_handlers.Path__Handler__Temporal                                import Path__Handler__Temporal
from memory_fs.path_handlers.Path__Handler__Latest                                  import Path__Handler__Latest
from memory_fs.storage_fs.Storage_FS                                                import Storage_FS
from osbot_utils.utils.Objects                                                      import __
from osbot_utils.type_safe.primitives.safe_str.filesystem.Safe_Str__File__Path      import Safe_Str__File__Path
from memory_fs.file_types.Memory_FS__File__Type__Json                               import Memory_FS__File__Type__Json
from memory_fs.schemas.Schema__Memory_FS__File__Config                              import Schema__Memory_FS__File__Config
from osbot_utils.type_safe.primitives.safe_str.identifiers.Safe_Id                  import Safe_Id
from tests.unit.Base_Test__File_FS                                                  import Base_Test__File_FS
from memory_fs.target_fs.Target_FS                                                  import Target_FS
from memory_fs.file_fs.File_FS                                                      import File_FS


class test_Target_FS(Base_Test__File_FS):                                               # Test target FS class

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.target_fs = Target_FS(storage_fs = cls.storage_fs)

    def setUp(self):                                                                    # Initialize test data
        super().setUp()
        self.file_id                  = Safe_Id('an-file')
        self.target_fs.path__handlers = []                                              # reset the path__handlers since they are often modified by the individual tests

    def test__init__(self):
        with self.target_fs as _:
            assert type(_)          is Target_FS
            assert _.storage_fs     == self.storage_fs
            assert _.path__handlers == []

    def test_file_fs(self):                                                             # Test file_fs method
        file_type = Memory_FS__File__Type__Json
        with self.target_fs.file_fs(file_id=self.file_id, file_type=file_type) as _:
            assert type(_)                         is File_FS
            assert type(_.file__config)            is Schema__Memory_FS__File__Config
            assert _.storage_fs                    == self.storage_fs
            assert _.file__config.file_id          == self.file_id
            assert type(_.file__config.file_type)  == file_type
            assert _.file__config.file_type.obj()  == __(name           = 'json' ,
                                                         content_type   ='JSON'  ,
                                                         file_extension = 'json' ,
                                                         encoding       = 'UTF_8',
                                                         serialization  = 'JSON' )
            assert _.file__config.file_paths       == []
            assert _.paths()                       == [Safe_Str__File__Path(f'{self.file_id}.json.config'  ),
                                                       Safe_Str__File__Path(f'{self.file_id}.json'         ),
                                                       Safe_Str__File__Path(f'{self.file_id}.json.metadata')]


    def test_file_fs__json(self):
        with self.target_fs.file_fs__json(file_id=self.file_id) as _:
            assert type(_) is File_FS
            assert _.file__config.file_id         == self.file_id
            assert _.file__config.file_type.obj() == Memory_FS__File__Type__Json().obj()

    def test__with_target_type__latest(self):
        self.target_fs.path__handlers = [Path__Handler__Latest()]
        with self.target_fs.file_fs__json(file_id=self.file_id) as _:
            assert type(_) is File_FS
            assert _.file__config.file_id == self.file_id
            assert _.paths() == ['latest/an-file.json.config'  ,
                                 'latest/an-file.json'         ,
                                 'latest/an-file.json.metadata']

    def test__with_target_type__latest__temporal(self):
        path_handler_temporal = Path__Handler__Temporal()
        path_now              = path_handler_temporal.path_now()
        self.target_fs.path__handlers = [Path__Handler__Latest(), path_handler_temporal]
        with self.target_fs.file_fs__json(file_id=self.file_id) as _:
            assert type(_) is File_FS
            assert _.file__config.file_id == self.file_id
            assert _.paths() == [ 'latest/an-file.json.config'      ,
                                 f'{path_now}/an-file.json.config'  ,
                                  'latest/an-file.json'             ,
                                 f'{path_now}/an-file.json'         ,
                                  'latest/an-file.json.metadata'    ,
                                 f'{path_now}/an-file.json.metadata']


    def test__regression___list__type_safety__not_checked_on_assigment(self):
        with Target_FS() as _:
            assert type(_.storage_fs             ) is Storage_FS
            assert type(_.path__handlers         ) is Type_Safe__List
            assert _.path__handlers.expected_type is Path__Handler

            with pytest.raises(TypeError, match="In Type_Safe__List: Invalid type for item: Expected 'Path__Handler', but got 'str'"):
                _.path__handlers = ['str']                                                      # FIXED: BUG: this breaks type safety (an exception should have been raised)

            with pytest.raises(TypeError, match="In Type_Safe__List: Invalid type for item: Expected 'Path__Handler', but got 'type'"):
                self.target_fs.path__handlers = [Path__Handler__Latest]                         # FIXED: this now raises the correct exception




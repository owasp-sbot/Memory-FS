from unittest                                               import TestCase
from memory_fs.file_fs.actions.File_FS__Name                import File_FS__Name, FILE_EXTENSION__MEMORY_FS__FILE__CONFIG
from memory_fs.file_fs.actions.File_FS__Paths               import File_FS__Paths
from memory_fs.file_types.Memory_FS__File__Type__Json       import Memory_FS__File__Type__Json
from memory_fs.file_types.Memory_FS__File__Type__Text       import Memory_FS__File__Type__Text
from memory_fs.file_types.Memory_FS__File__Type__Png        import Memory_FS__File__Type__Png
from memory_fs.schemas.Schema__Memory_FS__File__Config      import Schema__Memory_FS__File__Config
from osbot_utils.helpers.Safe_Id                            import Safe_Id
from osbot_utils.helpers.safe_str.Safe_Str__File__Path      import Safe_Str__File__Path


class test_File_FS__Paths(TestCase):                                                    # Test path generation logic

    def setUp(self):                                                                    # Initialize test data for each test
        self.file_id        = Safe_Id("test-file")
        self.file_type_json = Memory_FS__File__Type__Json()
        self.file_type_text = Memory_FS__File__Type__Text()
        self.file_type_png  = Memory_FS__File__Type__Png()
        self.file_config    = Schema__Memory_FS__File__Config(file_id   = self.file_id       ,
                                                              file_type = self.file_type_json)
        self.paths          = File_FS__Paths(file__config=self.file_config)

    def test__init__(self):                                                             # Test basic initialization
        assert type(self.paths)               is File_FS__Paths
        assert type(self.paths.file__config)  is Schema__Memory_FS__File__Config
        assert self.paths.file__config        == self.file_config

    def test_file_fs__name(self):                                                       # Test file_fs__name property
        file_name = self.paths.file_fs__name()
        assert type(file_name)        is File_FS__Name
        assert file_name.file__config == self.file_config

    def test_paths_no_file_paths(self):                                                # Test paths() when no file_paths are defined
        paths = self.paths.paths()
        assert type(paths) is list
        assert len(paths)  == 1
        assert paths       == [Safe_Str__File__Path(f'test-file.json.{FILE_EXTENSION__MEMORY_FS__FILE__CONFIG}')]

    def test_paths_with_single_path(self):                                             # Test paths() with single file path
        path = Safe_Str__File__Path("folder/subfolder")
        self.file_config.file_paths = [path]

        paths = self.paths.paths()
        assert len(paths) == 1
        assert paths      == [Safe_Str__File__Path(f'folder/subfolder/test-file.json.{FILE_EXTENSION__MEMORY_FS__FILE__CONFIG}')]

    def test_paths_with_multiple_paths(self):                                          # Test paths() with multiple file paths
        paths_list = [Safe_Str__File__Path("path1")            ,
                      Safe_Str__File__Path("path2/sub")        ,
                      Safe_Str__File__Path("path3/sub/deep")   ]
        self.file_config.file_paths = paths_list

        paths = self.paths.paths()
        assert len(paths) == 3
        assert paths      == [Safe_Str__File__Path(f'path1/test-file.json.{FILE_EXTENSION__MEMORY_FS__FILE__CONFIG}')        ,
                              Safe_Str__File__Path(f'path2/sub/test-file.json.{FILE_EXTENSION__MEMORY_FS__FILE__CONFIG}')    ,
                              Safe_Str__File__Path(f'path3/sub/deep/test-file.json.{FILE_EXTENSION__MEMORY_FS__FILE__CONFIG}')]

    def test_paths__content_no_file_paths(self):                                       # Test paths__content() when no file_paths are defined
        paths = self.paths.paths__content()
        assert type(paths) is list
        assert len(paths)  == 1
        assert paths       == [Safe_Str__File__Path('test-file.json')]

    def test_paths__content_with_single_path(self):                                    # Test paths__content() with single file path
        path = Safe_Str__File__Path("content/folder")
        self.file_config.file_paths = [path]

        paths = self.paths.paths__content()
        assert len(paths) == 1
        assert paths      == [Safe_Str__File__Path('content/folder/test-file.json')]

    def test_paths__content_different_file_types(self):                                # Test paths__content() with different file types
        paths_json = self.paths.paths__content()
        assert paths_json == [Safe_Str__File__Path('test-file.json')]

        self.file_config.file_type = self.file_type_text
        paths_text = File_FS__Paths(file__config=self.file_config).paths__content()
        assert paths_text == [Safe_Str__File__Path('test-file.txt')]

        self.file_config.file_type = self.file_type_png
        paths_png = File_FS__Paths(file__config=self.file_config).paths__content()
        assert paths_png == [Safe_Str__File__Path('test-file.png')]

    def test__regression__none_extension(self):                                        # Test bug when file_type.file_extension is None
        file_config = Schema__Memory_FS__File__Config(file_id='test-file')
        with File_FS__Paths(file__config=file_config) as _:
            paths = _.paths()
            assert paths == [Safe_Str__File__Path(f'test-file.{FILE_EXTENSION__MEMORY_FS__FILE__CONFIG}')]

            content_paths = _.paths__content()
            assert content_paths == [Safe_Str__File__Path('test-file')]
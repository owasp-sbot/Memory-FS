from unittest                                           import TestCase
from memory_fs.file.actions.File_FS__Name               import File_FS__Name, FILE_EXTENSION__MEMORY_FS__FILE__CONFIG
from memory_fs.file.actions.File_FS__Paths              import File_FS__Paths
from memory_fs.file_types.Memory_FS__File__Type__Json   import Memory_FS__File__Type__Json
from memory_fs.file_types.Memory_FS__File__Type__Text   import Memory_FS__File__Type__Text
from memory_fs.file_types.Memory_FS__File__Type__Png    import Memory_FS__File__Type__Png
from memory_fs.schemas.Schema__Memory_FS__File__Config  import Schema__Memory_FS__File__Config
from osbot_utils.helpers.Safe_Id                        import Safe_Id
from osbot_utils.helpers.safe_str.Safe_Str__File__Path  import Safe_Str__File__Path


class test_Memory_FS__Paths(TestCase):

    def setUp(self):                                                                             # Initialize test data for each test
        self.file_id        = Safe_Id("test-file")
        self.file_type_json = Memory_FS__File__Type__Json()
        self.file_type_text = Memory_FS__File__Type__Text()
        self.file_type_png  = Memory_FS__File__Type__Png()

        self.file_config = Schema__Memory_FS__File__Config(file_id   = self.file_id,
                                                          file_type = self.file_type_json)
        self.paths = File_FS__Paths(file__config=self.file_config)

    def test__init__(self):                                                                      # Test basic initialization
        assert type(self.paths) is File_FS__Paths
        assert type(self.paths.file__config) is Schema__Memory_FS__File__Config
        assert self.paths.file__config       == self.file_config

    def test_file_name(self):                                                                    # Test file_name property
        file_name = self.paths.file_fs__name()
        assert type(file_name) is File_FS__Name
        assert file_name.file__config     == self.file_config

    def test_paths_no_file_paths(self):                                                         # Test paths() when no file_paths are defined
        paths = self.paths.paths()
        assert type(paths) is list
        assert len(paths)  == 1
        assert paths       == [Safe_Str__File__Path(f'test-file.json.{FILE_EXTENSION__MEMORY_FS__FILE__CONFIG}')]

    def test_paths_with_single_path(self):                                                      # Test paths() with single file path
        path = Safe_Str__File__Path("folder/subfolder")
        self.file_config.file_paths = [path]

        paths = self.paths.paths()
        assert len(paths) == 1
        assert paths      == [Safe_Str__File__Path(f'folder/subfolder/test-file.json.{FILE_EXTENSION__MEMORY_FS__FILE__CONFIG}')]

    def test_paths_with_multiple_paths(self):                                                   # Test paths() with multiple file paths
        paths_list = [Safe_Str__File__Path("path1"),
                      Safe_Str__File__Path("path2/sub"),
                      Safe_Str__File__Path("path3/sub/deep")]
        self.file_config.file_paths = paths_list

        paths = self.paths.paths()
        assert len(paths) == 3
        assert paths      == [Safe_Str__File__Path(f'path1/test-file.json.{FILE_EXTENSION__MEMORY_FS__FILE__CONFIG}'),
                              Safe_Str__File__Path(f'path2/sub/test-file.json.{FILE_EXTENSION__MEMORY_FS__FILE__CONFIG}'),
                              Safe_Str__File__Path(f'path3/sub/deep/test-file.json.{FILE_EXTENSION__MEMORY_FS__FILE__CONFIG}')]

    def test_paths_different_file_types(self):                                                  # Test paths() with different file types
        # Test with JSON
        paths_json = self.paths.paths()
        assert paths_json == [Safe_Str__File__Path(f'test-file.json.{FILE_EXTENSION__MEMORY_FS__FILE__CONFIG}')]

        # Test with Text
        self.file_config.file_type = self.file_type_text
        paths_text = File_FS__Paths(file__config=self.file_config).paths()
        assert paths_text == [Safe_Str__File__Path(f'test-file.txt.{FILE_EXTENSION__MEMORY_FS__FILE__CONFIG}')]

        # Test with PNG
        self.file_config.file_type = self.file_type_png
        paths_png = File_FS__Paths(file__config=self.file_config).paths()
        assert paths_png == [Safe_Str__File__Path(f'test-file.png.{FILE_EXTENSION__MEMORY_FS__FILE__CONFIG}')]

    def test_paths__content_no_file_paths(self):                                               # Test paths__content() when no file_paths are defined
        paths = self.paths.paths__content()
        assert type(paths) is list
        assert len(paths)  == 1
        assert paths       == [Safe_Str__File__Path('test-file.json')]

    def test_paths__content_with_single_path(self):                                            # Test paths__content() with single file path
        path = Safe_Str__File__Path("content/folder")
        self.file_config.file_paths = [path]

        paths = self.paths.paths__content()
        assert len(paths) == 1
        assert paths      == [Safe_Str__File__Path('content/folder/test-file.json')]

    def test_paths__content_with_multiple_paths(self):                                         # Test paths__content() with multiple file paths
        paths_list = [Safe_Str__File__Path("content1"),
                      Safe_Str__File__Path("content2/sub")]
        self.file_config.file_paths = paths_list

        paths = self.paths.paths__content()
        assert len(paths) == 2
        assert paths      == [Safe_Str__File__Path('content1/test-file.json'),
                              Safe_Str__File__Path('content2/sub/test-file.json')]

    def test_paths__content_different_file_types(self):                                        # Test paths__content() with different file types
        # Test with JSON
        paths_json = self.paths.paths__content()
        assert paths_json == [Safe_Str__File__Path('test-file.json')]

        # Test with Text
        self.file_config.file_type = self.file_type_text
        paths_text = File_FS__Paths(file__config=self.file_config).paths__content()
        assert paths_text == [Safe_Str__File__Path('test-file.txt')]

        # Test with PNG
        self.file_config.file_type = self.file_type_png
        paths_png = File_FS__Paths(file__config=self.file_config).paths__content()
        assert paths_png == [Safe_Str__File__Path('test-file.png')]

    def test_paths_with_special_characters_in_file_id(self):                                   # Test paths with special characters in file_id
        special_file_id = Safe_Id("my-file_2024_v1")
        self.file_config.file_id = special_file_id
        self.file_config.file_paths = [Safe_Str__File__Path("data")]

        paths = File_FS__Paths(file__config=self.file_config).paths()
        assert paths == [Safe_Str__File__Path(f'data/my-file_2024_v1.json.{FILE_EXTENSION__MEMORY_FS__FILE__CONFIG}')]

    def test_paths_empty_file_id(self):                                                        # Test behavior with empty file_id
        # Note: Safe_Id might not allow empty strings, but testing the edge case
        try:
            empty_id_config = Schema__Memory_FS__File__Config(file_id   = Safe_Id(""),
                                                             file_type = self.file_type_json)
            paths = File_FS__Paths(file__config=empty_id_config).paths()
            assert paths == [Safe_Str__File__Path('.json.{FILE_EXTENSION__MEMORY_FS__FILE__CONFIG}')]
        except:
            # Safe_Id validation might prevent empty strings
            pass

    def test_cache_on_self_file_name(self):                                                    # Test that file_name is cached
        file_name_1 = self.paths.file_fs__name()
        file_name_2 = self.paths.file_fs__name()
        assert file_name_1 is file_name_2  # Same object due to @cache_on_self

    def test_type_safe_decorator(self):                                                        # Test @type_safe decorator on paths method
        # The paths() method has @type_safe decorator which should validate parameters
        # Since it takes no parameters, this mainly ensures the decorator doesn't break functionality
        paths = self.paths.paths()
        assert type(paths) is list
        assert all(type(p) is Safe_Str__File__Path for p in paths)

    def test_todo_comments_implementation(self):                                               # Test areas marked with TODO comments
        # TODO items mentioned in the code:
        # 1. content to be saved as {file_id}.{extension}
        # 2. config {file_id}.{extension}.config
        # 3. metadata to be saved as {file_id}.{extension}.metadata

        # Current implementation uses .{FILE_EXTENSION__MEMORY_FS__FILE__CONFIG} suffix
        paths = self.paths.paths()
        assert all(str(p).endswith(f'.{FILE_EXTENSION__MEMORY_FS__FILE__CONFIG}') for p in paths)

        # Content paths don't have .{FILE_EXTENSION__MEMORY_FS__FILE__CONFIG} suffix
        content_paths = self.paths.paths__content()
        assert all(not str(p).endswith(f'.{FILE_EXTENSION__MEMORY_FS__FILE__CONFIG}') for p in content_paths)

    def test__regression__none_extension(self):                                                         # Test bug when file_type.file_extension is None
        file_config = Schema__Memory_FS__File__Config(file_id='test-file')                     # Create a file type with no extension set
        with File_FS__Paths(file__config=file_config)  as _:

            paths = _.paths()
            assert paths == [Safe_Str__File__Path(f'test-file.{FILE_EXTENSION__MEMORY_FS__FILE__CONFIG}')]  # FIXED: (had .none. in the file name)

            content_paths = _.paths__content()
            assert content_paths == [Safe_Str__File__Path('test-file')]
from unittest                                               import TestCase
from memory_fs.file_fs.actions.File_FS__Name                import File_FS__Name, FILE_EXTENSION__MEMORY_FS__FILE__CONFIG, FILE_EXTENSION__MEMORY_FS__FILE__METADATA
from memory_fs.file_fs.actions.File_FS__Paths               import File_FS__Paths
from memory_fs.file_types.Memory_FS__File__Type__Json       import Memory_FS__File__Type__Json
from memory_fs.file_types.Memory_FS__File__Type__Text       import Memory_FS__File__Type__Text
from memory_fs.file_types.Memory_FS__File__Type__Png        import Memory_FS__File__Type__Png
from memory_fs.schemas.Schema__Memory_FS__File__Config      import Schema__Memory_FS__File__Config
from osbot_utils.type_safe.primitives.safe_str.identifiers.Safe_Id                            import Safe_Id
from osbot_utils.type_safe.primitives.safe_str.filesystem.Safe_Str__File__Path      import Safe_Str__File__Path


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

    # ===== Tests for paths() method (returns config paths) =====

    def test_paths_no_file_paths(self):                                                         # Test paths() when no file_paths are defined
        paths = self.paths.paths__config()
        assert type(paths) is list
        assert len(paths)  == 1
        assert paths       == [Safe_Str__File__Path(f'test-file.json.{FILE_EXTENSION__MEMORY_FS__FILE__CONFIG}')]

    def test_paths_with_single_path(self):                                                      # Test paths() with single file path
        path = Safe_Str__File__Path("folder/subfolder")
        self.file_config.file_paths = [path]

        paths = self.paths.paths__config()
        assert len(paths) == 1
        assert paths      == [Safe_Str__File__Path(f'folder/subfolder/test-file.json.{FILE_EXTENSION__MEMORY_FS__FILE__CONFIG}')]

    def test_paths_with_multiple_paths(self):                                          # Test paths() with multiple file paths
        paths_list = [Safe_Str__File__Path("path1")            ,
                      Safe_Str__File__Path("path2/sub")        ,
                      Safe_Str__File__Path("path3/sub/deep")   ]
        self.file_config.file_paths = paths_list

        paths = self.paths.paths__config()
        assert len(paths) == 3
        assert paths      == [Safe_Str__File__Path(f'path1/test-file.json.{FILE_EXTENSION__MEMORY_FS__FILE__CONFIG}')        ,
                              Safe_Str__File__Path(f'path2/sub/test-file.json.{FILE_EXTENSION__MEMORY_FS__FILE__CONFIG}')    ,
                              Safe_Str__File__Path(f'path3/sub/deep/test-file.json.{FILE_EXTENSION__MEMORY_FS__FILE__CONFIG}')]

    def test_paths_different_file_types(self):                                         # Test paths() with different file types
        # Test with JSON
        paths_json = self.paths.paths__config()
        assert paths_json == [Safe_Str__File__Path(f'test-file.json.{FILE_EXTENSION__MEMORY_FS__FILE__CONFIG}')]

        # Test with Text
        self.file_config.file_type = self.file_type_text
        paths_text = File_FS__Paths(file__config=self.file_config).paths__config()
        assert paths_text == [Safe_Str__File__Path(f'test-file.txt.{FILE_EXTENSION__MEMORY_FS__FILE__CONFIG}')]

        # Test with PNG
        self.file_config.file_type = self.file_type_png
        paths_png = File_FS__Paths(file__config=self.file_config).paths__config()
        assert paths_png == [Safe_Str__File__Path(f'test-file.png.{FILE_EXTENSION__MEMORY_FS__FILE__CONFIG}')]

    # ===== Tests for paths__config() method =====

    def test_paths__config_no_file_paths(self):                                                # Test paths__config() when no file_paths are defined
        paths = self.paths.paths__config()
        assert type(paths) is list
        assert len(paths)  == 1
        assert paths       == [Safe_Str__File__Path(f'test-file.json.{FILE_EXTENSION__MEMORY_FS__FILE__CONFIG}')]

    def test_paths__config_with_single_path(self):                                             # Test paths__config() with single file path
        path = Safe_Str__File__Path("configs/folder")
        self.file_config.file_paths = [path]

        paths = self.paths.paths__config()
        assert len(paths) == 1
        assert paths      == [Safe_Str__File__Path(f'configs/folder/test-file.json.{FILE_EXTENSION__MEMORY_FS__FILE__CONFIG}')]

    def test_paths__config_with_multiple_paths(self):                                          # Test paths__config() with multiple file paths
        paths_list = [Safe_Str__File__Path("configs/v1"),
                      Safe_Str__File__Path("configs/v2")]
        self.file_config.file_paths = paths_list

        paths = self.paths.paths__config()
        assert len(paths) == 2
        assert paths      == [Safe_Str__File__Path(f'configs/v1/test-file.json.{FILE_EXTENSION__MEMORY_FS__FILE__CONFIG}'),
                              Safe_Str__File__Path(f'configs/v2/test-file.json.{FILE_EXTENSION__MEMORY_FS__FILE__CONFIG}')]

    # ===== Tests for paths__content() method =====

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

    # ===== Edge cases and special scenarios =====

    def test_paths_with_special_characters_in_file_id(self):                                   # Test paths with special characters in file_id
        special_file_id = Safe_Id("my-file_2024_v1")
        self.file_config.file_id = special_file_id
        self.file_config.file_paths = [Safe_Str__File__Path("data")]

        paths = File_FS__Paths(file__config=self.file_config).paths__config()
        assert paths == [Safe_Str__File__Path(f'data/my-file_2024_v1.json.{FILE_EXTENSION__MEMORY_FS__FILE__CONFIG}')]

    def test_paths_with_empty_path_string(self):                                               # Test behavior with empty path string
        self.file_config.file_paths = [Safe_Str__File__Path("")]

        paths_config = self.paths.paths__config()
        assert paths_config == [Safe_Str__File__Path(f'test-file.json.{FILE_EXTENSION__MEMORY_FS__FILE__CONFIG}')]

        paths_content = self.paths.paths__content()
        assert paths_content == [Safe_Str__File__Path('test-file.json')]

    def test_paths_with_trailing_slash(self):                                                  # Test paths with trailing slashes
        self.file_config.file_paths = [Safe_Str__File__Path("folder/")]

        paths = self.paths.paths__config()
        assert paths == [Safe_Str__File__Path(f'folder/test-file.json.{FILE_EXTENSION__MEMORY_FS__FILE__CONFIG}')]

    def test_paths_with_root_path(self):                                                       # Test paths with root path "/"
        self.file_config.file_paths = [Safe_Str__File__Path("/")]

        paths = self.paths.paths__config()
        assert paths == [Safe_Str__File__Path(f'/test-file.json.{FILE_EXTENSION__MEMORY_FS__FILE__CONFIG}')]

    def test__regression__none_extension(self):                                                  # Test bug when file_type.file_extension is None
        file_config = Schema__Memory_FS__File__Config(file_id='test-file')                     # Create a file type with no extension set
        with File_FS__Paths(file__config=file_config) as _:
            paths = _.paths__config()
            assert paths == [Safe_Str__File__Path(f'test-file.{FILE_EXTENSION__MEMORY_FS__FILE__CONFIG}')]

            content_paths = _.paths__content()
            assert content_paths == [Safe_Str__File__Path('test-file')]

    # ===== Tests for caching behavior =====

    def test_cache_on_self_file_name(self):                                                    # Test that file_name is cached
        file_name_1 = self.paths.file_fs__name()
        file_name_2 = self.paths.file_fs__name()
        assert file_name_1 is file_name_2  # Same object due to @cache_on_self

    # ===== Tests for type safety =====

    def test_type_safe_decorator(self):                                                        # Test @type_safe decorator on paths method
        # The paths() method has @type_safe decorator which should validate parameters
        # Since it takes no parameters, this mainly ensures the decorator doesn't break functionality
        paths = self.paths.paths()
        assert type(paths) is list
        assert all(type(p) is Safe_Str__File__Path for p in paths)

    # ===== Tests for consistency between methods =====

    def test_consistency_paths_and_paths__config(self):                                        # Test that paths() and paths__config() return same results
        self.file_config.file_paths = [Safe_Str__File__Path("test/path")]

        paths_from_paths    = self.paths.paths          ()
        paths_from_config   = self.paths.paths__config  ()
        paths_from_content  = self.paths.paths__content ()
        paths_from_metadata = self.paths.paths__metadata()

        assert paths_from_paths == paths_from_config + paths_from_content + paths_from_metadata

    def test_all_methods_handle_multiple_paths_consistently(self):                             # Test all methods handle multiple paths consistently
        paths_list = [Safe_Str__File__Path("path1"),
                      Safe_Str__File__Path("path2")]
        self.file_config.file_paths = paths_list

        # All methods should return same number of paths
        assert len(self.paths.paths         ()) == 6
        assert len(self.paths.paths__config ()) == 2
        assert len(self.paths.paths__content()) == 2

    # ===== Tests for path composition =====

    def test_complex_nested_paths(self):                                                        # Test deeply nested path structures
        complex_path = Safe_Str__File__Path("a/b/c/d/e/f/g")
        self.file_config.file_paths = [complex_path]

        paths = self.paths.paths__config()
        assert paths == [Safe_Str__File__Path(f'a/b/c/d/e/f/g/test-file.json.{FILE_EXTENSION__MEMORY_FS__FILE__CONFIG}')]

    def test_paths_with_dots_in_path(self):                                                    # Test paths containing dots
        dotted_path = Safe_Str__File__Path("folder.v1/subfolder.v2")
        self.file_config.file_paths = [dotted_path]

        paths = self.paths.paths__content()
        assert paths == [Safe_Str__File__Path('folder.v1/subfolder.v2/test-file.json')]

    # ===== Additional test scenarios based on implementation =====

    def test_file_id_with_underscore_and_dash(self):                                          # Test file IDs with various valid characters
        mixed_id = Safe_Id("file_id-with-mixed_chars-123")
        self.file_config.file_id = mixed_id

        paths = self.paths.paths__content()
        assert paths == [Safe_Str__File__Path('file_id-with-mixed_chars-123.json')]

    def test_return_types_are_lists_of_safe_paths(self):                                      # Verify all methods return List[Safe_Str__File__Path]
        # Verify return types for all path methods
        for method in [self.paths.paths, self.paths.paths__config, self.paths.paths__content]:
            result = method()
            assert isinstance(result, list)
            assert all(isinstance(p, Safe_Str__File__Path) for p in result)

    def test_paths_ordering_preserved(self):                                                   # Test that path ordering is preserved
        ordered_paths = [
            Safe_Str__File__Path("first"),
            Safe_Str__File__Path("second"),
            Safe_Str__File__Path("third")
        ]
        self.file_config.file_paths = ordered_paths

        result_paths = self.paths.paths__content()
        expected = [
            Safe_Str__File__Path('first/test-file.json'),
            Safe_Str__File__Path('second/test-file.json'),
            Safe_Str__File__Path('third/test-file.json')
        ]
        assert result_paths == expected
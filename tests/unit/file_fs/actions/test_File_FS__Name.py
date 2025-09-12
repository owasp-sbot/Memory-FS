from unittest                                                                    import TestCase
from osbot_utils.type_safe.primitives.domains.files.safe_str.Safe_Str__File__Name  import Safe_Str__File__Name
from osbot_utils.type_safe.primitives.domains.files.safe_str.Safe_Str__File__Path   import Safe_Str__File__Path
from memory_fs.file_fs.actions.File_FS__Name                                     import File_FS__Name, FILE_EXTENSION__MEMORY_FS__FILE__CONFIG, FILE_EXTENSION__MEMORY_FS__FILE__METADATA
from memory_fs.file_types.Memory_FS__File__Type__Json                            import Memory_FS__File__Type__Json
from memory_fs.file_types.Memory_FS__File__Type__Text                            import Memory_FS__File__Type__Text
from memory_fs.schemas.Schema__Memory_FS__File__Config                           import Schema__Memory_FS__File__Config
from osbot_utils.type_safe.primitives.domains.identifiers.Safe_Id               import Safe_Id


class test_File_FS__Name(TestCase):                                                     # Test file naming logic

    @classmethod
    def setUpClass(cls):                                                                # Initialize test data
        cls.file_config = Schema__Memory_FS__File__Config()
        cls.file_name   = File_FS__Name(file__config=cls.file_config)

    def test__init__(self):                                                             # Test initialization
        with self.file_name as _:
            assert type(_)         is File_FS__Name
            assert _.file__config  == self.file_config

    # ===== Tests for name generation methods =====

    def test_build(self):                                                               # Test build method
        with self.file_name as _:
            elements = ["file", "name", "parts"]
            result   = _.build(elements)
            assert type(result) is Safe_Str__File__Name
            assert result       == "file.name.parts"

    def test_config(self):                                                              # Test config file name generation
        with self.file_name as _:
            config_file_name = _.config()
            assert type(config_file_name) is Safe_Str__File__Name
            assert config_file_name       == f'{self.file_config.file_id}.{FILE_EXTENSION__MEMORY_FS__FILE__CONFIG}'
            assert config_file_name       == f'{self.file_config.file_id}.config'

    def test_content(self):                                                             # Test content file name generation
        with self.file_name as _:
            content_file_name = _.content()
            assert type(content_file_name) is Safe_Str__File__Name
            assert content_file_name       == f'{self.file_config.file_id}'

    def test_content_with_extension(self):                                             # Test content with file extension
        # Setup file config with JSON type
        file_config_json = Schema__Memory_FS__File__Config(
            file_id   = Safe_Id("test-file"),
            file_type = Memory_FS__File__Type__Json()
        )
        file_name_json = File_FS__Name(file__config=file_config_json)

        content_name = file_name_json.content()
        assert content_name == "test-file.json"

        # Test with Text type
        file_config_text = Schema__Memory_FS__File__Config(
            file_id   = Safe_Id("test-file"),
            file_type = Memory_FS__File__Type__Text()
        )
        file_name_text = File_FS__Name(file__config=file_config_text)

        content_name = file_name_text.content()
        assert content_name == "test-file.txt"

    def test_metadata(self):                                                            # Test metadata file name generation
        with self.file_name as _:
            metadata_file_name = _.metadata()
            assert type(metadata_file_name) is Safe_Str__File__Name
            assert metadata_file_name       == f'{self.file_config.file_id}.{FILE_EXTENSION__MEMORY_FS__FILE__METADATA}'
            assert metadata_file_name       == f'{self.file_config.file_id}.metadata'

    # ===== Tests for path generation methods =====

    def test_for_path(self):                                                            # Test generic for_path method
        with self.file_name as _:
            # Test with path
            path = Safe_Str__File__Path("folder/subfolder")
            name = Safe_Str__File__Name("file.txt")
            result = _.for_path(path, name)
            assert result == Safe_Str__File__Path("folder/subfolder/file.txt")

            # Test without path
            result = _.for_path(None, name)
            assert result == Safe_Str__File__Path("file.txt")

    def test_for_path_with_trailing_slash(self):                                       # Test path joining with trailing slash
        with self.file_name as _:
            path = Safe_Str__File__Path("folder/")
            name = Safe_Str__File__Name("file.txt")
            result = _.for_path(path, name)
            # Should handle trailing slash correctly (no double slash)
            assert result == Safe_Str__File__Path("folder/file.txt")

    def test_for_path_with_root(self):                                                 # Test with root path
        with self.file_name as _:
            path = Safe_Str__File__Path("/")
            name = Safe_Str__File__Name("file.txt")
            result = _.for_path(path, name)
            assert result == Safe_Str__File__Path("/file.txt")

    def test_config__for_path(self):                                                    # Test config path generation
        with self.file_name as _:
            path         = Safe_Str__File__Path("folder/subfolder")
            result       = _.config__for_path(path)
            expected     = Safe_Str__File__Path(f'folder/subfolder/{self.file_config.file_id}.config')
            assert result == expected

    def test_config__for_path_empty(self):                                             # Test config path with no base path
        with self.file_name as _:
            result   = _.config__for_path()
            expected = Safe_Str__File__Path(f'{self.file_config.file_id}.config')
            assert result == expected

    def test_content__for_path(self):                                                   # Test content path generation
        with self.file_name as _:
            path         = Safe_Str__File__Path("data/files")
            result       = _.content__for_path(path)
            expected     = Safe_Str__File__Path(f'data/files/{self.file_config.file_id}')
            assert result == expected

    def test_content__for_path_with_extension(self):                                   # Test content path with file extension
        file_config = Schema__Memory_FS__File__Config(
            file_id   = Safe_Id("doc"),
            file_type = Memory_FS__File__Type__Json()
        )
        file_name = File_FS__Name(file__config=file_config)

        path     = Safe_Str__File__Path("content")
        result   = file_name.content__for_path(path)
        expected = Safe_Str__File__Path("content/doc.json")
        assert result == expected

    def test_metadata__for_path(self):                                                  # Test metadata path generation
        with self.file_name as _:
            path         = Safe_Str__File__Path("meta")
            result       = _.metadata__for_path(path)
            expected     = Safe_Str__File__Path(f'meta/{self.file_config.file_id}.metadata')
            assert result == expected

    def test_metadata__for_path_empty(self):                                           # Test metadata path with no base path
        with self.file_name as _:
            result   = _.metadata__for_path()
            expected = Safe_Str__File__Path(f'{self.file_config.file_id}.metadata')
            assert result == expected

    # ===== Edge cases and special scenarios =====

    def test_empty_path_string(self):                                                  # Test with empty path string
        with self.file_name as _:
            path = Safe_Str__File__Path("")
            name = Safe_Str__File__Name("file.txt")
            result = _.for_path(path, name)
            # Empty path should be treated as no path
            assert result == Safe_Str__File__Path("file.txt")

    def test_special_characters_in_file_id(self):                                      # Test file IDs with special characters
        file_config = Schema__Memory_FS__File__Config(
            file_id = Safe_Id("file_2024-01-15_v2")
        )
        file_name = File_FS__Name(file__config=file_config)

        assert file_name.config()   == "file_2024-01-15_v2.config"
        assert file_name.content()  == "file_2024-01-15_v2"
        assert file_name.metadata() == "file_2024-01-15_v2.metadata"

    def test_nested_paths(self):                                                        # Test deeply nested paths
        with self.file_name as _:
            path = Safe_Str__File__Path("a/b/c/d/e/f")
            result = _.config__for_path(path)
            expected = Safe_Str__File__Path(f'a/b/c/d/e/f/{self.file_config.file_id}.config')
            assert result == expected

    def test_path_with_dots(self):                                                     # Test paths containing dots
        with self.file_name as _:
            path = Safe_Str__File__Path("folder.v1/subfolder.v2")
            result = _.content__for_path(path)
            expected = Safe_Str__File__Path(f'folder.v1/subfolder.v2/{self.file_config.file_id}')
            assert result == expected

    def test_regression_none_extension(self):                                          # Test handling of None file extension
        # This addresses the BUG comment in the content() method
        file_config = Schema__Memory_FS__File__Config(file_id=Safe_Id('test-file'))
        file_name = File_FS__Name(file__config=file_config)

        # Should handle None extension gracefully
        content_name = file_name.content()
        assert content_name == "test-file"  # No extension appended

    def test_all_path_methods_consistency(self):                                       # Test consistency across all path methods
        with self.file_name as _:
            base_path = Safe_Str__File__Path("base/path")

            # All methods should handle the same base path consistently
            config_path   = _.config__for_path(base_path)
            content_path  = _.content__for_path(base_path)
            metadata_path = _.metadata__for_path(base_path)

            assert str(config_path).startswith("base/path/")
            assert str(content_path).startswith("base/path/")
            assert str(metadata_path).startswith("base/path/")

            # Check correct suffixes
            assert str(config_path).endswith(".config")
            assert str(metadata_path).endswith(".metadata")

    def test_file_extension_constants(self):                                           # Test that constants are correctly defined
        assert FILE_EXTENSION__MEMORY_FS__FILE__CONFIG   == 'config'
        assert FILE_EXTENSION__MEMORY_FS__FILE__METADATA == 'metadata'
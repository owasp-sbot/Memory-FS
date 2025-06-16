from unittest                                               import TestCase
from osbot_utils.helpers.safe_str.Safe_Str__File__Name      import Safe_Str__File__Name
from osbot_utils.helpers.safe_str.Safe_Str__File__Path      import Safe_Str__File__Path
from memory_fs.file_fs.actions.File_FS__Name                import File_FS__Name, FILE_EXTENSION__MEMORY_FS__FILE__CONFIG, FILE_EXTENSION__MEMORY_FS__FILE__METADATA
from memory_fs.schemas.Schema__Memory_FS__File__Config      import Schema__Memory_FS__File__Config


class test_File_FS__Name(TestCase):                                                     # Test file naming logic

    @classmethod
    def setUpClass(cls):                                                                # Initialize test data
        cls.file_config = Schema__Memory_FS__File__Config()
        cls.file_name   = File_FS__Name(file__config=cls.file_config)

    def test__init__(self):                                                             # Test initialization
        with self.file_name as _:
            assert type(_)         is File_FS__Name
            assert _.file__config  == self.file_config

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

    def test_metadata(self):                                                            # Test metadata file name generation
        with self.file_name as _:
            metadata_file_name = _.metadata()
            assert type(metadata_file_name) is Safe_Str__File__Name
            assert metadata_file_name       == f'{self.file_config.file_id}.{FILE_EXTENSION__MEMORY_FS__FILE__METADATA}'
            assert metadata_file_name       == f'{self.file_config.file_id}.metadata'

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

    def test_metadata__for_path(self):                                                  # Test metadata path generation
        with self.file_name as _:
            path         = Safe_Str__File__Path("meta")
            result       = _.metadata__for_path(path)
            expected     = Safe_Str__File__Path(f'meta/{self.file_config.file_id}.metadata')
            assert result == expected
from osbot_utils.helpers.safe_str.Safe_Str__Hash            import safe_str_hash
from osbot_utils.utils.Objects                              import __
from tests.unit.Base_Test__File_FS                          import Base_Test__File_FS
from memory_fs.file_fs.data.File_FS__Data                   import File_FS__Data
from memory_fs.file_fs.actions.File_FS__Name                import FILE_EXTENSION__MEMORY_FS__FILE__CONFIG
from osbot_utils.helpers.safe_str.Safe_Str__File__Path      import Safe_Str__File__Path


class test_File_FS__Data(Base_Test__File_FS):                                          # Test file data operations

    def setUp(self):                                                                    # Initialize test data
        super().setUp()
        self.file_data = File_FS__Data(file__config = self.file_config ,
                                       storage_fs   = self.storage_fs      )

    def test__init__(self):                                                             # Test initialization
        with self.file_data as _:
            assert type(_)         is File_FS__Data
            assert _.file__config  == self.file_config
            assert _.storage_fs    == self.storage_fs

    def test_config(self):                                                              # Test config method
        with self.file_data as _:
            assert _.config() == self.file_config

    def test_content(self):                                                             # Test content method (bytes)
        with self.file_data as _:
            assert _.content() is None                                                  # No content yet

            test_content        = b'test content'
            self.file.create__content(test_content)
            assert _.content() == test_content


    def test_data(self):                                                                # Test data method (deserialized)
        with self.file_data as _:
            test_dict = {"test": "data", "value": 123}
            self.file.save(test_dict)

            assert _.data() == test_dict

    def test_exists(self):                                                              # Test exists method
        with self.file_data as _:
            assert _.exists() is False

            self.file.create(self.default_content)
            assert _.exists() is True

    def test_not_exists(self):                                                          # Test not_exists method
        with self.file_data as _:
            assert _.not_exists() is True

            self.file.create(self.default_content)
            assert _.not_exists() is False

    def test_metadata(self):                                                            # Test metadata method
        test_content           = b'content for metadata'
        test_content__for_hash = b'"content for metadata"'
        self.file.create(test_content)

        with self.file_data as _:
            metadata = _.metadata()
            assert metadata.content__hash == safe_str_hash(test_content__for_hash)
            assert metadata.obj()         == __(content__hash         = '58a28b6f67'      ,
                                                chain_hash            = None              ,
                                                previous_version_path = None              ,
                                                content__size         = 20 + 2            ,
                                                tags                  = []                ,
                                                timestamp             = metadata.timestamp)

    def test_paths(self):                                                               # Test paths method
        with self.file_data as _:
            paths = _.paths()
            assert paths == [Safe_Str__File__Path(f'{self.file_config.file_id}.json.{FILE_EXTENSION__MEMORY_FS__FILE__CONFIG}')]
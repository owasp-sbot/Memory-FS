from memory_fs.file_types.Memory_FS__File__Type__Json  import Memory_FS__File__Type__Json
from tests.unit.Base_Test__File_FS                     import Base_Test__File_FS
from memory_fs.file_fs.data.File_FS__Content           import File_FS__Content


class test_File_FS__Content(Base_Test__File_FS):                                       # Test file content operations

    def setUp(self):                                                                    # Initialize test data
        super().setUp()
        self.file_content = File_FS__Content(file__config = self.file_config ,
                                             storage      = self.storage      )

    def test__init__(self):                                                             # Test initialization
        with self.file_content as _:
            assert type(_)         is File_FS__Content
            assert _.file__config  == self.file_config
            assert _.storage       == self.storage

    def test_bytes(self):                                                               # Test bytes method
        with self.file_content as _:
            assert _.bytes()                        is None                             # No content yet
            assert type(_.file__config.file_type)   is Memory_FS__File__Type__Json
            test_content         = b'raw bytes content'
            test_content_as_json = b'"raw bytes content"'
            self.file.create__content(test_content)
            assert _.bytes() != test_content                                            # todo: BUG: should be equal
            assert _.bytes() == test_content_as_json                                    # todo: BUG: review this use case (for example should we allow a raw bytes value in a Memory_FS__File__Type__Json object)

    def test_data(self):                                                                # Test data method (deserialized)
        with self.file_content as _:
            test_data = {"key": "value", "number": 42}
            self.file.save(test_data)

            assert _.data() == test_data                                                # Should deserialize JSON

    def test_data_with_text_file(self):                                                # Test data with text file type
        text_config = self.create_file_config(file_id   = 'text-file'       ,
                                              file_type = self.file_type_text)
        text_file   = self.create_test_file_from_config(text_config)
        text_content = File_FS__Content(file__config = text_config ,
                                        storage      = self.storage )

        plain_text = "This is plain text"
        text_file.save(plain_text)

        assert text_content.data() == plain_text                                       # Should return plain text

    def test_exists(self):                                                              # Test exists method
        with self.file_content as _:
            assert _.exists() is False

            self.file.create__content(b'some content')
            assert _.exists() is True

    # Helper method
    def create_test_file_from_config(self, config):                                    # Create a File_FS from config
        from memory_fs.file_fs.File_FS import File_FS
        return File_FS(file_config = config       ,
                       storage     = self.storage )
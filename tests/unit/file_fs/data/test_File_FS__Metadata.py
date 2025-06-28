from tests.unit.Base_Test__File_FS                          import Base_Test__File_FS
from memory_fs.file_fs.data.File_FS__Metadata               import File_FS__Metadata
from memory_fs.schemas.Schema__Memory_FS__File__Metadata    import Schema__Memory_FS__File__Metadata
from osbot_utils.helpers.safe_str.Safe_Str__Hash            import safe_str_hash


class test_File_FS__Metadata(Base_Test__File_FS):                                      # Test file metadata operations

    def setUp(self):                                                                    # Initialize test data
        super().setUp()
        self.file_metadata = File_FS__Metadata(file__config = self.file_config ,
                                               storage_fs   = self.storage_fs      )

    def test__init__(self):                                                             # Test initialization
        with self.file_metadata as _:
            assert type(_)         is File_FS__Metadata
            assert _.file__config  == self.file_config
            assert _.storage_fs       == self.storage_fs

    def test_metadata_no_content(self):                                                # Test metadata when no content exists
        with self.file_metadata as _:
            metadata = _.metadata()
            assert type(metadata)      is Schema__Memory_FS__File__Metadata
            assert metadata.content__hash is None                                       # No hash when no content

    def test_metadata_with_content(self):                                              # Test metadata when content exists
        test_content = b'test content for metadata'
        self.file.create__content(test_content)

        with self.file_metadata as _:
            metadata = _.metadata()
            assert type(metadata) is Schema__Memory_FS__File__Metadata

            # Note: JSON encoding wraps in quotes
            expected_hash = safe_str_hash('"test content for metadata"')
            assert metadata.content__hash == expected_hash
from osbot_utils.utils.Objects                              import __
from osbot_utils.helpers.safe_str.Safe_Str__File__Path      import Safe_Str__File__Path
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

    def test__exists__create__load__delete(self):
        with self.file_metadata as _:
            assert safe_str_hash(self.default_content)          == '9473fdd0d8'
            assert _.exists()                                   is False
            assert _.paths()                                    == [Safe_Str__File__Path('test-file.json.metadata')]
            assert _.create(content=self.default_content)       == ['test-file.json.metadata']                          # first call to create should create the files
            assert _.create(content=self.default_content)       == []                                                   # next call should not do anything
            assert _.exists()                                   is True
            with _.load() as file_metadata_1:                                                                           # this is needed because we need the .timestamp value in the test below
                assert file_metadata_1.obj()                    == __(content__hash         = '9473fdd0d8',
                                                                      chain_hash            = None        ,             # Not implemented (at the moment)
                                                                      previous_version_path = None        ,             # Not implemented (at the moment)
                                                                      content__size         = 12          ,
                                                                      tags                  = []          ,
                                                                      timestamp             = file_metadata_1.timestamp)
            assert _.delete()                                   == ['test-file.json.metadata']
            assert _.exists()                                   is False
            with _.load() as file_metadata_2:
                assert file_metadata_2.obj()                    == __(content__hash         = None        ,             # confirm we are now getting a default value
                                                                      chain_hash            = None        ,
                                                                      previous_version_path = None        ,
                                                                      content__size         = 0           ,
                                                                      tags                  = []          ,
                                                                      timestamp             = file_metadata_2.timestamp)



    def test_metadata_no_content(self):                                                # Test metadata when no content exists
        with self.file_metadata as _:
            metadata = _.load()
            assert type(metadata)      is Schema__Memory_FS__File__Metadata
            assert metadata.content__hash is None                                       # No hash when no content

    def test_metadata_with_content(self):                                              # Test metadata when content exists
        test_content = 'test content for metadata'
        self.file.create(test_content)

        with self.file_metadata as _:
            metadata = _.load()
            assert type(metadata) is Schema__Memory_FS__File__Metadata

            expected_hash = safe_str_hash('"test content for metadata"')            # Note: JSON encoding wraps in quotes
            assert metadata.content__hash == expected_hash
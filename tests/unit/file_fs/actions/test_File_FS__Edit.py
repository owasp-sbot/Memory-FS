from osbot_utils.helpers.safe_str.Safe_Str__File__Path  import Safe_Str__File__Path
from tests.unit.Base_Test__File_FS                      import Base_Test__File_FS
from memory_fs.file_fs.actions.File_FS__Edit            import File_FS__Edit


class test_File_FS__Edit(Base_Test__File_FS):                                           # Test file editing operations

    def setUp(self):                                                                    # Initialize test data
        super().setUp()
        self.file_edit = self.file.file_fs__edit()

    def test__init__(self):                                                             # Test initialization
        with self.file_edit as _:
            assert type(_)                    is File_FS__Edit
            assert _.file__config             == self.file_config
            assert _.storage_fs               == self.storage_fs

    def test_save__content(self):                                                       # Test saving content
        with self.file_edit as _:
            content = 'this is some content'
            result  = _.save__content(content)
            assert result            == [f'{self.file_config.file_id}.json'         ,
                                         f'{self.file_config.file_id}.json.metadata']
            assert _.load__content() == content

    def test_save__content_multiple_paths(self):                                       # Test saving content to multiple paths
        self.file_config.file_paths = ['path1', 'path2']

        with File_FS__Edit(file__config = self.file_config ,
                           storage_fs   = self.storage_fs  ) as _:
            content              = 'multi-path content'
            content__saved_bytes = b'"multi-path content"'          # since the data is being saved as a json string
            result               = _.save__content(content)

            assert sorted(result) == sorted(['path1/test-file.json'         ,
                                             'path1/test-file.json.metadata',
                                             'path2/test-file.json'         ,
                                             'path2/test-file.json.metadata'])

            # Verify content saved to both paths
            assert self.storage_fs.file__bytes(Safe_Str__File__Path('path1/test-file.json')) == content__saved_bytes
            assert self.storage_fs.file__bytes(Safe_Str__File__Path('path2/test-file.json')) == content__saved_bytes

    def test_load__content(self):                                                       # Test loading content
        with self.file_edit as _:
            assert _.load__content() is None                                            # No content yet
            content = 'test content to load'
            _.save__content(content)
            assert _.load__content() == content

    def test__regression__save__is_not_handling_null_extensions(self):                           # Test null extension handling
        with self.file_edit as _:
            assert _.save__content(b'') == [f'{self.file_config.file_id}.json'         ,         # when saving content we should update both file and it's metadata
                                            f'{self.file_config.file_id}.json.metadata',]        # Should handle empty content
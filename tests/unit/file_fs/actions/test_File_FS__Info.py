from osbot_utils.type_safe.primitives.domains.cryptography.safe_str.Safe_Str__Hash   import safe_str_hash
from osbot_utils.type_safe.primitives.domains.files.safe_str.Safe_Str__File__Path    import Safe_Str__File__Path
from memory_fs.file_fs.File_FS                                                       import File_FS
from memory_fs.schemas.Safe_Str__Cache_Hash                                          import Safe_Str__Cache_Hash
from tests.unit.Base_Test__File_FS                                                   import Base_Test__File_FS
from memory_fs.file_fs.actions.File_FS__Info                                         import File_FS__Info
from osbot_utils.type_safe.primitives.domains.identifiers.Safe_Id                    import Safe_Id

# todo: review performance impact of these tests (and methods used), since they are taking ~10ms to ~15ms to execute (which is a significant % of the current test suite)

class test_File_FS__Info(Base_Test__File_FS):                                          # Test file info operations

    def setUp(self):                                                                    # Initialize test data
        super().setUp()
        self.file_info = File_FS__Info(file__config = self.file_config ,
                                       storage_fs   = self.storage_fs      )

    def test__init__(self):                                                             # Test initialization
        with self.file_info as _:
            assert type(_)         is File_FS__Info
            assert _.file__config  == self.file_config
            assert _.storage_fs    == self.storage_fs

    def test_info_no_file(self):                                                       # Test info when file doesn't exist
        with self.file_info as _:
            assert _.info() is None

    def test_info_with_file(self):                                                     # Test info when file exists
        test_content = 'test content'
        assert self.file.create(file_data=test_content) == [Safe_Str__File__Path('test-file.json'         ),
                                                            Safe_Str__File__Path('test-file.json.config'  ),
                                                            Safe_Str__File__Path('test-file.json.metadata')]

        with self.file_info as _:
            info = _.info()
            assert type(info) is dict                                                   # todo: Should be strongly typed

            assert info[Safe_Id("exists")]       is True
            assert info[Safe_Id("content_type")] == "application/json; charset=utf-8"
            assert info[Safe_Id("content_hash")] == Safe_Str__Cache_Hash(safe_str_hash(f'"{test_content}"') )         # todo: see the side effects that the hash is of the serialised test_content and not the actually value
            assert info[Safe_Id("size"        )] == len(test_content) + 2                       # size contains the padded "
            assert info[Safe_Id("size"        )] == 12  + 2

    def test_info_different_file_types(self):                                           # Test info with different file types
        # Test with text file
        text_config = self.create_file_config(file_id   = 'text-file'       ,
                                              file_type = self.file_type_text)
        text_file   = self.create_test_file_from_config(text_config)
        text_info   = File_FS__Info(file__config = text_config ,
                                    storage_fs   = self.storage_fs )

        text_file.create(b'plain text')

        info = text_info.info()
        assert info[Safe_Id("content_type")] == "text/plain; charset=utf-8"

    # Helper method
    #   todo: see if we really need this, or if we should have this in Base_Test__File_FS
    def create_test_file_from_config(self, config):                                     # Create a File_FS from config
        return File_FS(file__config = config       ,
                       storage_fs   = self.storage_fs )
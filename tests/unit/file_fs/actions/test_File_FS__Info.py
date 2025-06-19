from memory_fs.file_fs.File_FS                              import File_FS
from tests.unit.Base_Test__File_FS                          import Base_Test__File_FS
from memory_fs.file_fs.actions.File_FS__Info                import File_FS__Info
from osbot_utils.helpers.Safe_Id                            import Safe_Id
from osbot_utils.helpers.safe_str.Safe_Str__Hash            import safe_str_hash

class test_File_FS__Info(Base_Test__File_FS):                                          # Test file info operations

    def setUp(self):                                                                    # Initialize test data
        super().setUp()
        self.file_info = File_FS__Info(file__config = self.file_config ,
                                       storage      = self.storage      )

    def test__init__(self):                                                             # Test initialization
        with self.file_info as _:
            assert type(_)         is File_FS__Info
            assert _.file__config  == self.file_config
            assert _.storage       == self.storage

    def test_info_no_file(self):                                                       # Test info when file doesn't exist
        with self.file_info as _:
            assert _.info() is None

    def test_info_with_file(self):                                                     # Test info when file exists
        test_content = b'test content'
        self.file.create()
        self.file.create__content(test_content)

        with self.file_info as _:
            info = _.info()
            assert type(info) is dict                                                   # todo: Should be strongly typed

            assert info[Safe_Id("exists")]       is True
            assert info[Safe_Id("content_type")] == "application/json; charset=utf-8"
            assert info[Safe_Id("content_hash")] == safe_str_hash('"test content"')

            # BUG: Size is not being captured properly
            assert info[Safe_Id("size")] != len(test_content)
            assert info[Safe_Id("size")] == 0                                           # Current bug

    def test_info_different_file_types(self):                                           # Test info with different file types
        # Test with text file
        text_config = self.create_file_config(file_id   = 'text-file'       ,
                                              file_type = self.file_type_text)
        text_file   = self.create_test_file_from_config(text_config)
        text_info   = File_FS__Info(file__config = text_config ,
                                    storage      = self.storage )

        text_file.create()
        text_file.create__content(b'plain text')

        info = text_info.info()
        assert info[Safe_Id("content_type")] == "text/plain; charset=utf-8"

    # Helper method
    #   todo: see if we really need this, or if we should have this in Base_Test__File_FS
    def create_test_file_from_config(self, config):                                     # Create a File_FS from config
        return File_FS(file_config = config       ,
                       storage     = self.storage )
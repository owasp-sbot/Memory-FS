from unittest                                               import TestCase
from memory_fs.file_fs.File_FS                              import File_FS
from memory_fs.schemas.Schema__Memory_FS__File__Type        import Schema__Memory_FS__File__Type
from memory_fs.storage_fs.providers.Storage_FS__Memory      import Storage_FS__Memory
from memory_fs.schemas.Schema__Memory_FS__File__Config      import Schema__Memory_FS__File__Config
from memory_fs.file_types.Memory_FS__File__Type__Json       import Memory_FS__File__Type__Json
from memory_fs.file_types.Memory_FS__File__Type__Text       import Memory_FS__File__Type__Text


class Base_Test__File_FS(TestCase):                                                             # Base test class for File_FS tests with common setup

    @classmethod
    def setUpClass(cls):                                                                        # Setup common File_FS infrastructure
        cls.storage_fs             = Storage_FS__Memory()
        cls.file_type_json         = Memory_FS__File__Type__Json()
        cls.file_type_text         = Memory_FS__File__Type__Text()
        cls.default_file_id        = 'test-file'
        cls.default_content        = b'test content'

    def setUp(self):                                                                            # Clear storage and create fresh file for each test
        self.storage_fs.clear()
        self.file_config = self.create_file_config()
        self.file        = File_FS(file__config = self.file_config ,
                                   storage_fs   = self.storage_fs  )

    def create_file_config(self, file_id    : str                           = None ,            # Helper to create file configuration
                                 file_type  : Schema__Memory_FS__File__Type = None ,
                                 file_paths : list                          = None):
        return Schema__Memory_FS__File__Config(file_id    = file_id    or self.default_file_id ,
                                               file_type  = file_type  or self.file_type_json  ,
                                               file_paths = file_paths or []                   )

    def create_and_save_file(self, content : bytes = None                                       # Helper to create and save a file with content
                              ):
        self.file.create()
        if content is not None:
            self.file.create__content(content)
        else:
            self.file.create__content(self.default_content)
        return self.file

    def assert_file_exists(self, exists : bool = True):                                         # Helper assertion for file existence
        assert self.file.exists() is exists

    def assert_content_equals(self, expected_content : bytes):                                  # Helper assertion for file content
        assert self.file.content() == expected_content
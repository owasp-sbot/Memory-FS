from unittest                                           import TestCase
from memory_fs.Memory_FS                                import Memory_FS
from memory_fs.file_fs.File_FS                          import File_FS
from memory_fs.schemas.Schema__Memory_FS__File__Config import Schema__Memory_FS__File__Config
from memory_fs.storage_fs.providers.Storage_FS__Memory  import Storage_FS__Memory


class Base_Test__Memory_FS(TestCase):                               # Base test class for Memory_FS tests with common setup

    @classmethod
    def setUpClass(cls):                                            # Setup common Memory_FS infrastructure
        cls.memory_fs = Memory_FS()
        cls.setup_memory_storage()

    @classmethod
    def setup_memory_storage(cls):                                  # Configure in-memory storage for tests
        storage_fs                       = Storage_FS__Memory()
        cls.memory_fs.storage.storage_fs = storage_fs
        cls.storage_fs = storage_fs

    def setUp(self):                                                # Clear storage before each test
        self.storage_fs.clear()

    def create_test_file(self, file_id: str   = 'test-file',        # Helper to create a test file
                               content: bytes = b'test content'):

        config  = Schema__Memory_FS__File__Config(file_id=file_id)
        file_fs = File_FS                        (file_config=config, storage=self.memory_fs.storage)

        if content:
            file_fs.create()
            file_fs.create__content(content)

        return file_fs
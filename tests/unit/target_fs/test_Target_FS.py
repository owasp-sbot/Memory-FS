from unittest                                               import TestCase
from memory_fs.storage_fs.providers.Storage_FS__Memory      import Storage_FS__Memory
from osbot_utils.helpers.safe_str.Safe_Str__Hash            import safe_str_hash
from memory_fs.schemas.Schema__Memory_FS__File__Metadata    import Schema__Memory_FS__File__Metadata
from osbot_utils.helpers.safe_int.Safe_UInt__FileSize       import Safe_UInt__FileSize
from osbot_utils.utils.Objects                              import __
from memory_fs.target_fs.Target_FS__Create                  import Target_FS__Create
from osbot_utils.helpers.safe_str.Safe_Str__File__Path      import Safe_Str__File__Path
from memory_fs.Memory_FS                                    import Memory_FS
from memory_fs.file_fs.File_FS                              import File_FS
from memory_fs.file_fs.actions.File_FS__Name                import FILE_EXTENSION__MEMORY_FS__FILE__CONFIG
from memory_fs.file_types.Memory_FS__File__Type__Json       import Memory_FS__File__Type__Json
from memory_fs.schemas.Schema__Memory_FS__File__Config      import Schema__Memory_FS__File__Config

class test_Target_FS(TestCase):

    def setUp(self):
        self.memory_fs          = Memory_FS()
        self.storage_fs         = Storage_FS__Memory()          # todo: find a better way to have this in-memory setup
        self.storage            = self.memory_fs.storage
        self.storage.storage_fs = self.storage_fs
        self.file_content       = b"test content"
        self.file_id            = 'an-file'
        self.file_type          = Memory_FS__File__Type__Json()
        self.test_config        = Schema__Memory_FS__File__Config  (file_id = self.file_id, file_type = self.file_type)
        self.test_content_bytes = b"test content"
        self.test_path          = Safe_Str__File__Path(f"an-file.json.{FILE_EXTENSION__MEMORY_FS__FILE__CONFIG}")
        self.file_fs            = File_FS(file_config=self.test_config, storage=self.storage)

        self.target_fs_create = Target_FS__Create(storage=self.storage)


    def test__load(self):                                                                         # Tests loading files

        assert self.target_fs_create.from_path__config(self.test_path) is None

        assert self.file_fs.create         (                               ) == [f'an-file.json.{FILE_EXTENSION__MEMORY_FS__FILE__CONFIG}']
        assert self.file_fs.create__content(content=self.test_content_bytes) == ['an-file.json']

        target_fs      = self.target_fs_create.from_path__config(self.test_path)
        loaded_file    = target_fs.file_fs()
        loaded_content = loaded_file.content()             #self.memory_fs__data.load_content(self.test_content_path)
        metadata       = loaded_file.metadata()

        assert type(loaded_file)                  is File_FS
        assert loaded_file.obj()                  == __(file_config = self.test_config.obj(),
                                                        storage     = self.storage.obj())
        assert type(loaded_content)               is bytes
        assert type(metadata)                     is Schema__Memory_FS__File__Metadata

        assert metadata.content__size != Safe_UInt__FileSize(len(self.test_content_bytes))                  # BUG
        assert metadata.content__size == 0                                                                  # BUG
        assert loaded_content         == b'"test content"'                                                  # todo: review these asserts (although I think the prob might be in this test, and not in the code logic)
        assert metadata.content__hash == safe_str_hash('"test content"')                                    # todo: review if '"test content"' is correct instead of just 'test content'

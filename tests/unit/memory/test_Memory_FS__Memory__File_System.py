from tests.unit.Base_Test__File_FS                          import Base_Test__File_FS
from memory_fs.file_fs.actions.File_FS__Name                import FILE_EXTENSION__MEMORY_FS__FILE__CONFIG
from osbot_utils.helpers.Safe_Id                            import Safe_Id
from osbot_utils.helpers.safe_str.Safe_Str__File__Path      import Safe_Str__File__Path
from osbot_utils.helpers.safe_str.Safe_Str__Hash            import safe_str_hash
from osbot_utils.helpers.safe_int.Safe_UInt__FileSize       import Safe_UInt__FileSize


# todo: review performance impact of these tests (and methods used), since they are taking ~10ms to ~15ms to execute (which is a significant % of the current test suite)

class test_Memory_FS__Memory__File_System(Base_Test__File_FS):                          # Using base class for optimization

    @classmethod
    def setUpClass(cls):                                                                # Class-level setup runs ONCE
        super().setUpClass()
        cls.test_path          = Safe_Str__File__Path(f"an-file.json.{FILE_EXTENSION__MEMORY_FS__FILE__CONFIG}")
        cls.test_content_path  = Safe_Str__File__Path("an-file.json")
        cls.test_content_bytes = b"test content"
        cls.file_id            = 'an-file'

    def setUp(self):                                                                    # Minimal per-test setup
        super().setUp()
        self.file_config.file_id = self.file_id                                        # Just update the ID

    def test_save_and_exists(self):                                                     # Tests saving files and checking existence
        assert self.file.exists         () is False
        assert self.file.exists__content() is False

        assert self.file.create         ()                                    == [self.test_path]
        assert self.file.create__content(content=self.test_content_bytes)    == [self.test_content_path]

        assert self.file.exists         () is True
        assert self.file.exists__content() is True

    def test__bug__load(self):                                                          # Tests loading files
        self.file.create()
        metadata = self.file.metadata()
        assert metadata.content__size != Safe_UInt__FileSize(len(self.test_content_bytes))  # BUG: size not captured

    def test_delete(self):                                                              # Tests deleting files
        assert self.file.create         ()                                    == [self.test_path]
        assert self.file.create__content(content=self.test_content_bytes)    == [self.test_content_path]
        assert self.file.exists         ()                                    is True
        assert self.file.exists__content()                                    is True

        assert self.file.delete         ()                                    == [self.test_path]
        assert self.file.delete__content()                                    == [self.test_content_path]
        assert self.file.exists         ()                                    is False
        assert self.file.exists__content()                                    is False

        assert self.file.delete         ()                                    == []     # Delete non-existent
        assert self.file.delete__content()                                    == []

    def test_list_files(self):                                                          # Tests listing files
        path_1         = Safe_Str__File__Path("folder1")
        path_2         = Safe_Str__File__Path("folder1/sub-folder-1")
        path_3         = Safe_Str__File__Path("folder2")
        full_file_name = f'an-file.json.{FILE_EXTENSION__MEMORY_FS__FILE__CONFIG}'

        # Test with path_1
        self.file.file_config.file_paths = [path_1]
        assert self.file.create() == [f'folder1/{full_file_name}']

        # Test with path_2
        self.file.file_config.file_paths = [path_2]
        assert self.file.create() == [f'folder1/sub-folder-1/{full_file_name}']

        # Test with path_3
        self.file.file_config.file_paths = [path_3]
        assert self.file.create() == [f'folder2/{full_file_name}']

        # Verify files list
        all_files = sorted(list(self.storage_fs.files__paths()))
        assert len(all_files) == 3
        assert all_files == [Safe_Str__File__Path('folder1/an-file.json.config'             ),
                             Safe_Str__File__Path('folder1/sub-folder-1/an-file.json.config'),
                             Safe_Str__File__Path('folder2/an-file.json.config'             )]

        # Test filtered list
        folder1_files = [p for p in all_files if str(p).startswith('folder1/')]
        assert len(folder1_files) == 2

    def test_get_file_info(self):                                                       # Tests getting file information
        assert self.file.info() is None

        assert self.file.create         ()                                 == [self.test_path]
        assert self.file.create__content(content=self.test_content_bytes) == [self.test_content_path]

        info = self.file.info()
        assert type(info)                    is dict                                    # BUG: should be strongly typed
        assert info[Safe_Id("exists")]       is True
        assert info[Safe_Id("size")]         != len(self.test_content_bytes)           # BUG: size issue
        assert info[Safe_Id("content_hash")] == safe_str_hash('"test content"')
        assert info[Safe_Id("content_type")] == "application/json; charset=utf-8"

    def test_clear(self):                                                               # Tests clearing all files
        assert self.file.create         ()                                 == [self.test_path]
        assert self.file.create__content(content=self.test_content_bytes) == [self.test_content_path]

        assert len(self.storage_fs.content_data) == 2                                   # Config and content

        self.storage_fs.clear()

        assert len(self.storage_fs.content_data) == 0
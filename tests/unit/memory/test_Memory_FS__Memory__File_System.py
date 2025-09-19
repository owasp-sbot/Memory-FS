from osbot_utils.type_safe.primitives.domains.cryptography.safe_str.Safe_Str__Hash          import safe_str_hash
from osbot_utils.type_safe.primitives.domains.files.safe_uint.Safe_UInt__FileSize           import Safe_UInt__FileSize
from osbot_utils.type_safe.primitives.domains.cryptography.safe_str.Safe_Str__Cache_Hash    import Safe_Str__Cache_Hash
from tests.unit.Base_Test__File_FS                                                          import Base_Test__File_FS
from memory_fs.file_fs.actions.File_FS__Name                                                import FILE_EXTENSION__MEMORY_FS__FILE__CONFIG, FILE_EXTENSION__MEMORY_FS__FILE__METADATA
from osbot_utils.type_safe.primitives.domains.identifiers.safe_str.Safe_Str__Id             import Safe_Str__Id
from osbot_utils.type_safe.primitives.domains.files.safe_str.Safe_Str__File__Path           import Safe_Str__File__Path


# todo: review performance impact of these tests (and methods used), since they are taking ~10ms to ~15ms to execute (which is a significant % of the current test suite)

class test_Memory_FS__Memory__File_System(Base_Test__File_FS):                          # Using base class for optimization

    @classmethod
    def setUpClass(cls):                                                                # Class-level setup runs ONCE
        super().setUpClass()
        cls.file_id          = "an-file"
        cls.test_content_path  = Safe_Str__File__Path(f"{cls.file_id}.json")
        cls.test_config_path   = Safe_Str__File__Path(f"{cls.file_id}.json.{FILE_EXTENSION__MEMORY_FS__FILE__CONFIG}")
        cls.test_metadata_path = Safe_Str__File__Path(f"{cls.file_id}.json.{FILE_EXTENSION__MEMORY_FS__FILE__METADATA}")
        cls.test_content_bytes = b"test content"
        cls.file_id            = 'an-file'

    def setUp(self):                                                                    # Minimal per-test setup
        super().setUp()
        self.file_config.file_id = self.file_id                                        # Just update the ID

    def test__bug__load(self):                                                          # Tests loading files
        self.file.create(file_data=self.test_content_bytes)
        metadata = self.file.metadata()
        assert metadata.content__size != Safe_UInt__FileSize(len(self.test_content_bytes))  # BUG: size not captured

    def test_delete(self):                                                              # Tests deleting files
        assert self.file.create(file_data=self.test_content_bytes)            == [self.test_content_path,
                                                                                  self.test_config_path ,
                                                                                  self.test_metadata_path
                                                                                  ]
        assert self.file.exists         ()                                    is True

        assert self.file.delete         ()                                    == [self.test_content_path  ,
                                                                                  self.test_config_path   ,
                                                                                  self.test_metadata_path ]
        assert self.file.exists         ()                                    is False

        assert self.file.delete         ()                                    == []     # Delete non-existent

    def test_list_files(self):                                                          # Tests listing files
        path_1         = Safe_Str__File__Path("folder1")
        path_2         = Safe_Str__File__Path("folder1/sub-folder-1")
        path_3         = Safe_Str__File__Path("folder2")
        full_file_name = f'an-file.json.{FILE_EXTENSION__MEMORY_FS__FILE__CONFIG}'

        # Test with path_1
        self.file.file__config.file_paths = [path_1]
        assert self.file.create() == [Safe_Str__File__Path('folder1/an-file.json'         ),
                                      Safe_Str__File__Path('folder1/an-file.json.config'  ),
                                      Safe_Str__File__Path('folder1/an-file.json.metadata')]

        # Test with path_2
        self.file.file__config.file_paths = [path_2]
        assert self.file.create() == [Safe_Str__File__Path('folder1/sub-folder-1/an-file.json'),
                                      Safe_Str__File__Path('folder1/sub-folder-1/an-file.json.config'),
                                      Safe_Str__File__Path('folder1/sub-folder-1/an-file.json.metadata')]

        # Test with path_3
        self.file.file__config.file_paths = [path_3]
        assert self.file.create() == [Safe_Str__File__Path('folder2/an-file.json'         ),
                                      Safe_Str__File__Path('folder2/an-file.json.config'  ),
                                      Safe_Str__File__Path('folder2/an-file.json.metadata')]

        # Verify files list
        all_files = sorted(list(self.storage_fs.files__paths()))
        assert len(all_files) == 9
        assert all_files == [Safe_Str__File__Path('folder1/an-file.json'),
                             Safe_Str__File__Path('folder1/an-file.json.config'),
                             Safe_Str__File__Path('folder1/an-file.json.metadata'),
                             Safe_Str__File__Path('folder1/sub-folder-1/an-file.json'),
                             Safe_Str__File__Path('folder1/sub-folder-1/an-file.json.config'),
                             Safe_Str__File__Path('folder1/sub-folder-1/an-file.json.metadata'),
                             Safe_Str__File__Path('folder2/an-file.json'),
                             Safe_Str__File__Path('folder2/an-file.json.config'),
                             Safe_Str__File__Path('folder2/an-file.json.metadata')]

        # Test filtered list
        folder1_files = [p for p in all_files if str(p).startswith('folder1/')]
        assert len(folder1_files) == 6

    def test_get_file_info(self):                                                       # Tests getting file information
        assert self.file.info() is None

        assert self.file.create(file_data=self.test_content_bytes) == [self.test_content_path ,
                                                                       self.test_config_path  ,
                                                                       self.test_metadata_path]

        info = self.file.info()
        assert type(info)                    is dict                                    # BUG: should be strongly typed
        assert info[Safe_Str__Id("exists")]       is True
        assert info[Safe_Str__Id("size")]         == len(self.test_content_bytes) + 2        # content size includes the serialised string
        assert info[Safe_Str__Id("content_hash")] == Safe_Str__Cache_Hash(safe_str_hash('"test content"'))
        assert info[Safe_Str__Id("content_type")] == "application/json; charset=utf-8"

    def test_clear(self):                                                               # Tests clearing all files
        assert self.file.create(file_data=self.test_content_bytes) == [self.test_content_path ,
                                                                       self.test_config_path  ,
                                                                       self.test_metadata_path]

        assert len(self.storage_fs.content_data) == 3                                   # Config,  content and metadata files

        self.storage_fs.clear()

        assert len(self.storage_fs.content_data) == 0
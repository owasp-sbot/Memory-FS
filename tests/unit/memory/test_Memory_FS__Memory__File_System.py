from unittest                                              import TestCase
from memory_fs.Memory_FS                                   import Memory_FS
from osbot_utils.type_safe.Type_Safe__Dict                 import Type_Safe__Dict
from osbot_utils.helpers.Safe_Id                           import Safe_Id
from osbot_utils.helpers.safe_str.Safe_Str__File__Path     import Safe_Str__File__Path
from osbot_utils.helpers.safe_str.Safe_Str__File__Name     import Safe_Str__File__Name
from osbot_utils.helpers.safe_str.Safe_Str__Hash           import safe_str_hash
from osbot_utils.helpers.safe_int.Safe_UInt__FileSize      import Safe_UInt__FileSize
from memory_fs.core.Memory_FS__File_System                 import Memory_FS__File_System
from memory_fs.schemas.Schema__Memory_FS__File             import Schema__Memory_FS__File
from memory_fs.schemas.Schema__Memory_FS__File__Config     import Schema__Memory_FS__File__Config
from memory_fs.schemas.Schema__Memory_FS__File__Content    import Schema__Memory_FS__File__Content
from memory_fs.schemas.Enum__Memory_FS__File__Content_Type import Enum__Memory_FS__File__Content_Type
from memory_fs.schemas.Enum__Memory_FS__File__Encoding     import Enum__Memory_FS__File__Encoding
from memory_fs.schemas.Schema__Memory_FS__File__Info       import Schema__Memory_FS__File__Info
from memory_fs.schemas.Schema__Memory_FS__File__Metadata   import Schema__Memory_FS__File__Metadata

# todo: all this logic needs to be refactored into the new Memory_FS__* classes
class test_Memory_FS__Memory__File_System(TestCase):

    def setUp(self):                                                                             # Initialize test data
        self.memory_fs          = Memory_FS()
        self.memory_fs__data    = self.memory_fs.data()
        self.memory_fs__edit    = self.memory_fs.edit()
        self.file_system        = self.memory_fs.file_system
        self.test_path          = Safe_Str__File__Path("test/folder/file.json")
        self.test_content_path  = Safe_Str__File__Path("test/folder/file.html")
        self.test_content_bytes = b"test content"

        # Create file components according to new schema
        self.test_file_content = Schema__Memory_FS__File__Content(size         = Safe_UInt__FileSize(len(self.test_content_bytes)),
                                                                  encoding     = Enum__Memory_FS__File__Encoding.UTF_8,
                                                                  content_path = self.test_content_path)
        self.test_file_info    = Schema__Memory_FS__File__Info   (file_name    = Safe_Str__File__Name("file.json"),
                                                                  file_ext     = Safe_Id             ("json"     ),
                                                                  content_type = Enum__Memory_FS__File__Content_Type.JSON,
                                                                  content      = self.test_file_content)
        self.test_config      = Schema__Memory_FS__File__Config  ()
        self.test_metadata    = Schema__Memory_FS__File__Metadata(paths         = {Safe_Id("test"): self.test_path},
                                                                  content_paths = {Safe_Id("test"): self.test_content_path},
                                                                  content_hash  = safe_str_hash("test content"   ),
                                                                  config        = self.test_config)
        self.test_file       = Schema__Memory_FS__File           (config        = self.test_config,
                                                                  info          = self.test_file_info,
                                                                  metadata      = self.test_metadata)

    def test_init(self):                                                                         # Tests basic initialization
        assert type(self.file_system             ) is Memory_FS__File_System
        assert type(self.file_system.files       ) is Type_Safe__Dict
        assert type(self.file_system.content_data) is Type_Safe__Dict
        assert len(self.file_system.files        ) == 0
        assert len(self.file_system.content_data ) == 0

    def test_save_and_exists(self):                                                             # Tests saving files and checking existence
        assert self.memory_fs__data.exists          (self.test_path                   ) is False
        assert self.memory_fs__data.exists_content  (self.test_content_path   ) is False

        assert self.memory_fs__edit.save            (self.test_path, self.test_file                         ) is True
        assert self.memory_fs__edit.save_content    (self.test_content_path, self.test_content_bytes) is True

        assert self.memory_fs__data.exists          (self.test_path                   ) is True
        assert self.memory_fs__data.exists_content  (self.test_content_path   ) is True

    def test_load(self):                                                                         # Tests loading files
        assert self.file_system.load(self.test_path                     ) is None
        assert self.file_system.load_content(self.test_content_path     ) is None

        self.memory_fs__edit.save(self.test_path, self.test_file)
        self.memory_fs__edit.save_content(self.test_content_path, self.test_content_bytes)

        loaded_file = self.file_system.load(self.test_path)
        loaded_content = self.file_system.load_content(self.test_content_path)

        assert loaded_file is self.test_file
        assert loaded_file.info.content.size == Safe_UInt__FileSize(len(self.test_content_bytes))
        assert loaded_file.metadata.content_hash == safe_str_hash("test content")
        assert loaded_content == self.test_content_bytes

    def test_delete(self):                                                                       # Tests deleting files
        self.memory_fs__edit.save        (self.test_path, self.test_file)
        self.memory_fs__edit.save_content(self.test_content_path, self.test_content_bytes)

        assert self.memory_fs__edit.delete          (self.test_path) is True
        assert self.memory_fs__edit.delete_content  (self.test_content_path) is True
        assert self.memory_fs__data.exists          (self.test_path) is False
        assert self.memory_fs__data.exists_content  (self.test_content_path) is False
        assert self.memory_fs__edit.delete          (self.test_path) is False                                # Delete non-existent file

    def test_list_files(self):                                                                   # Tests listing files
        path_1 = Safe_Str__File__Path("folder1/file1.json")
        path_2 = Safe_Str__File__Path("folder1/file2.json")
        path_3 = Safe_Str__File__Path("folder2/file3.json")

        self.memory_fs__edit.save(path_1, self.test_file)
        self.memory_fs__edit.save(path_2, self.test_file)
        self.memory_fs__edit.save(path_3, self.test_file)

        all_files     = self.memory_fs__data.list_files()
        folder1_files = self.memory_fs__data.list_files(Safe_Str__File__Path("folder1"))

        assert len(all_files)       == 3
        assert path_1               in all_files
        assert path_2               in all_files
        assert path_3               in all_files
        assert len(folder1_files)   == 2
        assert path_1               in folder1_files
        assert path_2               in folder1_files
        assert path_3           not in folder1_files

    def test_get_file_info(self):                                                                # Tests getting file information
        assert self.memory_fs__data.get_file_info(self.test_path) is None

        self.memory_fs__edit.save(self.test_path, self.test_file)
        info = self.memory_fs__data.get_file_info(self.test_path)

        assert info[Safe_Id("exists"      )] is True
        assert info[Safe_Id("size"        )] == len(self.test_content_bytes)
        assert info[Safe_Id("content_hash")] == safe_str_hash("test content")
        assert info[Safe_Id("timestamp"   )] == self.test_metadata.timestamp
        assert info[Safe_Id("content_type")] == "application/json; charset=utf-8"
        assert info[Safe_Id("paths"       )] == {Safe_Id("test"): self.test_path}

    def test_move(self):                                                                         # Tests moving files
        source_path         = Safe_Str__File__Path("source/file.json")
        source_content_path = Safe_Str__File__Path("source/file.html")
        dest_path           = Safe_Str__File__Path("destination/file.json")
        dest_content_path   = Safe_Str__File__Path("destination/file.html")

        self.memory_fs__edit.save        (source_path, self.test_file)
        self.memory_fs__edit.save_content(source_content_path, self.test_content_bytes)

        assert self.memory_fs__edit.move    (source_path, dest_path) is True
        assert self.memory_fs__data.exists  (source_path           ) is False
        assert self.memory_fs__data.exists  (dest_path             ) is True
        assert self.file_system.load        (dest_path             ) == self.test_file
        assert self.file_system.load        (dest_path      ).json() == self.test_file.json()

        # Content should not be moved automatically in this test since paths don't match
        assert self.memory_fs__edit.move(source_path, dest_path) is False                          # Move non-existent file

    def test_copy(self):                                                                         # Tests copying files
        source_path         = Safe_Str__File__Path("source/file.json")
        source_content_path = Safe_Str__File__Path("source/file.html")
        dest_path           = Safe_Str__File__Path("destination/file.json")

        self.memory_fs__edit.save(source_path, self.test_file)
        self.memory_fs__edit.save_content(source_content_path, self.test_content_bytes)

        assert self.memory_fs__edit.copy(source_path, dest_path) is True
        assert self.memory_fs__data.exists  (source_path           ) is True
        assert self.memory_fs__data.exists  (dest_path             ) is True
        assert self.file_system.load        (source_path           ) is self.test_file
        assert self.file_system.load        (dest_path             ) is self.test_file

        assert self.memory_fs__edit.copy(Safe_Str__File__Path("missing"), dest_path) is False      # Copy non-existent file

    def test_clear(self):                                                                        # Tests clearing all files and directories
        self.memory_fs__edit.save(Safe_Str__File__Path("file1.json"), self.test_file)
        self.memory_fs__edit.save(Safe_Str__File__Path("file2.json"), self.test_file)
        self.memory_fs__edit.save_content(Safe_Str__File__Path("file1.html"), self.test_content_bytes)

        assert len(self.file_system.files       ) > 0
        assert len(self.file_system.content_data) > 0

        self.file_system.clear()

        assert len(self.file_system.files       ) == 0
        assert len(self.file_system.content_data) == 0

    def test_stats(self):                                                                        # Tests file system statistics
        content_1 = b"short"
        content_2 = b"much longer content"

        file_content_1 = Schema__Memory_FS__File__Content(size         = Safe_UInt__FileSize(len(content_1)),
                                                          encoding     = Enum__Memory_FS__File__Encoding.UTF_8,
                                                          content_path = Safe_Str__File__Path("dir1/file1.txt"))

        file_content_2 = Schema__Memory_FS__File__Content(size         = len(content_2),
                                                          encoding     = Enum__Memory_FS__File__Encoding.UTF_8,
                                                          content_path = "dir2/file2.txt")

        file_info_1 = Schema__Memory_FS__File__Info(file_name    = Safe_Str__File__Name("file1.txt"),
                                                    file_ext     = Safe_Id("txt"),
                                                    content_type = Enum__Memory_FS__File__Content_Type.TXT,
                                                    content      = file_content_1)

        file_info_2 = Schema__Memory_FS__File__Info(file_name    ="file2.txt",
                                                    file_ext     = "txt",
                                                    content_type = Enum__Memory_FS__File__Content_Type.TXT,
                                                    content      = file_content_2)

        file_1 = Schema__Memory_FS__File(config   = self.test_config,
                                         info     = file_info_1,
                                         metadata = self.test_metadata)

        file_2 = Schema__Memory_FS__File(config   = self.test_config,
                                         info     = file_info_2,
                                         metadata = self.test_metadata)

        self.memory_fs__edit.save        (Safe_Str__File__Path("dir1/file1.txt.json"), file_1)
        self.memory_fs__edit.save        (Safe_Str__File__Path("dir2/file2.txt.json"), file_2)
        self.memory_fs__edit.save_content(Safe_Str__File__Path("dir1/file1.txt"     ), content_1)
        self.memory_fs__edit.save_content(Safe_Str__File__Path("dir2/file2.txt"     ), content_2)

        stats = self.file_system.stats()

        assert stats[Safe_Id("type"         )] == Safe_Id("memory")
        assert stats[Safe_Id("file_count"   )] == 2
        assert stats[Safe_Id("content_count")] == 2
        assert stats[Safe_Id("total_size"   )] == len(content_1) + len(content_2)

        assert type(stats) is dict
        assert stats       == { Safe_Id('content_count'): 2,
                                Safe_Id('file_count'   ): 2,
                                Safe_Id('total_size'   ): 24,
                                Safe_Id('type'): Safe_Id('memory')}

    def test__bug__filename_should_not_have_extension(self):
        with self.test_file_info as _:
            assert type(_) is Schema__Memory_FS__File__Info
            assert type(_.file_name) is     Safe_Str__File__Name            # BUG: this supports . (dots) in the file name
            assert type(_.file_name) is not Safe_Id                         # BUG: it is probably better to only allow filenames to be Safe_Id (which only supports r'[^a-zA-Z0-9_-]' )
from unittest                                               import TestCase
from osbot_utils.utils.Objects                              import __
from memory_fs.file_fs.File_FS                                 import File_FS
from memory_fs.Memory_FS                                    import Memory_FS
from memory_fs.file_fs.actions.File_FS__Exists                 import File_FS__Exists
from memory_fs.file_fs.actions.File_FS__Name                   import FILE_EXTENSION__MEMORY_FS__FILE__CONFIG
from memory_fs.file_types.Memory_FS__File__Type__Json       import Memory_FS__File__Type__Json
from memory_fs.file_types.Memory_FS__File__Type__Text       import Memory_FS__File__Type__Text
from memory_fs.storage_fs.providers.Storage_FS__Memory      import Storage_FS__Memory
from osbot_utils.type_safe.Type_Safe__Dict                  import Type_Safe__Dict
from osbot_utils.helpers.Safe_Id                            import Safe_Id
from osbot_utils.helpers.safe_str.Safe_Str__File__Path      import Safe_Str__File__Path
from osbot_utils.helpers.safe_str.Safe_Str__Hash            import safe_str_hash
from osbot_utils.helpers.safe_int.Safe_UInt__FileSize       import Safe_UInt__FileSize
from memory_fs.core.Memory_FS__File_System                  import Memory_FS__File_System
from memory_fs.schemas.Schema__Memory_FS__File              import Schema__Memory_FS__File
from memory_fs.schemas.Schema__Memory_FS__File__Config      import Schema__Memory_FS__File__Config
from memory_fs.schemas.Schema__Memory_FS__File__Metadata    import Schema__Memory_FS__File__Metadata

# todo: all this logic needs to be refactored into the new Memory_FS__* classes
class test_Memory_FS__Memory__File_System(TestCase):

    def setUp(self):                                                                             # Initialize test data
        self.memory_fs          = Memory_FS()
        self.memory_fs__data    = self.memory_fs.data()
        self.memory_fs__edit    = self.memory_fs.edit()
        self.storage            = self.memory_fs.storage
        self.file_system        = self.storage.file_system
        self.test_path          = Safe_Str__File__Path(f"an-file.json.{FILE_EXTENSION__MEMORY_FS__FILE__CONFIG}")
        self.test_content_path  = Safe_Str__File__Path("an-file.json")
        self.test_content_bytes = b"test content"

        # Create file components according to new schema
        self.file_content      = b"test content"
        self.file_id           = 'an-file'
        self.file_type         = Memory_FS__File__Type__Json()
        self.test_config       = Schema__Memory_FS__File__Config  (file_id       = self.file_id,
                                                                   file_type     = self.file_type)
        #self.test_metadata     = Schema__Memory_FS__File__Metadata(content__hash = safe_str_hash(self.file_content.decode()))
        self.test_file         = Schema__Memory_FS__File          (config        = self.test_config)

        self.test_file__exists = File_FS__Exists(file__config=self.test_config, storage=self.storage )

        self.storage_fs         = Storage_FS__Memory()          # todo: find a better way to have this in-memory setup
        self.storage.storage_fs = self.storage_fs
        self.file_fs            = File_FS(file_config=self.test_config, storage=self.storage)

    def test_init(self):                                                                         # Tests basic initialization
        assert type(self.file_system             ) is Memory_FS__File_System
        assert type(self.file_system.files       ) is Type_Safe__Dict
        assert type(self.file_system.content_data) is Type_Safe__Dict
        assert len(self.file_system.files        ) == 0
        assert len(self.file_system.content_data ) == 0

    def test_save_and_exists(self):                                                             # Tests saving files and checking existence
        assert self.file_fs.exists         () is False
        assert self.file_fs.exists__content() is False

        assert self.file_fs.create         (                               ) == [f'an-file.json.{FILE_EXTENSION__MEMORY_FS__FILE__CONFIG}']
        assert self.file_fs.create__content(content=self.test_content_bytes) == ['an-file.json']

        assert self.file_fs.exists          () is True
        assert self.file_fs.exists__content () is True


    def test__load(self):                                                                         # Tests loading files
        assert self.memory_fs__data.load        (self.test_path             ) is None

        assert self.file_fs.create         (                               ) == [f'an-file.json.{FILE_EXTENSION__MEMORY_FS__FILE__CONFIG}']
        assert self.file_fs.create__content(content=self.test_content_bytes) == ['an-file.json']

        loaded_file    = self.memory_fs__data.load        (self.test_path)
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

    def test__bug__load(self):  # Tests loading files
        self.file_fs.create()
        metadata = self.file_fs.metadata()
        assert metadata.content__size != Safe_UInt__FileSize(len(self.test_content_bytes)) # BUG: todo: bug the size is not being captured on the save action


    def test_delete(self):                                                                       # Tests deleting files
        with self.file_fs as _:
            assert _.create            (                               ) == [self.test_path        ]
            assert _.create__content   (content=self.test_content_bytes) == [self.test_content_path]
            assert _.exists            ()                                is True
            assert _.exists__content   ()                                is True
            assert _.delete            ()                                == [self.test_path        ]
            assert _.delete__content   ()                                == [self.test_content_path]
            assert _.exists            ()                                is False
            assert _.exists__content   ()                                is False
            assert _.delete            ()                                == []                                                      # Delete non-existent file
            assert _.delete__content   ()                                == []

    def test_list_files(self):                                                                   # Tests listing files
        with self.file_fs as _:
            path_1         = Safe_Str__File__Path("folder1")
            path_2         = Safe_Str__File__Path("folder1/sub-folder-1")
            path_3         = Safe_Str__File__Path("folder2")
            full_file_name = f'an-file.json.{FILE_EXTENSION__MEMORY_FS__FILE__CONFIG}'

            assert _.file_fs__create().file_fs__paths().file__config.file_paths == []

            _.file_config.file_paths = [path_1]                                                                                 # manually change this value

            assert _.file_fs__create().file_fs__paths().file__config.file_paths == [path_1]
            assert _.file_fs__create().file_fs__paths().paths()                 == [f'{path_1}/{full_file_name}']
            assert _.create()                                                   == [f'folder1/{full_file_name}']

            _.file_config.file_paths = [path_2]                                                                                 # manually change this value
            assert _.create()                                                   == [f'folder1/sub-folder-1/{full_file_name}']

            _.file_config.file_paths = [path_3]                                                                                 # manually change this value
            assert _.create()                                                   == [f'folder2/{full_file_name}']
            assert self.test_config.file_paths == _.file_config.file_paths


        all_files     = self.memory_fs__data.list_files()
        folder1_files = self.memory_fs__data.list_files(Safe_Str__File__Path("folder1"))


        assert len(all_files)                == 3
        assert f"{path_1}/{full_file_name}"  in all_files
        assert f"{path_2}/{full_file_name}"  in all_files
        assert f"{path_3}/{full_file_name}"  in all_files
        assert all_files                     == [ Safe_Str__File__Path('folder1/an-file.json.config'             ),
                                                  Safe_Str__File__Path('folder1/sub-folder-1/an-file.json.config'),
                                                  Safe_Str__File__Path('folder2/an-file.json.config'             )]

        assert len(folder1_files)               == 2
        assert f"{path_1}/{full_file_name}"     in folder1_files
        assert f"{path_2}/{full_file_name}"     in folder1_files
        assert f"{path_3}/{full_file_name}" not in folder1_files

    # todo: refactor to test_File_FS__Info
    def test_get_file_info(self):                                                                # Tests getting file information
        assert self.file_fs.info              ()                                is None
        assert self.file_fs.create            (                               ) == [self.test_path        ]
        assert self.file_fs.create__content   (content=self.test_content_bytes) == [self.test_content_path]

        info = self.file_fs.info()
        assert type(info)                   is dict                                         # BUG: this should be a strongly typed class
        assert info[Safe_Id("exists"      )] is True
        assert info[Safe_Id("size"        )] != len(self.test_content_bytes)
        assert info[Safe_Id("content_hash")] == safe_str_hash('"test content"')               # todo: review if '"test content"' is correct instead of just 'test content'
        #assert info[Safe_Id("timestamp"   )] == self.test_metadata.timestamp               # todo: add check for metadata.timestamp
        assert info[Safe_Id("content_type")] == "application/json; charset=utf-8"

    # todo: see if we need this, since now that we have multiple paths support, the logic in the move is more complicated
    # def test_move(self):                                                                         # Tests moving files
    #     source_path         = Safe_Str__File__Path("source/file.json")
    #     source_content_path = Safe_Str__File__Path("source/file.html")
    #     dest_path           = Safe_Str__File__Path("destination/file.json")
    #     dest_content_path   = Safe_Str__File__Path("destination/file.html")
    #
    #     self.memory_fs__edit.save        (source_path, self.test_file)
    #     self.memory_fs__edit.save_content(source_content_path, self.test_content_bytes)
    #
    #     assert self.memory_fs__edit.move    (source_path, dest_path) is True
    #     assert self.memory_fs__data.exists  (source_path           ) is False
    #     assert self.memory_fs__data.exists  (dest_path             ) is True
    #     assert self.memory_fs__data.load    (dest_path             ) == self.test_file
    #     assert self.memory_fs__data.load    (dest_path      ).json() == self.test_file.json()
    #
    #     # Content should not be moved automatically in this test since paths don't match
    #     assert self.memory_fs__edit.move(source_path, dest_path) is False                          # Move non-existent file

    # todo: see if we need this, since now that we have multiple paths support, the logic in the copy is more complicated

    # def test_copy(self):                                                                         # Tests copying files
    #     source_path         = Safe_Str__File__Path("source/file.json")
    #     source_content_path = Safe_Str__File__Path("source/file.html")
    #     dest_path           = Safe_Str__File__Path("destination/file.json")
    #
    #     self.memory_fs__edit.save(source_path, self.test_file)
    #     self.memory_fs__edit.save_content(source_content_path, self.test_content_bytes)
    #
    #     assert self.memory_fs__edit.copy(source_path, dest_path) is True
    #     assert self.memory_fs__data.exists  (source_path           ) is True
    #     assert self.memory_fs__data.exists  (dest_path             ) is True
    #     assert self.memory_fs__data.load    (source_path           ) is self.test_file
    #     assert self.memory_fs__data.load    (dest_path             ) is self.test_file
    #
    #     assert self.memory_fs__edit.copy(Safe_Str__File__Path("missing"), dest_path) is False      # Copy non-existent file

    def test_clear(self):                                                                        # Tests clearing all files and directories
        assert self.file_fs.create            (                               ) == [self.test_path        ]
        assert self.file_fs.create__content   (content=self.test_content_bytes) == [self.test_content_path]

        assert len(self.storage_fs.content_data ) == 2              # one for config and one for content

        self.memory_fs__edit.clear()                                # delete the entire db

        assert len(self.storage_fs.content_data) == 0

    def test_stats(self):                                                                        # Tests file system statistics
        content_1 = b"short"
        content_2 = b"much longer content"

        test_config_1    = Schema__Memory_FS__File__Config  (file_id       = "file-1",
                                                             file_type     = Memory_FS__File__Type__Text()  )
        # test_metadata_1  = Schema__Memory_FS__File__Metadata(content__hash = safe_str_hash("test content"   ),
        #                                                      content__size = Safe_UInt__FileSize(len(content_1)))

        test_config_2    = Schema__Memory_FS__File__Config  (file_id       = "file-2"                       ,
                                                             file_type     = Memory_FS__File__Type__Text()  )
        # test_metadata_2  = Schema__Memory_FS__File__Metadata(content__hash = safe_str_hash("test content"   ),
        #                                                      content__size = len(content_2))




        # file_1 = Schema__Memory_FS__File(config   = test_config_1)
        #
        # file_2 = Schema__Memory_FS__File(config   = test_config_2)

        with File_FS(file_config=test_config_1, storage=self.storage) as _:
            assert _.create         (                   ) == [f'file-1.txt.{FILE_EXTENSION__MEMORY_FS__FILE__CONFIG}']
            assert _.create__content(content = content_1) == ['file-1.txt']

        with File_FS(file_config=test_config_2, storage=self.storage) as _:
            assert _.create         (                   ) == [f'file-2.txt.{FILE_EXTENSION__MEMORY_FS__FILE__CONFIG}']
            assert _.create__content(content = content_2) == ['file-2.txt']

        stats = self.memory_fs__data.stats()

        assert stats[Safe_Id("type"         )] == Safe_Id("memory")
        assert stats[Safe_Id("file_count"   )] == 4
        assert stats[Safe_Id("total_size"   )] == len(content_1) + len(content_2) + 6           # todo: figure out where these extra 6 is coming from (which I think is from the json serialisation of the string )

        assert type(stats) is dict
        assert stats       == { Safe_Id('file_count'   ): 4,
                                Safe_Id('total_size'   ): 30,
                                Safe_Id('type'         ): Safe_Id('memory')}

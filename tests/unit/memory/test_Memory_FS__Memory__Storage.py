from unittest                                                import TestCase
from memory_fs.schemas.Enum__Memory_FS__File__Encoding       import Enum__Memory_FS__File__Encoding
from memory_fs.schemas.Schema__Memory_FS__File               import Schema__Memory_FS__File
from memory_fs.Memory_FS                                     import Memory_FS
from memory_fs.path_handlers.Path__Handler__Latest           import Path__Handler__Latest
from memory_fs.path_handlers.Path__Handler__Temporal         import Path__Handler__Temporal
from osbot_utils.helpers.Safe_Id                             import Safe_Id
from osbot_utils.helpers.safe_str.Safe_Str__File__Path       import Safe_Str__File__Path
from memory_fs.schemas.Schema__Memory_FS__File__Config       import Schema__Memory_FS__File__Config
from memory_fs.file_types.Memory_FS__File__Type__Json        import Memory_FS__File__Type__Json
from memory_fs.file_types.Memory_FS__File__Type__Markdown    import Memory_FS__File__Type__Markdown
from memory_fs.file_types.Memory_FS__File__Type__Html        import Memory_FS__File__Type__Html
from memory_fs.file_types.Memory_FS__File__Type__Png         import Memory_FS__File__Type__Png


class test_Memory_FS__Memory__Storage(TestCase):

    def setUp(self):                                                                             # Initialize test data
        self.memory_fs          = Memory_FS()
        self.memory_fs__data    = self.memory_fs.data   ()
        self.memory_fs__delete  = self.memory_fs.delete ()
        self.memory_fs__edit    = self.memory_fs.edit   ()
        self.memory_fs__exists  = self.memory_fs.exists ()
        self.memory_fs__load    = self.memory_fs.load   ()
        self.memory_fs__save    = self.memory_fs.save   ()
        self.file_system        = self.memory_fs.storage.file_system

        # Create file types
        self.file_type_json     = Memory_FS__File__Type__Json    ()
        self.file_type_markdown = Memory_FS__File__Type__Markdown()
        self.file_type_html     = Memory_FS__File__Type__Html    ()
        self.file_type_png      = Memory_FS__File__Type__Png     ()

        self.file_name          = Safe_Id("an-file")
        self.file_paths         = [Path__Handler__Latest  ().generate_path(),
                                   Path__Handler__Temporal().generate_path()]

        self.test_config = Schema__Memory_FS__File__Config(file_paths = self.file_paths     ,
                                                           file_name  = self.file_name      ,
                                                           file_type  = self.file_type_json )

        self.test_data                 = "test content"
        self.path_now                  = Path__Handler__Temporal().path_now()
        self.file_id__latest__content  = Safe_Str__File__Path('latest/an-file.json'                  )
        self.file_id__latest__metadata = Safe_Str__File__Path('latest/an-file.json.fs.json'          )
        self.file_id__now__content     = Safe_Str__File__Path(f'{self.path_now}/an-file.json'        )
        self.file_id__now__metadata    = Safe_Str__File__Path(f'{self.path_now}/an-file.json.fs.json')

    def test_save_string_data_as_json(self):                                                    # Tests saving string data with JSON file type
        saved_paths               = self.memory_fs__save.save(self.test_data, self.test_config)

        assert saved_paths       == [self.file_id__latest__metadata ,
                                     self.file_id__latest__content  ,
                                     self.file_id__now__metadata    ,
                                     self.file_id__now__content     ]
        assert len(saved_paths)  == 4

        # Verify metadata files were saved
        assert self.memory_fs__data.exists(self.file_id__latest__metadata       ) is True
        assert self.memory_fs__data.exists(self.file_id__now__metadata          ) is True

        # Verify content files were saved
        assert self.memory_fs__data.exists_content(self.file_id__latest__content) is True
        assert self.memory_fs__data.exists_content(self.file_id__now__content   ) is True

        #  Verify content was saved and is JSON formatted
        loaded_file   = self.memory_fs__data.load        (self.file_id__latest__metadata)
        content_bytes = self.memory_fs__data.load_content(self.file_id__latest__content)
        assert type(loaded_file) is Schema__Memory_FS__File
        assert content_bytes     == b'"test content"'       # JSON serialization should wrap string in quotes

    def test_save_dict_data_as_json(self):                                                      # Tests saving dict data with JSON file type
        test_dict = {"key": "value", "number": 42}
        saved_paths = self.memory_fs__save.save(test_dict, self.test_config)

        loaded_data = self.memory_fs__load.load_data(self.test_config)
        assert loaded_data      == test_dict
        assert len(saved_paths) == 4

    def test_save_string_data_as_markdown(self):                                               # Tests saving string data with Markdown file type
        config_markdown = Schema__Memory_FS__File__Config(file_name     = self.file_name         ,
                                                          file_paths    = self.file_paths        ,
                                                          file_type     = self.file_type_markdown)

        markdown_content = "# Test Header\n\nThis is a test."
        saved_paths      = self.memory_fs__save.save(markdown_content, config_markdown)
        assert saved_paths == [ 'latest/an-file.md.fs.json'          ,
                                'latest/an-file.md'                  ,
                                f'{self.path_now}/an-file.md.fs.json',
                                f'{self.path_now}/an-file.md'        ]

        # Verify content is saved as plain string (not JSON)
        loaded_data = self.memory_fs__load.load_data(config_markdown)
        assert loaded_data == markdown_content

    def test_save_html_content(self):                                                           # Tests saving HTML content
        config_html = Schema__Memory_FS__File__Config(file_name     = "index"     ,
                                                      file_paths    = self.file_paths    ,
                                                      file_type     = self.file_type_html)

        html_content = "<html><body><h1>Test</h1></body></html>"
        saved_paths = self.memory_fs__save.save(html_content, config_html)
        assert saved_paths == [ 'latest/index.html.fs.json'          ,
                                'latest/index.html'                  ,
                                f'{self.path_now}/index.html.fs.json',
                                f'{self.path_now}/index.html'        ]

        loaded_data = self.memory_fs__load.load_data(config_html)
        assert loaded_data == html_content

    def test_save_binary_data_as_png(self):                                                     # Tests saving binary data with PNG file type
        config_png = Schema__Memory_FS__File__Config(file_name     = "image"           ,
                                                     file_paths    = self.file_paths   ,
                                                     file_type     = self.file_type_png)

        # Simulate PNG data (just bytes for testing)
        png_data    = b"\x89PNG\r\n\x1a\n\x00\x00\x00\rIHDR"
        saved_paths = self.memory_fs__save.save(png_data, config_png, )
        assert saved_paths == [ 'latest/image.png.fs.json'          ,
                                'latest/image.png'                  ,
                                f'{self.path_now}/image.png.fs.json',
                                f'{self.path_now}/image.png'        ]


        # Verify binary data is preserved
        loaded_data = self.memory_fs__load.load_data(config_png)
        assert loaded_data == png_data

        # Verify encoding is BINARY
        assert self.file_type_png.encoding == Enum__Memory_FS__File__Encoding.BINARY

    def test_save_without_file_type_raises_error(self):                                        # Tests that saving without file type raises error
        config_no_type = Schema__Memory_FS__File__Config()

        with self.assertRaises(ValueError) as context:
            self.memory_fs__save.save(self.test_data, config_no_type)

        assert "file_config.file_type is required" in str(context.exception)

    def test_load_data_method(self):                                                            # Tests the new load_data method
        # Save different types of data
        test_data = {
            "string": "hello",
            "number": 123,
            "list": [1, 2, 3]
        }

        self.memory_fs__save.save(test_data, self.test_config)

        # Load using load_data
        loaded_data = self.memory_fs__load.load_data(self.test_config)
        assert loaded_data == test_data

    def test_file_type_properties_in_saved_file(self):                                         # Tests that file type properties are correctly saved
        saved_paths = self.memory_fs__save.save(self.test_data, self.test_config)
        loaded_file = self.memory_fs__load.load(self.test_config)
        assert type(loaded_file) is Schema__Memory_FS__File

        # Verify file info matches file type
        with loaded_file.config.file_type as _:
            assert _.file_extension == self.file_type_json.file_extension
            assert _.content_type   == self.file_type_json.content_type
            assert _.encoding       == self.file_type_json.encoding

    def test_exists_without_default_handler_all_must_exist(self):                               # Tests exists without default (all must exist)
        assert self.memory_fs__exists.exists(self.test_config) is False

        saved_paths = self.memory_fs__save.save(self.test_data, self.test_config)
        assert len(saved_paths) == 4

        assert self.memory_fs__exists.exists(self.test_config) is True

        # Delete one file - should now return False
        assert self.memory_fs__edit.delete(saved_paths[0]) is True
        assert self.memory_fs__exists.exists(self.test_config) is False

    def test_delete(self):                                                                       # Tests deleting files
        files_created = self.memory_fs__save.save(self.test_data, self.test_config)

        assert len(files_created) == 4

        file          = self.memory_fs__load.load(self.test_config)
        assert type(file) is Schema__Memory_FS__File

        files_deleted = self.memory_fs__delete.delete(self.test_config)

        assert sorted(files_created) == sorted(files_deleted)

        assert self.memory_fs__exists.exists(self.test_config) is False

    def test_empty_file_paths(self):                                                              # Tests behavior with no handlers
        empty_config = Schema__Memory_FS__File__Config(file_paths = []                 ,
                                                       file_type  = self.file_type_json)

        saved_paths = self.memory_fs__save.save(self.test_data, empty_config)
        assert len(saved_paths) == 0

        assert self.memory_fs__exists.exists(empty_config) is False
        assert self.memory_fs__load.load    (empty_config) is None

    def test_list_files(self):                                                                  # Tests listing files
        # Create configs with different file_types to avoid path collisions
        config_1 = Schema__Memory_FS__File__Config(file_name  = "file_1"              ,
                                                   file_paths = self.file_paths       ,
                                                   file_type  = self.file_type_json   )     # use json for config 1

        config_2 = Schema__Memory_FS__File__Config(file_name  = "file_2"                  ,
                                                   file_paths = self.file_paths           ,
                                                   file_type   = self.file_type_markdown) # use mardown for config 2

        self.memory_fs__save.save("content_1", config_1)
        self.memory_fs__save.save("content_2", config_2)

        all_files = self.memory_fs__data.list_files()           # todo figure out a better way to name this since these are the fs.json files (i.e. this all files doesn't include the content files, which could be an expectation)

        assert len(all_files) == 4
        assert sorted(all_files) == sorted([Safe_Str__File__Path('latest/file_1.json.fs.json'          ),
                                            Safe_Str__File__Path('latest/file_2.md.fs.json'            ),
                                            Safe_Str__File__Path(f'{self.path_now}/file_1.json.fs.json'),
                                            Safe_Str__File__Path(f'{self.path_now}/file_2.md.fs.json'  )])


    def test_clear(self):                                                                        # Tests clearing storage
        self.memory_fs__save.save("content1", self.test_config)

        assert len(self.memory_fs__data.list_files())     > 0
        assert len(self.file_system.content_data) > 0

        self.memory_fs__edit.clear()

        assert len(self.memory_fs__data.list_files())     == 0
        assert len(self.file_system.content_data) == 0

    def test_stats(self):                                                                        # Tests storage statistics
        config_1 = Schema__Memory_FS__File__Config(file_name  = "file_1"              ,
                                                   file_paths = self.file_paths       ,
                                                   file_type  = self.file_type_json   )

        config_2 = Schema__Memory_FS__File__Config(file_name  = "file_2"              ,
                                                   file_paths = self.file_paths       ,
                                                   file_type   = self.file_type_json  )

        self.memory_fs__save.save("short"              , config_1)
        self.memory_fs__save.save("much longer content", config_2)

        stats = self.memory_fs__data.stats()

        assert stats[Safe_Id("type")] == Safe_Id("memory")
        assert stats[Safe_Id("file_count"   )] == 4                                             # 4 = 2x metadata files * 2x file_paths
        assert stats[Safe_Id("content_count")] == 4                                             # 4 = 2x content files  * 2x file_paths
        # JSON serialization adds quotes, so sizes will be larger
        assert stats[Safe_Id("total_size")] > len("short") + len("much longer content")         # todo: double check this value
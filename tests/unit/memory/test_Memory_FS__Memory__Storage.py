from unittest                                                                      import TestCase
from memory_fs.file_fs.File_FS                                                     import File_FS
from memory_fs.file_fs.actions.File_FS__Name                                       import FILE_EXTENSION__MEMORY_FS__FILE__CONFIG, FILE_EXTENSION__MEMORY_FS__FILE__METADATA
from memory_fs.schemas.Enum__Memory_FS__File__Encoding                             import Enum__Memory_FS__File__Encoding
from memory_fs.path_handlers.Path__Handler__Latest                                 import Path__Handler__Latest
from memory_fs.path_handlers.Path__Handler__Temporal                               import Path__Handler__Temporal
from memory_fs.storage_fs.providers.Storage_FS__Memory                             import Storage_FS__Memory
from osbot_utils.type_safe.primitives.domains.identifiers.safe_str.Safe_Str__Id    import Safe_Str__Id
from osbot_utils.type_safe.primitives.domains.files.safe_str.Safe_Str__File__Path  import Safe_Str__File__Path
from memory_fs.schemas.Schema__Memory_FS__File__Config                             import Schema__Memory_FS__File__Config
from memory_fs.file_types.Memory_FS__File__Type__Json                              import Memory_FS__File__Type__Json
from memory_fs.file_types.Memory_FS__File__Type__Markdown                          import Memory_FS__File__Type__Markdown
from memory_fs.file_types.Memory_FS__File__Type__Html                              import Memory_FS__File__Type__Html
from memory_fs.file_types.Memory_FS__File__Type__Png                               import Memory_FS__File__Type__Png


# todo: review performance impact of these tests (and methods used), since they are taking ~30ms to ~40ms to execute (which is a significant % of the current test suite)
class test_Memory_FS__Memory__Storage(TestCase):

    # todo: refactor this to use @classmethod and only create one instance of storage_fs
    def setUp(self):                                                                             # Initialize test data
        self.storage_fs         = Storage_FS__Memory()

        # Create file types
        self.file_type_json     = Memory_FS__File__Type__Json    ()
        self.file_type_markdown = Memory_FS__File__Type__Markdown()
        self.file_type_html     = Memory_FS__File__Type__Html    ()
        self.file_type_png      = Memory_FS__File__Type__Png     ()

        self.file_id          = Safe_Str__Id("an-file")
        self.file_paths         = [Path__Handler__Latest  ().generate_path(),
                                   Path__Handler__Temporal().generate_path()]

        self.test_config = Schema__Memory_FS__File__Config(file_paths = self.file_paths     ,
                                                           file_id  = self.file_id      ,
                                                           file_type  = self.file_type_json )

        self.test_data                 = "test content"
        self.path_now                  = Path__Handler__Temporal().path_now()
        self.file_id__latest__content  = Safe_Str__File__Path( 'latest/an-file.json'                  )
        self.file_id__latest__config   = Safe_Str__File__Path(f'latest/an-file.json.{FILE_EXTENSION__MEMORY_FS__FILE__CONFIG}'          )
        self.file_id__latest__metadata = Safe_Str__File__Path(f'latest/an-file.json.{FILE_EXTENSION__MEMORY_FS__FILE__METADATA}'        )
        self.file_id__now__content     = Safe_Str__File__Path(f'{self.path_now}/an-file.json'         )
        self.file_id__now__config      = Safe_Str__File__Path(f'{self.path_now}/an-file.json.{FILE_EXTENSION__MEMORY_FS__FILE__CONFIG}'  )
        self.file_id__now__metadata    = Safe_Str__File__Path(f'{self.path_now}/an-file.json.{FILE_EXTENSION__MEMORY_FS__FILE__METADATA}')
        self.file_fs                   = File_FS(file__config=self.test_config, storage_fs=self.storage_fs)

    def test_save_string_data_as_json(self):                                                    # Tests saving string data with JSON file type
        with self.file_fs as _:
            saved_paths = _.create(self.test_data)

            assert type(_)                       is File_FS
            assert sorted(saved_paths)           == sorted([self.file_id__latest__config     ,
                                                            self.file_id__latest__content    ,
                                                            self.file_id__latest__metadata   ,
                                                            self.file_id__now__config        ,
                                                            self.file_id__now__content       ,
                                                            self.file_id__now__metadata      ])
            assert len(saved_paths)             == 6
            assert _.exists()                   is True                 # Verify metadata files were saved

            assert _.file_fs__content().bytes() == b'"test content"'
            assert _.content()                  == 'test content'        # data when loaded should have the correct type (in this case a string)

    def test_save_dict_data_as_json(self):                                                      # Tests saving dict data with JSON file type
        test_dict = {"key": "value", "number": 42}
        with self.file_fs as _:
            saved_paths = _.update(test_dict)

            assert saved_paths == sorted([Safe_Str__File__Path('latest/an-file.json'                   ),
                                          Safe_Str__File__Path(f'{self.path_now}/an-file.json'         ),
                                          Safe_Str__File__Path('latest/an-file.json.metadata'          ),
                                          Safe_Str__File__Path(f'{self.path_now}/an-file.json.metadata')])
            loaded_data = _.content()
            assert loaded_data      == test_dict

    def test_save_string_data_as_markdown(self):                                               # Tests saving string data with Markdown file type
        config_markdown = Schema__Memory_FS__File__Config(file_id     = self.file_id         ,
                                                          file_paths    = self.file_paths        ,
                                                          file_type     = self.file_type_markdown)

        with File_FS(file__config=config_markdown, storage_fs=self.storage_fs) as _:
            markdown_content = "# Test Header\n\nThis is a test."
            saved_paths      = _.update(markdown_content)
            assert saved_paths == sorted([ 'latest/an-file.md'                  ,
                                           f'{self.path_now}/an-file.md'         ,
                                            'latest/an-file.md.metadata'         ,
                                           f'{self.path_now}/an-file.md.metadata'])

            assert _.content() == markdown_content                      # confirm that round trip works

    def test_save_html_content(self):                                                           # Tests saving HTML content
        config_html = Schema__Memory_FS__File__Config(file_id     = "index"     ,
                                                      file_paths    = self.file_paths    ,
                                                      file_type     = self.file_type_html)

        with File_FS(file__config=config_html, storage_fs=self.storage_fs) as _:
            html_content = "<html><body><h1>Test</h1></body></html>"
            saved_paths = _.create(html_content)
            assert saved_paths == sorted([ f'latest/index.html.{FILE_EXTENSION__MEMORY_FS__FILE__CONFIG}'            ,
                                            'latest/index.html'                                                      ,
                                           f'latest/index.html.{FILE_EXTENSION__MEMORY_FS__FILE__METADATA}'          ,
                                           f'{self.path_now}/index.html.{FILE_EXTENSION__MEMORY_FS__FILE__CONFIG}'   ,
                                           f'{self.path_now}/index.html'                                             ,
                                           f'{self.path_now}/index.html.{FILE_EXTENSION__MEMORY_FS__FILE__METADATA}'])

            loaded_data = _.content()
            assert loaded_data == html_content

    def test_save_binary_data_as_png(self):                                                     # Tests saving binary data with PNG file type
        config_png = Schema__Memory_FS__File__Config(file_id     = "image"           ,
                                                     file_paths    = self.file_paths   ,
                                                     file_type     = self.file_type_png)

        with File_FS(file__config=config_png, storage_fs=self.storage_fs) as _:
            # Simulate PNG data (just bytes for testing)
            png_data    = b"\x89PNG\r\n\x1a\n\x00\x00\x00\rIHDR"
            saved_paths = _.create(png_data)
            assert saved_paths == sorted([ f'latest/image.png.config'           ,
                                            'latest/image.png'                  ,
                                            'latest/image.png.metadata'         ,
                                           f'{self.path_now}/image.png.config'  ,
                                           f'{self.path_now}/image.png'         ,
                                           f'{self.path_now}/image.png.metadata'])

            # Verify binary data is preserved
            loaded_data = _.content()
            assert loaded_data == png_data

            # Verify encoding is BINARY
            assert self.file_type_png.encoding == Enum__Memory_FS__File__Encoding.BINARY

    def test_save_without_file_type_raises_error(self):                                        # Tests that saving without file type raises error
        config_no_type = Schema__Memory_FS__File__Config()

        with File_FS(file__config=config_no_type, storage_fs=self.storage_fs) as file_fs:
            with self.assertRaises(ValueError) as context:
                file_fs.update(self.test_data)

            assert "Unknown serialization method: None" in str(context.exception)

    def test_data(self):                                                            # Tests the new load_data method
        # Save different types of data
        test_data = {
            "string": "hello",
            "number": 123,
            "list": [1, 2, 3]
        }

        with self.file_fs as _:
            _.update(test_data)

            # Load using load
            loaded_data = _.content()
            assert loaded_data == test_data

    def test_file_type_properties_in_saved_file(self):                                         # Tests that file type properties are correctly saved
        with self.file_fs as _:
            saved_paths = _.create(self.test_data)
            loaded_file = _.metadata()
            assert loaded_file is not None

            # Verify file info matches file type
            assert _.file__config.file_type.file_extension == self.file_type_json.file_extension
            assert _.file__config.file_type.content_type   == self.file_type_json.content_type
            assert _.file__config.file_type.encoding       == self.file_type_json.encoding

    def test_exists_without_default_handler_all_must_exist(self):                               # Tests exists without default (all must exist)
        with self.file_fs as _:
            assert _.exists() is False
            saved_paths = _.create(self.test_data)
            assert len(saved_paths) == 6
            assert _.exists()       is True
            assert _.delete()       == saved_paths
            assert _.exists()       is False                # Delete config - should now return False

    def test_delete(self):                                                                       # Tests deleting files
        with self.file_fs as _:
            files_created = _.create(self.test_data)

            assert len(files_created) == 6

            file = _.metadata()
            assert file is not None

            files_deleted = _.delete()

            assert sorted(files_created) == sorted(files_deleted)

            assert _.exists() is False

    def test_empty_file_paths(self):                                                              # Tests behavior with no handlers
        empty_config = Schema__Memory_FS__File__Config(file_paths = []                 ,
                                                         file_type  = self.file_type_json)
        with File_FS(file__config=empty_config, storage_fs=self.storage_fs) as file_fs:
            saved_paths  = file_fs.create(self.test_data)
            file_id    = empty_config.file_id
            assert len(saved_paths) == 3
            assert saved_paths      == [f'{file_id}.json',
                                        f'{file_id}.json.{FILE_EXTENSION__MEMORY_FS__FILE__CONFIG}'  ,
                                        f'{file_id}.json.{FILE_EXTENSION__MEMORY_FS__FILE__METADATA}']

            assert file_fs.exists() is True                            # confirm file was created
            assert file_fs.metadata() is not None                      # and we can get it

    # def test_list_files(self):                                                                  # Tests listing files
    #     # Create configs with different file_types to avoid path collisions
    #     config_1 = Schema__Memory_FS__File__Config(file_id  = "file_1"              ,
    #                                                file_paths = self.file_paths       ,
    #                                                file_type  = self.file_type_json   )     # use json for config 1
    #
    #     config_2 = Schema__Memory_FS__File__Config(file_id  = "file_2"                  ,
    #                                                file_paths = self.file_paths           ,
    #                                                file_type   = self.file_type_markdown) # use mardown for config 2
    #
    #     with File_FS(file_config=config_1, storage_fs=self.storage_fs) as file_fs_1:
    #         file_fs_1.create("content_1")
    #
    #     with File_FS(file_config=config_2, storage_fs=self.storage_fs) as file_fs_2:
    #         file_fs_2.create("content_2")
    #
    #     all_files = self.storage_fs.list_files()           # todo figure out a better way to name this since these are the {FILE_EXTENSION__MEMORY_FS__FILE__CONFIG} files (i.e. this all files doesn't include the content files, which could be an expectation)
    #
    #     assert len(all_files) == 8
    #     assert sorted(all_files) == sorted([Safe_Str__File__Path(f'latest/file_1.json'                                                                                  ),
    #                                         Safe_Str__File__Path(f'latest/file_1.json.{FILE_EXTENSION__MEMORY_FS__FILE__CONFIG}'         ),
    #                                         Safe_Str__File__Path(f'latest/file_2.md'                                                     ),
    #                                         Safe_Str__File__Path(f'latest/file_2.md.{FILE_EXTENSION__MEMORY_FS__FILE__CONFIG}'           ),
    #                                         Safe_Str__File__Path(f'{self.path_now}/file_1.json'                                          ),
    #                                         Safe_Str__File__Path(f'{self.path_now}/file_1.json.{FILE_EXTENSION__MEMORY_FS__FILE__CONFIG}'),
    #                                         Safe_Str__File__Path(f'{self.path_now}/file_2.md'                                            ),
    #                                         Safe_Str__File__Path(f'{self.path_now}/file_2.md.{FILE_EXTENSION__MEMORY_FS__FILE__CONFIG}'  )])

import json
from osbot_utils.testing.__ import __, __SKIP__
from osbot_utils.type_safe.primitives.domains.numerical.safe_float.Safe_Float__Percentage_Exact import Safe_Float__Percentage_Exact
from tests.unit.Base_Test__File_FS                                                              import Base_Test__File_FS
from osbot_utils.type_safe.primitives.domains.files.safe_str.Safe_Str__File__Path               import Safe_Str__File__Path
from memory_fs.file_fs.actions.File_FS__Create                                                  import File_FS__Create
from memory_fs.file_fs.File_FS                                                                  import File_FS
from memory_fs.file_types.Memory_FS__File__Type__Json                                           import Memory_FS__File__Type__Json
from memory_fs.file_types.Memory_FS__File__Type__Json__Single                                   import Memory_FS__File__Type__Json__Single
from memory_fs.schemas.Schema__Memory_FS__File__Config                                          import Schema__Memory_FS__File__Config


class test_File_FS__Create__json_single(Base_Test__File_FS):                      # Test single-file JSON creation

    def setUp(self):                                                              # Initialize test data
        super().setUp()                                                           # Create file config with single-file JSON type
        self.single_file_type = Memory_FS__File__Type__Json__Single()
        self.single_file_config = Schema__Memory_FS__File__Config(file_id   = 'test-single-file',
                                                                  file_type = self.single_file_type,
                                                                  file_paths = [])
        self.single_file = File_FS(file__config = self.single_file_config,
                                   storage_fs   = self.storage_fs        )
        self.single_file_create = self.single_file.file_fs__create()

    def test__init__(self):                                                       # Test initialization
        with self.single_file_create as _:
            assert type(_) is File_FS__Create
            assert _.file__config == self.single_file_config
            assert _.storage_fs == self.storage_fs
            assert type(_.file__config.file_type) is Memory_FS__File__Type__Json__Single

            assert self.single_file.obj() == __(file__config=__(exists_strategy='first',
                                                                file_id='test-single-file',
                                                                file_key='',
                                                                file_paths=[],
                                                                file_type=__(name='json_single',
                                                                             content_type='application/json; charset=utf-8',
                                                                             file_extension='json',
                                                                             encoding='utf-8',
                                                                             serialization='json')),
                                                storage_fs=__(content_data=__()))

    def test_create__single_file_only(self):                                     # Test that only content file is created
        test_data = {"key": "value", "number": 42}

        with self.single_file_create as _:

            assert _.file_fs__content ().exists() is False
            assert _.file_fs__config  ().exists() is False                      # Verify no files exist initially
            assert _.file_fs__content ().exists() is False
            assert _.file_fs__metadata().exists() is False

            files_created = _.create(test_data)                                 # Create the single file

            assert len(files_created) == 1                                      # Should only create one file (content)
            assert files_created      == ['test-single-file.json']

            content_path  = Safe_Str__File__Path('test-single-file.json'         )  # Verify only content file exists
            config_path   = Safe_Str__File__Path('test-single-file.json.config'  )
            metadata_path = Safe_Str__File__Path('test-single-file.json.metadata')

            assert self.storage_fs.file__exists(content_path ) is True      # content exists
            assert self.storage_fs.file__exists(config_path  ) is False     # No config
            assert self.storage_fs.file__exists(metadata_path) is False     # No metadata

            assert _.file_fs__config  ().exists() is False                  # correct since this file doesn't exist
            assert _.file_fs__content ().exists() is True                   # correct this file exists
            assert _.file_fs__metadata().exists() is False                  # correct this file shouldn't exist

            stored_data = self.storage_fs.file__json(content_path)          # Verify content is correct
            assert stored_data == test_data                                 # which confirms no side effects of not having a config and metadata files

            assert _.obj()     == __(file__config = __( exists_strategy = 'first'                        ,
                                                        file_id         = 'test-single-file'             ,
                                                        file_key        = ''                             ,
                                                        file_paths      = []                             ,
                                                        file_type       = __(name          = 'json_single'                      ,
                                                                              content_type  = 'application/json; charset=utf-8' ,
                                                                              file_extension= 'json'                            ,
                                                                              encoding      = 'utf-8'                           ,
                                                                              serialization = 'json'))                         ,

                                       storage_fs   = __(content_data = __(test_single_file_json = b'{\n  \"key\": \"value\",\n'
                                                                                                       b'  \"number\": 42\n}')))



    def test_create__with_paths(self):                                          # Test single file with path handlers
        self.single_file_config.file_paths = [ Safe_Str__File__Path('latest'),          # Add paths to config
                                               Safe_Str__File__Path('v1')    ]

        test_data = "test content"

        with self.single_file_create as _:
            files_created = _.create(test_data)

            # Should create single file in each path
            assert len(files_created) == 2
            assert sorted(files_created) == ['latest/test-single-file.json',
                                             'v1/test-single-file.json'    ]

            # Verify no config or metadata files in any path
            for path_prefix in ['latest', 'v1']:
                content_path = Safe_Str__File__Path(f'{path_prefix}/test-single-file.json')
                config_path = Safe_Str__File__Path(f'{path_prefix}/test-single-file.json.config')
                metadata_path = Safe_Str__File__Path(f'{path_prefix}/test-single-file.json.metadata')

                assert self.storage_fs.file__exists(content_path ) is True
                assert self.storage_fs.file__exists(config_path  ) is False
                assert self.storage_fs.file__exists(metadata_path) is False
                assert _.file_fs__config  ().exists() is False                  # correct since this file doesn't exist
                assert _.file_fs__content ().exists() is True                   # correct this file exists
                assert _.file_fs__metadata().exists() is False                  # correct this file shouldn't exist

            stored_data = self.storage_fs.file__json(content_path)          # Verify content is correct
            assert stored_data == test_data

    def test_storage_efficiency_comparison(self):                               # Compare storage footprint
        test_data = {"key": "value", "number": 42}

        regular_file = self.file                                                # Create regular JSON file
        regular_file.create(test_data)

        self.single_file.create(test_data)                                      # Create single JSON file

        with self.storage_fs.content_data as _:                                 # Check storage - regular should have 3x more entries

            regular_files = [k for k in _.keys() if 'test-file' in str(k)]      # Count files for each type
            single_files  = [k for k in _.keys() if 'test-single' in str(k)]

            assert len(regular_files) == 3                                      # .json, .json.config, .json.metadata
            assert len(single_files ) == 1                                      # .json only

        # confirm 66% reduction in storage entries (from 3 to 1)
        reduction = Safe_Float__Percentage_Exact(1 - len(single_files)/len(regular_files))      # use Safe_Float__Percentage_Exact to allow us to do the assert below :)
        assert reduction == 0.67                                                                # without Safe_Float__Percentage_Exact this value is 0.6666666666666667 :)

    def test_create__empty_data(self):                                          # Test creating with empty data
        with self.single_file_create as _:
            files_created = _.create({})

            assert len(files_created) == 1
            assert files_created == ['test-single-file.json']

            content = self.storage_fs.file__json(Safe_Str__File__Path('test-single-file.json'))         # Verify empty JSON object was stored
            assert content == {}

            assert _.file_fs__config  ().exists() is False                  # correct since this file doesn't exist
            assert _.file_fs__content ().exists() is True                   # correct this file exists
            assert _.file_fs__metadata().exists() is False                  # correct this file shouldn't exist

            assert _.obj() == __(file__config=__(exists_strategy='first',
                                                               file_id='test-single-file',
                                                               file_key='',
                                                               file_paths=[],
                                                               file_type=__(name='json_single',
                                                                            content_type='application/json; charset=utf-8',
                                                                            file_extension='json',
                                                                            encoding='utf-8',
                                                                            serialization='json')),
                                               storage_fs=__(content_data=__(test_single_file_json=b'{}')))

            data = b'{}'
            assert data.decode() == '{}'
            assert json.loads(data.decode()) == {}

    def test_create__none_data(self):                                           # Test creating with None
        with self.single_file_create as _:
            files_created = _.create(None)

            assert len(files_created) == 1
            assert files_created == ['test-single-file.json']

            # Verify null was stored
            content = self.storage_fs.file__json(Safe_Str__File__Path('test-single-file.json'))
            assert content                        is None
            assert _.file_fs__content ().exists() is True
            assert _.obj() == __(file__config=__(  exists_strategy='first',
                                                   file_id='test-single-file',
                                                   file_key='',
                                                   file_paths=[],
                                                   file_type=__(name='json_single',
                                                                content_type='application/json; charset=utf-8',
                                                                file_extension='json',
                                                                encoding='utf-8',
                                                                serialization='json')),
                                   storage_fs=__(content_data=__(test_single_file_json=b'null')))

            data = b'null'
            assert data.decode() == 'null'
            assert json.loads(data.decode()) is None

    def test_create__vs_regular_json(self):                                     # Compare with regular JSON file creation
        # Create regular JSON file
        regular_file_create = self.file.file_fs__create()
        regular_files = regular_file_create.create({"regular": "data"})

        # Create single JSON file
        single_files = self.single_file_create.create({"single": "data"})

        # Regular should create 3 files
        assert len(regular_files) == 3
        assert sorted(regular_files) == [
            f'{self.default_file_id}.json',
            f'{self.default_file_id}.json.config',
            f'{self.default_file_id}.json.metadata'
        ]

        # Single should create 1 file
        assert len(single_files) == 1
        assert single_files == ['test-single-file.json']
        assert self.storage_fs.obj()  == __(content_data = __(test_file_json_config     = b'{\n    \"exists_strategy\": \"first\"'
                                                                                        b',\n    \"file_id\": \"test-file\",\n  '
                                                                                        b'  \"file_key\": \"\",\n    \"file_path'
                                                                                        b's\": [],\n    \"file_type\": {\n     '
                                                                                        b'   \"name\": \"json\",\n        \"cont'
                                                                                        b'ent_type\": \"application/json; charse'
                                                                                        b't=utf-8\",\n        \"file_extensio'
                                                                                        b'n\": \"json\",\n        \"encoding\": '
                                                                                        b'\"utf-8\",\n        \"serialization\"'
                                                                                        b': \"json\"\n    }\n}'                                     ,

                                                              test_file_json          = b'{\n  \"regular\": \"data\"\n}'                          ,
                                                              test_file_json_metadata = __SKIP__                        ,       # because of the timestamp this value is not deterministic
                                                              test_single_file_json   = b'{\n  \"single\": \"data\"\n}'))


    def test_isinstance_check(self):                                            # Test that isinstance check works correctly
        # Test with single file type
        assert isinstance(self.single_file_type, Memory_FS__File__Type__Json__Single) is True
        assert isinstance(self.single_file_type, Memory_FS__File__Type__Json        ) is True  # Also inherits from Json

        # Test with regular JSON type
        regular_json_type = Memory_FS__File__Type__Json()
        assert isinstance(regular_json_type, Memory_FS__File__Type__Json__Single) is False
        assert isinstance(regular_json_type, Memory_FS__File__Type__Json        ) is True

    def test_create__binary_content(self):                                      # Test with binary data (should serialize to JSON)
        test_data = {"binary": "data", "bytes": 123}

        with self.single_file_create as _:
            files_created = _.create(test_data)
            assert files_created == ['test-single-file.json']

            stored_bytes = self.storage_fs.file__bytes(Safe_Str__File__Path('test-single-file.json'))       # Verify serialization worked

            serializer     = _.file_fs__serializer()                                                        # use the actual serialiser
            expected_bytes = serializer.serialize(test_data, self.single_file_type)                         # to get the expected bytes

            assert stored_bytes == b'{\n  "binary": "data",\n  "bytes": 123\n}'
            assert stored_bytes == expected_bytes                                       # different


    def test_create__already_exists(self):                                      # Test behavior when file already exists
        test_data_1 = {"first": "version"}
        test_data_2 = {"second": "version"}

        with self.single_file_create as _:
            # Create first time
            files_1 = _.create(test_data_1)
            assert len(files_1) == 1

            # Create again (should overwrite)
            files_2 = _.create(test_data_2)
            assert len(files_2) == 1

            # Verify content was updated
            content = self.storage_fs.file__json(Safe_Str__File__Path('test-single-file.json'))
            assert content == test_data_2
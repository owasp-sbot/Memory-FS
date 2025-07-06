from tests.unit.Base_Test__File_FS                      import Base_Test__File_FS
from osbot_utils.utils.Json                             import json_to_bytes, json_to_str
from memory_fs.file_fs.actions.File_FS__Create          import File_FS__Create

class test_File_FS__Create(Base_Test__File_FS):  # Test file creation operations

    def setUp(self):                                                        # Initialize test data
        super().setUp()
        self.file_create = self.file.file_fs__create()

    def test__init__(self):                                                 # Test initialization
        with self.file_create as _:
            assert type(_) is File_FS__Create
            assert _.file__config   == self.file_config
            assert _.storage_fs     == self.storage_fs

    def test_create__config(self):                                          # Test config file creation
        content__json   = self.file_config.json()
        content__str    = json_to_str  (content__json)
        content__bytes  = json_to_bytes(content__json)

        with self.file_create as _:
            assert _.file_fs__config().exists() is False
            files_created = _.create__config()
            assert files_created == [f"{self.file.file_id()}.json.config"]

            for file_created in files_created:
                assert self.storage_fs.file__exists (file_created) is True
                assert self.storage_fs.file__bytes  (file_created) == content__bytes
                assert self.storage_fs.file__str    (file_created) == content__str
                assert self.storage_fs.file__json   (file_created) == content__json

            assert _.file_fs__config().exists() is True

    def test_create__config_already_exists(self):                           # Test creating config when it already exists
        with self.file_create as _:
            files_created_1 = _.create__config()
            files_created_2 = _.create__config()

            assert len(files_created_1) == 1
            assert len(files_created_2) == 0                                # Should not create again

    def test_create__content(self):                                         # Test content file creation
        content = b'this is some content'

        with self.file_create as _:
            files_created = _.create__content(content)
            assert files_created == [f'{self.file_config.file_id}.json']

            for file_created in files_created:
                assert self.storage_fs.file__exists(file_created) is True
                assert self.storage_fs.file__bytes(file_created) == content
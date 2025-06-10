from unittest                                          import TestCase

from memory_fs.file.File_FS                            import File_FS
from osbot_utils.utils.Json                            import json_to_bytes, json_to_str
from memory_fs.storage_fs.providers.Storage_FS__Memory import Storage_FS__Memory
from memory_fs.file.actions.Memory_FS__File__Create    import Memory_FS__File__Create

class test_Memory_FS__File__Create(TestCase):

    @classmethod
    def setUpClass(cls):
        cls.storage_fs              = Storage_FS__Memory()
        cls.file                    = File_FS()
        cls.file.storage.storage_fs = cls.storage_fs            # todo: find a better way to use the Storage_FS__Memory as default in these tests
        cls.file_config             = cls.file.file_config
        cls.file_id                 = cls.file_config.file_id
        cls.file__edit              = cls.file.file__edit()
        cls.file__data              = cls.file.file__data()
        cls.file__create            = cls.file.file__create()

    def test_load__content(self):
        with self.file__edit as _:
            content = b'this is some content'
            result  = _.save__content(content)
            assert result == [f'{self.file_id}']
            assert _.load__content() == content

    def test_create(self):
        content__json  = self.file_config.json()
        content__str   = json_to_str  (content__json)
        content__bytes = json_to_bytes(content__json)

        with self.file__create as _:
            assert type(_) is Memory_FS__File__Create
            files_created = _.create__config()
            assert files_created == [f"{self.file.file_id()}.config"]

            for file_created in files_created:
                assert _.storage.storage_fs.file__exists(file_created) is True              # todo: refactor once "storage"  class is replaced with just storage_fs
                assert _.storage.storage_fs.file__bytes (file_created) == content__bytes
                assert _.storage.storage_fs.file__str   (file_created) == content__str
                assert _.storage.storage_fs.file__json  (file_created) == content__json

        assert content__json == { 'exists_strategy': 'FIRST'                    ,
                                  'file_id'        : self.file_id               ,
                                  'file_paths'     : []                         ,
                                  'file_type'      : { 'content_type'  : None  ,
                                                       'encoding'      : None  ,
                                                       'file_extension': None  ,
                                                       'name'          : None  ,
                                                       'serialization' : None  }}


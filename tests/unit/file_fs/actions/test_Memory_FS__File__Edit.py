from unittest                                           import TestCase
from memory_fs.file_fs.File_FS                          import File_FS
from memory_fs.file_fs.actions.File_FS__Edit            import File_FS__Edit
from memory_fs.storage_fs.providers.Storage_FS__Memory  import Storage_FS__Memory


class test_Memory_FS__File__Edit(TestCase):

    @classmethod
    def setUpClass(cls):
        cls.storage_fs              = Storage_FS__Memory()
        cls.file                    = File_FS(storage_fs=cls.storage_fs)
        cls.file_config             = cls.file.file_config
        cls.file_id                 = cls.file_config.file_id
        cls.file_edit               = cls.file.file_fs__edit()

    def test__init__(self):
        with self.file_edit as _:
            assert type(_               ) is File_FS__Edit

    def test_save__content(self):
        with self.file_edit as _:
            content = b'this is some content'
            result  = _.save__content(content)
            assert result == [f'{self.file_id}']
            assert _.load__content() == content


    def test__bug__save__is_not_handling_null_extensions(self):
        with self.file_edit as _:
            assert _.save__content(b'') == [f'{self.file_id}']

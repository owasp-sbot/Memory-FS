from unittest                                          import TestCase
from memory_fs.file_fs.actions.File_FS__Name              import FILE_EXTENSION__MEMORY_FS__FILE__CONFIG
from memory_fs.storage_fs.providers.Storage_FS__Memory import Storage_FS__Memory
from osbot_utils.helpers.safe_str.Safe_Str__File__Path import Safe_Str__File__Path
from memory_fs.file_fs.File_FS                            import File_FS

class test_Memory_FS__File__Data(TestCase):

    @classmethod
    def setUpClass(cls):
        cls.storage_fs              = Storage_FS__Memory()
        cls.file                    = File_FS()
        cls.file.storage.storage_fs = cls.file.storage.storage_fs = cls.storage_fs          # todo: find a way to do this assigment better
        cls.file_config             = cls.file.file_config
        cls.file_id                 = cls.file_config.file_id
        cls.file_edit               = cls.file.file_fs__edit()
        cls.file_data               = cls.file.file_fs__data()

    def test_load__content(self):
        with self.file_edit as _:
            content = b'this is some content'
            result  = _.save__content(content)
            assert result == [f'{self.file_id}']
            assert _.load__content() == content

    def test_load__paths(self):
        with self.file_data as _:
            paths = _.paths()
            assert paths == [Safe_Str__File__Path(f'{self.file_config.file_id}.{FILE_EXTENSION__MEMORY_FS__FILE__CONFIG}')]  # BUG: this should be
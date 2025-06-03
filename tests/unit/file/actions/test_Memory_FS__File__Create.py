from unittest                                       import TestCase
from memory_fs.file.Memory_FS__File                 import Memory_FS__File
from memory_fs.file.actions.Memory_FS__File__Create import Memory_FS__File__Create


from osbot_utils.utils.Dev import pprint


class test_Memory_FS__File__Create(TestCase):

    @classmethod
    def setUpClass(cls):
        cls.file        = Memory_FS__File()
        cls.file_config = cls.file.file_config
        cls.file_id   = cls.file_config.file_id
        cls.file_edit   = cls.file.edit()
        cls.file_data   = cls.file.data()
        cls.file_create = cls.file.create()

    def test_load__content(self):
        with self.file_edit as _:
            content = b'this is some content'
            result  = _.save__content(content)
            assert result == [f'{self.file_id}.None']
            assert _.load__content() == content

    def test_create(self):
        with self.file_create as _:
            assert type(_) is Memory_FS__File__Create
            # todo: finish this method implementation
            pprint(_.create())

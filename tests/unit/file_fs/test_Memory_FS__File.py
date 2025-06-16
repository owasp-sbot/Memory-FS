from unittest                                           import TestCase
from memory_fs.schemas.Schema__Memory_FS__File__Config  import Schema__Memory_FS__File__Config
from memory_fs.storage_fs.providers.Storage_FS__Memory  import Storage_FS__Memory
from osbot_utils.utils.Objects                          import __
from memory_fs.file_fs.File_FS                             import File_FS

class test_Memory_FS__File(TestCase):

    @classmethod
    def setUpClass(cls):
        cls.storage_fs              = Storage_FS__Memory()
        cls.file                    = File_FS()
        cls.file.storage.storage_fs = cls.storage_fs                                            # todo: find a better way to do this assigment

    def test__init__(self):
        with self.file as _:
            assert type(_) is File_FS
            assert type(_.config()) is Schema__Memory_FS__File__Config
            assert _.obj()           == __(file_config =__(exists_strategy ='FIRST'                ,
                                                           file_id         = _.file_config.file_id,
                                                           file_paths      = [],
                                                           file_type       = __(name          = None,
                                                                               content_type   = None,
                                                                               file_extension = None,
                                                                               encoding       = None,
                                                                               serialization  = None)),

                                           storage     =  __(storage_type = 'memory'                         ,
                                                             file_system  = __(files=__(), content_data=__()),
                                                             storage_fs   =  __(content_data=__())                            ))

    def test_create(self):
        with self.file as _:
            assert _.exists() is False                                         # file should not exist before it is created
            assert _.create()  == [f"{self.file.file_id()}.config"]             # create file returns the files created
            assert _.exists() is True                                          # file should now exist


    def test_exists(self):
        with self.file as _:
            assert _.exists() is True

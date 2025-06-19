from unittest                                               import TestCase
from memory_fs.storage_fs.providers.Storage_FS__Sqlite      import Storage_FS__Sqlite
from memory_fs.storage_fs.Storage_FS                        import Storage_FS


class test_Storage_FS__Sqlite(TestCase):                                                # Test SQLite storage provider

    def test__init__(self):                                                             # Test initialization
        with Storage_FS__Sqlite() as _:
            assert type(_)                      is Storage_FS__Sqlite
            assert issubclass(type(_), Storage_FS) is True

    def test__not_implemented(self):                                                    # Test that it's not implemented
        # This is a placeholder class that needs implementation
        # All methods should behave like the base Storage_FS class
        with Storage_FS__Sqlite() as _:
            assert _.file__bytes("test.txt")             is None
            assert _.file__delete("test.txt")            is False
            assert _.file__exists("test.txt")            is False
            assert _.file__save("test.txt", b"content")  is False
from typing                                                 import Any
from memory_fs.file_fs.actions.File_FS__Exists              import File_FS__Exists
from memory_fs.file_fs.actions.File_FS__Paths               import File_FS__Paths
from memory_fs.file_fs.data.File_FS__Config                 import File_FS__Config
from memory_fs.file_fs.data.File_FS__Content                import File_FS__Content
from memory_fs.file_fs.data.File_FS__Metadata               import File_FS__Metadata
from memory_fs.schemas.Schema__Memory_FS__File__Metadata    import Schema__Memory_FS__File__Metadata
from memory_fs.storage_fs.Storage_FS                        import Storage_FS
from osbot_utils.decorators.methods.cache_on_self           import cache_on_self
from memory_fs.schemas.Schema__Memory_FS__File__Config      import Schema__Memory_FS__File__Config
from osbot_utils.type_safe.Type_Safe                        import Type_Safe

class File_FS__Data(Type_Safe):
    file__config : Schema__Memory_FS__File__Config
    storage_fs  : Storage_FS

    @cache_on_self
    def file_fs__exists(self):
        return File_FS__Exists(file__config=self.file__config, storage_fs=self.storage_fs)

    @cache_on_self
    def file_fs__paths(self):
        return File_FS__Paths(file__config=self.file__config)

    @cache_on_self
    def file_fs__content(self):
        return File_FS__Content(file__config=self.file__config, storage_fs= self.storage_fs)

    @cache_on_self
    def file_fs__metadata(self):
        return File_FS__Metadata(file__config=self.file__config, storage_fs=self.storage_fs)

    @cache_on_self
    def file_fs__config(self) -> File_FS__Config:
        return File_FS__Config(file__config=self.file__config, storage_fs=self.storage_fs)                    # todo: wrap the file__config and storage in another class since there are tons of methods that always need these two objects


    def config(self) -> Schema__Memory_FS__File__Config:
        return self.file_fs__config().config()

    def content(self) -> bytes:                                                                         # todo: see if bytes is a better name for this method
        return self.file_fs__content().bytes()

    def data(self) -> Any:
        return self.file_fs__content().data()

    def exists(self):
        return self.file_fs__exists().config()                                                          # if the .config() exists, then the file 'exists'

    def metadata(self) -> Schema__Memory_FS__File__Metadata:
        return self.file_fs__metadata().load()

    def not_exists(self):
        return self.exists() is False

    def paths(self):
        return self.file_fs__paths().paths()


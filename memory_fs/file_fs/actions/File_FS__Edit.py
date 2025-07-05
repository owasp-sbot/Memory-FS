from typing import Any

from memory_fs.file_fs.actions.File_FS__Paths           import File_FS__Paths
from memory_fs.file_fs.actions.File_FS__Update import File_FS__Update
from memory_fs.file_fs.data.File_FS__Content import File_FS__Content
from memory_fs.storage_fs.Storage_FS                    import Storage_FS
from osbot_utils.decorators.methods.cache_on_self       import cache_on_self
from memory_fs.schemas.Schema__Memory_FS__File__Config  import Schema__Memory_FS__File__Config
from osbot_utils.type_safe.Type_Safe                    import Type_Safe

class File_FS__Edit(Type_Safe):
    file__config : Schema__Memory_FS__File__Config
    storage_fs  : Storage_FS

    ###### File_FS__* methods #######

    @cache_on_self
    def file_fs__content(self):
        return File_FS__Content(file__config=self.file__config, storage_fs=self.storage_fs)

    @cache_on_self
    def file_fs__paths(self):
        return File_FS__Paths(file__config=self.file__config)

    @cache_on_self
    def file_fs__update(self):
        return File_FS__Update(file__config=self.file__config, storage_fs=self.storage_fs)

    ###### File_FS__Edit methods #######

    def load__content(self) -> Any:
        return self.file_fs__content().load()

    def save__content(self, file_data: Any):
        return self.file_fs__update().update(file_data=file_data)


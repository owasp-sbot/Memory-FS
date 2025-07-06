from memory_fs.file_fs.data.File_FS__File import File_FS__File
from osbot_utils.utils.Json                             import json_to_bytes
from memory_fs.file_fs.actions.File_FS__Exists          import File_FS__Exists
from memory_fs.file_fs.actions.File_FS__Paths           import File_FS__Paths
from memory_fs.storage_fs.Storage_FS                    import Storage_FS
from osbot_utils.decorators.methods.cache_on_self       import cache_on_self
from memory_fs.file_fs.actions.File_FS__Name            import File_FS__Name
from memory_fs.schemas.Schema__Memory_FS__File__Config  import Schema__Memory_FS__File__Config
from osbot_utils.type_safe.Type_Safe                    import Type_Safe


# note: config file can only be created or deleted (it cannot be edited)

class File_FS__Config(File_FS__File):               # todo: refactor the methods from this class that are the same for the .content() and .metadata() files, what about an base class called File_FS__File (which contains most of the shared code)

    def create(self):
        if self.exists() is False:
            return self.update(data=self.data())
        return []

    def config(self) -> Schema__Memory_FS__File__Config:
        return self.file__config

    def data(self):
        content__data  = self.file__config.json()
        content__bytes = json_to_bytes(content__data)
        return content__bytes

    def paths(self):
        return self.file_fs__paths().paths__config()
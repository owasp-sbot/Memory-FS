from osbot_utils.utils.Json import json_to_bytes

from memory_fs.file_fs.actions.File_FS__Exists          import File_FS__Exists
from memory_fs.file_fs.actions.File_FS__Paths import File_FS__Paths
from memory_fs.storage_fs.Storage_FS                    import Storage_FS
from osbot_utils.decorators.methods.cache_on_self       import cache_on_self
from memory_fs.file_fs.actions.File_FS__Name            import File_FS__Name
from memory_fs.schemas.Schema__Memory_FS__File__Config  import Schema__Memory_FS__File__Config
from osbot_utils.type_safe.Type_Safe                    import Type_Safe

class File_FS__Config(Type_Safe):               # todo: refactor the methods from this class that are the same for the .content() and .metadata() files
    file__config : Schema__Memory_FS__File__Config
    storage_fs  : Storage_FS

    ###### File_FS__* methods #######

    @cache_on_self
    def file_fs__exists(self):
        return File_FS__Exists(file__config=self.file__config, storage_fs=self.storage_fs)

    @cache_on_self
    def file_fs__name(self):
        return File_FS__Name(file__config=self.file__config)

    @cache_on_self
    def file_fs__paths(self):
        return File_FS__Paths(file__config=self.file__config)

    ###### Main methods #######

    def config(self) -> Schema__Memory_FS__File__Config:
        return self.file__config

    def create(self):
        if self.exists() is False:
            files_to_save = self.file_fs__paths().paths__config()
            files_saved   = []
            for file_to_save in files_to_save:
                content__data  = self.file__config.json()
                content__bytes = json_to_bytes(content__data)                                           # todo: refactor this logic of saving the json into bytes into a separate method or class (since it shouldn't be here)
                if self.storage_fs.file__save(file_to_save, content__bytes):
                    files_saved.append(file_to_save)
            return files_saved
        return []
    def file_id(self):
        return self.file__config.file_id

    def file_name(self):                                                                                # todo: see if we need these methods in this class
        return self.file_fs__name().config()

    def exists(self) -> bool:
        return self.file_fs__exists().config()

    def not_exists(self) -> bool:
        return self.exists() is False

from memory_fs.file.actions.Memory_FS__File__Data       import Memory_FS__File__Data
from memory_fs.file.actions.Memory_FS__File__Edit       import Memory_FS__File__Edit
from memory_fs.schemas.Schema__Memory_FS__File__Config  import Schema__Memory_FS__File__Config
from memory_fs.storage.Memory_FS__Storage import Memory_FS__Storage
from osbot_utils.decorators.methods.cache_on_self       import cache_on_self
from memory_fs.schemas.Schema__Memory_FS__File          import Schema__Memory_FS__File
from osbot_utils.type_safe.Type_Safe                    import Type_Safe


class Memory_FS__File(Type_Safe):
    file   : Schema__Memory_FS__File
    storage: Memory_FS__Storage

    @cache_on_self
    def data(self):
        return Memory_FS__File__Data(file=self.file)

    @cache_on_self
    def edit(self):
        return Memory_FS__File__Edit(file=self.file)

    def config(self) -> Schema__Memory_FS__File__Config:
        return self.file.config
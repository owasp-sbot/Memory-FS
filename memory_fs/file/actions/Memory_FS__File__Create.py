from memory_fs.actions.Memory_FS__Edit import Memory_FS__Edit
from memory_fs.file.actions.Memory_FS__File__Data       import Memory_FS__File__Data
from memory_fs.file.actions.Memory_FS__File__Edit import Memory_FS__File__Edit
from osbot_utils.decorators.methods.cache_on_self       import cache_on_self
from memory_fs.schemas.Schema__Memory_FS__File__Config  import Schema__Memory_FS__File__Config
from memory_fs.storage.Memory_FS__Storage               import Memory_FS__Storage
from osbot_utils.type_safe.Type_Safe                    import Type_Safe

# todo: move the note below to https://github.com/owasp-sbot/Memory-FS/blob/dev/docs/memory_fs/file/actions/Memory_FS__File__Create.md
#       this is where we are going to be storing details about each class

# note: config file can only be created or deleted (it cannot be edited)

class Memory_FS__File__Create(Type_Safe):
    file__config : Schema__Memory_FS__File__Config
    storage      : Memory_FS__Storage

    @cache_on_self
    def file__edit(self):
        return Memory_FS__File__Edit(file__config=self.file__config, storage=self.storage)

    @cache_on_self
    def file__data(self):
        return Memory_FS__File__Data(file__config=self.file__config, storage=self.storage)

    def create(self):
        with self.file__data() as _:
            if _.exists() is False:
                return self.file__edit().create__config()
            return False

    def exists(self):
        return self.file__data().exists()
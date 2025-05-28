from memory_fs.actions.Memory_FS__Delete            import Memory_FS__Delete
from memory_fs.actions.Memory_FS__Exists            import Memory_FS__Exists
from memory_fs.actions.Memory_FS__File__New         import Memory_FS__File__New
from memory_fs.actions.Memory_FS__Load              import Memory_FS__Load
from memory_fs.actions.Memory_FS__Save              import Memory_FS__Save
from memory_fs.file.Memory_FS__File__Storage        import Memory_FS__File__Storage
from osbot_utils.decorators.methods.cache_on_self   import cache_on_self
from memory_fs.actions.Memory_FS__Data              import Memory_FS__Data
from memory_fs.actions.Memory_FS__Edit              import Memory_FS__Edit
from memory_fs.core.Memory_FS__File_System          import Memory_FS__File_System
from osbot_utils.type_safe.Type_Safe                import Type_Safe


class Memory_FS(Type_Safe):
    file_system : Memory_FS__File_System

    @cache_on_self
    def data(self):
        return Memory_FS__Data(file_system=self.file_system)

    @cache_on_self
    def delete(self):
        return Memory_FS__Delete(file_system=self.file_system)

    @cache_on_self
    def edit(self):
        return Memory_FS__Edit(file_system=self.file_system)

    @cache_on_self
    def exists(self):
        return Memory_FS__Exists(file_system=self.file_system)

    @cache_on_self
    def load(self):
        return Memory_FS__Load(file_system=self.file_system)

    @cache_on_self
    def new(self, file_storage: Memory_FS__File__Storage = None):
        return Memory_FS__File__New(file_system=self.file_system, file_storage=file_storage)

    @cache_on_self
    def save(self):
        return Memory_FS__Save(file_system=self.file_system)

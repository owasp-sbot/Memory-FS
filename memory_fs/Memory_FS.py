from osbot_utils.decorators.methods.cache_on_self import cache_on_self

from memory_fs.actions.Memory_FS__Data     import Memory_FS__Data
from memory_fs.actions.Memory_FS__Edit     import Memory_FS__Edit
from memory_fs.core.Memory_FS__File_System import Memory_FS__File_System
from osbot_utils.type_safe.Type_Safe       import Type_Safe


class Memory_FS(Type_Safe):
    file_system : Memory_FS__File_System

    @cache_on_self
    def data(self):
        return Memory_FS__Data(file_system=self.file_system)

    @cache_on_self
    def edit(self):
        return Memory_FS__Edit(file_system=self.file_system)

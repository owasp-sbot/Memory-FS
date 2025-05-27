from memory_fs.actions.Memory_FS__Data import Memory_FS__Data
from osbot_utils.type_safe.Type_Safe   import Type_Safe


class Memory_FS(Type_Safe):
    def data(self):
        return Memory_FS__Data()

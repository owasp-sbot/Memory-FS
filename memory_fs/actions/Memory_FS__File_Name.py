from memory_fs.schemas.Schema__Memory_FS__File__Config import Schema__Memory_FS__File__Config
from osbot_utils.type_safe.Type_Safe import Type_Safe

class Memory_FS__File_Name(Type_Safe):
    file_config: Schema__Memory_FS__File__Config

    def config(self):
        return 'abc'

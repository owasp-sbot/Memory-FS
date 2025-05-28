from typing                                             import List, Type
from memory_fs.schemas.Schema__Memory_FS__Path__Handler import Schema__Memory_FS__Path__Handler
from osbot_utils.type_safe.Type_Safe                    import Type_Safe

class Schema__Memory_FS__File__Storage__Config(Type_Safe):
    path_handlers : List[Type[Schema__Memory_FS__Path__Handler]]

class Memory_FS__File__Storage(Type_Safe):
    config: Schema__Memory_FS__File__Storage__Config

    def file__paths(self):
        return len(self.config.path_handlers)
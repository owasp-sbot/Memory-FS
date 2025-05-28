from typing                                 import Type, List

from memory_fs.storage.Memory_FS__Storage import Memory_FS__Storage
from osbot_utils.helpers.Safe_Id            import Safe_Id
from memory_fs.Memory_FS                    import Memory_FS
from memory_fs.path_handlers.Path__Handler  import Path__Handler
from osbot_utils.type_safe.Type_Safe        import Type_Safe

class Schema__Memory_FS__Project__Config(Type_Safe):
    storage      : Type[Memory_FS__Storage]
    path_handlers: List[Type[Path__Handler]]
    name         : Safe_Id                   = None
from typing                                             import List, Set
from osbot_utils.helpers.safe_str.Safe_Str__File__Path  import Safe_Str__File__Path
from memory_fs.schemas.Schema__Memory_FS__File__Type    import Schema__Memory_FS__File__Type
from osbot_utils.helpers.Safe_Id                        import Safe_Id
from osbot_utils.type_safe.Type_Safe                    import Type_Safe
from memory_fs.schemas.Schema__Memory_FS__Path__Handler import Schema__Memory_FS__Path__Handler

class Schema__Memory_FS__File__Config(Type_Safe):
    content_path    : Safe_Str__File__Path                   = None         # todo: to remove
    path_handlers   : List[Schema__Memory_FS__Path__Handler]                # todo: to remove
    default_handler : Schema__Memory_FS__Path__Handler       = None         # todo: to remove
    file_type       : Schema__Memory_FS__File__Type
    file_name       : Safe_Id                                = None          # e.g., "article"
    file_paths      : List[Safe_Str__File__Path]
    tags            : Set[Safe_Id]

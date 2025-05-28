from typing                                             import List, Set
from osbot_utils.helpers.Random_Guid                    import Random_Guid
from osbot_utils.helpers.safe_str.Safe_Str__File__Path  import Safe_Str__File__Path
from memory_fs.schemas.Schema__Memory_FS__File__Type    import Schema__Memory_FS__File__Type
from osbot_utils.helpers.Safe_Id                        import Safe_Id
from osbot_utils.type_safe.Type_Safe                    import Type_Safe

class Schema__Memory_FS__File__Config(Type_Safe):
    file_id         : Random_Guid
    file_name       : Safe_Id                               = None      # todo see side effects of settings this to a random value
    file_paths      : List[Safe_Str__File__Path]
    file_type       : Schema__Memory_FS__File__Type

from typing                                             import Optional, Set
from osbot_utils.helpers.Safe_Id                        import Safe_Id
from osbot_utils.helpers.Timestamp_Now                  import Timestamp_Now
from osbot_utils.helpers.safe_int.Safe_UInt__FileSize   import Safe_UInt__FileSize
from osbot_utils.helpers.safe_str.Safe_Str__File__Path  import Safe_Str__File__Path
from osbot_utils.helpers.safe_str.Safe_Str__Hash        import Safe_Str__Hash
from osbot_utils.type_safe.Type_Safe                    import Type_Safe


class Schema__Memory_FS__File__Metadata(Type_Safe):
    content__hash        : Safe_Str__Hash                        = None
    content__size        : Safe_UInt__FileSize
    chain_hash           : Optional[Safe_Str__Hash]              = None
    previous_version_path: Optional[Safe_Str__File__Path]        = None         # todo: refactor this logic into a better naming convention and class structure
    tags                 : Set[Safe_Id]                                         # todo: should we move this into an 'user_data' section (since this is the only part of this data object that us editable by the user
    timestamp            : Timestamp_Now

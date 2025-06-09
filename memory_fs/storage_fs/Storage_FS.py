from osbot_utils.helpers.safe_str.Safe_Str__File__Path  import Safe_Str__File__Path
from osbot_utils.type_safe.Type_Safe                    import Type_Safe


class Storage_FS(Type_Safe):

    def file__bytes (self, path: Safe_Str__File__Path             ) -> bytes: raise NotImplementedError
    def file__exists(self, path: Safe_Str__File__Path             ) -> bool : raise NotImplementedError
    def file__json  (self, path: Safe_Str__File__Path             ) -> bytes: raise NotImplementedError
    def file__save  (self, path: Safe_Str__File__Path, data: bytes) -> bool : raise NotImplementedError
    def file__str   (self, path: Safe_Str__File__Path             ) -> str  : raise NotImplementedError
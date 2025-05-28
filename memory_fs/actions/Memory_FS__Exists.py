from osbot_utils.helpers.safe_str.Safe_Str__File__Path import Safe_Str__File__Path

from memory_fs.actions.Memory_FS__Data                  import Memory_FS__Data
from memory_fs.actions.Memory_FS__Paths                 import Memory_FS__Paths
from memory_fs.storage.Memory_FS__Storage               import Memory_FS__Storage
from osbot_utils.decorators.methods.cache_on_self       import cache_on_self
from memory_fs.schemas.Schema__Memory_FS__File__Config  import Schema__Memory_FS__File__Config
from osbot_utils.type_safe.Type_Safe                    import Type_Safe

class Memory_FS__Exists(Type_Safe):
    storage     : Memory_FS__Storage

    @cache_on_self
    def memory_fs__data(self):
        return Memory_FS__Data(storage=self.storage)

    def memory_fs__paths(self):
        return Memory_FS__Paths()

    def exists(self, file_config : Schema__Memory_FS__File__Config  # todo: see if we need to add the default path (or to have a separate "exists strategy")
                ) -> bool:
        if not file_config.file_paths:                                                  # if there is at last one file_path
            return False
        for file_path in file_config.file_paths:                                # and we found all of them
            full_file_path = Safe_Str__File__Path(f"{file_path}/{file_config.file_name}.{file_config.file_type.file_extension}.fs.json")
            if not self.memory_fs__data().exists(full_file_path):               #   todo: review the impact of checking this for all exists (since this will check for all files in the mapped file_paths (which in some cases is exactly what we want))
                return False
        return True


from typing                                                 import List, Dict, Any
from memory_fs.file_fs.actions.File_FS__Name                import FILE_EXTENSION__MEMORY_FS__FILE__CONFIG
from osbot_utils.utils.Json                                 import bytes_to_json
from memory_fs.file_fs.File_FS                              import File_FS
from memory_fs.schemas.Schema__Memory_FS__File__Config      import Schema__Memory_FS__File__Config
from memory_fs.storage.Memory_FS__Storage                   import Memory_FS__Storage
from osbot_utils.helpers.Safe_Id                            import Safe_Id
from osbot_utils.helpers.safe_str.Safe_Str__File__Path      import Safe_Str__File__Path
from osbot_utils.type_safe.Type_Safe                        import Type_Safe

# todo: I think most of these Memory_FS__* classes should be refactored to the Storage_FS__* classes
class Memory_FS__Data(Type_Safe):
    storage     : Memory_FS__Storage


    def list_files(self, prefix : Safe_Str__File__Path = None                                  # List all files, optionally filtered by prefix
                    ) -> List[Safe_Str__File__Path]:                                           # todo: see if we need this method
        if prefix is None:
            return list(self.storage.storage_fs.files__paths())

        prefix_str = str(prefix)
        if not prefix_str.endswith('/'):
            prefix_str += '/'

        return [path for path in self.storage.files__paths()
                if str(path).startswith(prefix_str)]

    def load(self, path: Safe_Str__File__Path) -> File_FS: # todo: see if we should have this method, or if we do need this more generic load() method (maybe to allow the discovery of the file from one of the paths: config, content or metadata)
        return self.load__from_path__config(path)          #for now assume the path is Safe_Str__File__Path

    def load__from_path__config(self, path : Safe_Str__File__Path) -> File_FS:                 # Load a File_Fs object from a config path
        with self.storage.storage_fs as _:
            if _.file__exists(path):                                                # todo add a check if path is indeed a .config file
                file_bytes = _.file__bytes(path)
                file_json  = bytes_to_json(file_bytes)
                file_config = Schema__Memory_FS__File__Config.from_json(file_json)  # todo: add error handling and the cases when file_json is not Schema__Memory_FS__File__Config
                file_fs     = File_FS(file_config=file_config, storage=self.storage)
                return file_fs


    # def load_content(self, path : Safe_Str__File__Path                                         # Load raw content from the given path
    #                   ) -> Optional[bytes]:
    #     return self.storage.file__content(path)


    # todo: see if we need this method (this was originally developed during one of the first architectures, but we will probably be better with an Storage_FS__Stats class (which can then take into account limitations of the current storage)
    # todo: this should return a python object (and most likely moved into a Memory_FS__Stats class)
    def stats(self) -> Dict[Safe_Id, Any]:                                                     # Get file system statistics
        total_size = 0
        for path in self.storage.files__paths():
            if path.endswith(FILE_EXTENSION__MEMORY_FS__FILE__CONFIG):                              # todo: we need a better way to only get the .config files (and calculate its size)
                fs_file = self.load(path)                                                           # todo: review the existance of this method, since this could have big performance implications
                content = fs_file.content()
                total_size += len(content)                                                          # todo: use the file size instead

        return {Safe_Id("type")            : Safe_Id("memory")               ,
                Safe_Id("file_count")      : len(self.storage.files__paths ()),
                Safe_Id("total_size")      : total_size                      }

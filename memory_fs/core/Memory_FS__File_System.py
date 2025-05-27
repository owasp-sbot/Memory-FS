from typing                                              import Dict, List, Optional, Any
from osbot_utils.helpers.Safe_Id                         import Safe_Id
from osbot_utils.helpers.safe_str.Safe_Str__File__Path   import Safe_Str__File__Path
from osbot_utils.type_safe.Type_Safe                     import Type_Safe
from memory_fs.schemas.Schema__Memory_FS__File           import Schema__Memory_FS__File


class Memory_FS__File_System(Type_Safe):                                                # In-memory file system that maintains directory structure and file storage
    files          : Dict[Safe_Str__File__Path, Schema__Memory_FS__File]                                  # Path -> File metadata mapping
    content_data   : Dict[Safe_Str__File__Path, bytes]                                           # Path -> Raw content mapping

    def load(self, path : Safe_Str__File__Path                                                 # Load a file metadata from the given path
              ) -> Optional[Schema__Memory_FS__File]:
        return self.files.get(path)

    def load_content(self, path : Safe_Str__File__Path                                         # Load raw content from the given path
                      ) -> Optional[bytes]:
        return self.content_data.get(path)





    def clear(self) -> None:                                                                    # Clear all files and directories
        self.files.clear()
        self.content_data.clear()

    def stats(self) -> Dict[Safe_Id, Any]:                                                     # Get file system statistics
        total_size = 0
        for path, content in self.content_data.items():
            total_size += len(content)

        return {Safe_Id("type")            : Safe_Id("memory")       ,
                Safe_Id("file_count")      : len(self.files)        ,
                Safe_Id("content_count")   : len(self.content_data) ,
                Safe_Id("total_size")      : total_size             }
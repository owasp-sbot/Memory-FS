from typing import Dict, List
from osbot_utils.utils.Json                             import bytes_to_json
from osbot_utils.type_safe.type_safe_core.decorators.type_safe         import type_safe
from osbot_utils.type_safe.primitives.domains.files.safe_str.Safe_Str__File__Path  import Safe_Str__File__Path
from memory_fs.storage_fs.Storage_FS                    import Storage_FS

# todo: see if this class shouldn't be leveraging the Serialisation and DeSerialisation classes/logic

class Storage_FS__Memory(Storage_FS):
    content_data: Dict[Safe_Str__File__Path, bytes]

    def clear(self):
        self.content_data.clear()
        return True

    @type_safe
    def file__bytes(self, path: Safe_Str__File__Path):
        return self.content_data.get(path)

    @type_safe
    def file__delete(self, path: Safe_Str__File__Path) -> bool:
        if path in self.content_data:
            del self.content_data[path]
            return True
        return False

    @type_safe
    def file__exists(self, path: Safe_Str__File__Path):
        return path in self.content_data

    @type_safe
    def file__json(self, path: Safe_Str__File__Path):
        file_bytes = self.file__bytes(path)
        if file_bytes:
            return bytes_to_json(file_bytes)

    @type_safe
    def file__save(self, path: Safe_Str__File__Path, data: bytes) -> bool:
        self.content_data[path] = data
        return True

    @type_safe
    def file__str(self, path: Safe_Str__File__Path):
        file_bytes = self.file__bytes(path)
        if file_bytes:
            return file_bytes.decode()                  # todo: add content type to this decode


    def files__paths(self):
        return self.content_data.keys()

    def folder__folders(self, parent_folder   : Safe_Str__File__Path,
                              return_full_path: bool = True
                         ) -> List[Safe_Str__File__Path]:
        subfolders   = set()
        prefix       = str(parent_folder)
        if not prefix.endswith('/'):
            prefix += '/'

        for path in self.content_data.keys():
            path_str = str(path)
            if path_str.startswith(prefix):
                remainder = path_str[len(prefix):]
                parts     = remainder.split('/')
                if len(parts) > 1:       # means there is at least one subfolder before the file
                    if return_full_path:
                        subfolder = prefix + parts[0]
                    else:
                        subfolder = parts[0]
                    subfolders.add(Safe_Str__File__Path(subfolder))
        return sorted(subfolders)

    # todo: add unit tests for this method
    def folder__files__all(self, parent_folder: Safe_Str__File__Path) -> List[Safe_Str__File__Path]:         # Get all files under a specific folder
        matching_files = []
        prefix         = str(parent_folder)
        if not prefix.endswith('/'):
            prefix += '/'

        for path in self.content_data.keys():
            if str(path).startswith(prefix):
                matching_files.append(path)

        return matching_files
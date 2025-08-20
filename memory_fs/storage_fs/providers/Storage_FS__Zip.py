from typing                                                                     import List, Optional
from osbot_utils.type_safe.primitives.safe_str.filesystem.Safe_Str__File__Path  import Safe_Str__File__Path
from osbot_utils.type_safe.type_safe_core.decorators.type_safe                  import type_safe
from osbot_utils.utils.Json                                                     import bytes_to_json
from osbot_utils.utils.Zip                                                      import (zip_bytes__add_file,
                                                                                        zip_bytes__file, zip_bytes__file_list,
                                                                                        zip_bytes__remove_file, zip_bytes__replace_file,
                                                                                        zip_bytes__files)
from memory_fs.storage_fs.Storage_FS                                            import Storage_FS


class Storage_FS__Zip(Storage_FS):
    zip_bytes: bytes                                                                    # In-memory zip content

    # def __init__(self, **kwargs):
    #     super().__init__(**kwargs)
    #     if self.zip_bytes is None:                                                      # Initialize with empty zip if not provided
    #         self.zip_bytes = zip_bytes_empty()

    @type_safe
    def file__bytes(self, path: Safe_Str__File__Path                                   # Read file content as bytes from zip
                    ) -> Optional[bytes]:
        if self.file__exists(path):
            file_bytes = zip_bytes__file(self.zip_bytes, str(path))
            if file_bytes is None:
                return b""
            return file_bytes
        return None

    @type_safe
    def file__delete(self, path: Safe_Str__File__Path                                  # Delete a file from zip
                      ) -> Optional[bytes]:
        if self.file__exists(path):
            self.zip_bytes =  zip_bytes__remove_file(self.zip_bytes, str(path))
            return True
        return False

    @type_safe
    def file__exists(self, path: Safe_Str__File__Path                                  # Check if file exists in zip
                     ) -> bool:
        if self.zip_bytes:
            files_in_zip = zip_bytes__file_list(self.zip_bytes)
            return str(path) in files_in_zip
        return False

    @type_safe
    def file__json(self, path: Safe_Str__File__Path                                    # Read file content as JSON from zip
                   ) -> Optional[dict]:
        file_bytes = self.file__bytes(path)
        if file_bytes:
            return bytes_to_json(file_bytes)
        return None

    @type_safe
    def file__save(self, path: Safe_Str__File__Path ,                                  # Save bytes to zip
                         data: bytes
                   ) -> bool:

        path_str = str(path)
        if self.file__exists(path):                                                # Use replace if file exists
            self.zip_bytes = zip_bytes__replace_file(self.zip_bytes, path_str, data)
        else:                                                                       # Use add for new files
            self.zip_bytes = zip_bytes__add_file(self.zip_bytes, path_str, data)
        return True                                                                 # this always works

    @type_safe
    def file__str(self, path: Safe_Str__File__Path                                     # Read file content as string from zip
                  ) -> Optional[str]:
        file_bytes = self.file__bytes(path)
        if file_bytes is not None:
            return file_bytes.decode('utf-8')
        return None

    def files__paths(self) -> List[Safe_Str__File__Path]:                              # List all file paths in zip
        if self.zip_bytes:
            files_list = zip_bytes__file_list(self.zip_bytes)
            return [Safe_Str__File__Path(file_path) for file_path in sorted(files_list)]
        return []

    def clear(self) -> bool:                                                           # Clear all files (reset to empty zip)
        self.zip_bytes = b""
        return True

    # Additional Zip-specific utility methods

    def get_all_files(self) -> dict:                                                   # Get all files and their contents
        try:
            return zip_bytes__files(self.zip_bytes)
        except Exception:
            return {}

    def size_bytes(self) -> int:                                                       # Get the size of the zip in bytes
        return len(self.zip_bytes)

    def file_count(self) -> int:                                                       # Get the number of files in the zip
        return len(self.files__paths())

    def export_bytes(self) -> bytes:                                                   # Export the entire zip as bytes
        return self.zip_bytes

    @type_safe
    def import_bytes(self, zip_bytes: bytes                                            # Import zip from bytes
                     ) -> bool:
        zip_bytes__file_list(zip_bytes)                                                # This will Validate it's a valid zip by trying to list files
        self.zip_bytes = zip_bytes
        return True
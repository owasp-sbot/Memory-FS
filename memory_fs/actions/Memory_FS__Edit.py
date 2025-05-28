from memory_fs.schemas.Schema__Memory_FS__File          import Schema__Memory_FS__File
from memory_fs.storage.Memory_FS__Storage               import Memory_FS__Storage
from osbot_utils.helpers.safe_str.Safe_Str__File__Path  import Safe_Str__File__Path
from osbot_utils.type_safe.Type_Safe                    import Type_Safe


class Memory_FS__Edit(Type_Safe):
    storage     : Memory_FS__Storage

    def clear(self) -> None:                                                                    # Clear all files and directories
        self.storage.files       ().clear()         # todo: refactor this logic to storage
        self.storage.content_data().clear()

    def copy(self, source      : Safe_Str__File__Path ,                                        # Copy a file from source to destination
                   destination : Safe_Str__File__Path
              ) -> bool:
        if source not in self.storage.files():
            return False

        file = self.storage.file(source)
        self.save(destination, file)

        # Also copy content if it exists
        if source in self.storage.content_data():                                               # todo: need to refactor the logic of the files and the support files
            self.save_content(destination, self.storage.file__content(source))

        return True

    def delete(self, path : Safe_Str__File__Path                                               # Delete a file at the given path
                ) -> bool:
        if path in self.storage.files():
            del self.storage.files()[path]                                                     # todo: this needs to be abstracted out in the storage class
            return True
        return False

    def delete_content(self, path : Safe_Str__File__Path                                       # Delete content at the given path
                        ) -> bool:
        if path in self.storage.content_data():
            del self.storage.content_data()[path]                                               # todo: this needs to be abstracted out in the storage class
            return True
        return False

    def move(self, source      : Safe_Str__File__Path ,                                        # Move a file from source to destination
                   destination : Safe_Str__File__Path
              ) -> bool:
        if source not in self.storage.files():
            return False

        file = self.storage.file(source)
        self.save(destination, file)
        self.delete(source)

        # Also move content if it exists
        if source in self.storage.content_data():
            self.save_content(destination, self.storage.file__content(source))
            self.delete_content(source)

        return True

    def save(self, path : Safe_Str__File__Path ,                                               # Save a file metadata at the given path
                   file : Schema__Memory_FS__File
              ) -> bool:
        self.storage.files()[path] = file                                                      # Store the file metadata
        return True

    # todo:need to save the length in the metadata
    def save_content(self, path    : Safe_Str__File__Path ,                                    # Save raw content at the given path
                           content : bytes
                      ) -> bool:
        self.storage.content_data()[path] = content                                         # todo: this needs to be abstracted out in the storage class              # Store the raw content
        return True

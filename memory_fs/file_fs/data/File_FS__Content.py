from typing                                             import Any, List
from osbot_utils.helpers.safe_str.Safe_Str__File__Path  import Safe_Str__File__Path
from memory_fs.file_fs.actions.File_FS__Serializer      import File_FS__Serializer
from memory_fs.file_fs.actions.File_FS__Exists          import File_FS__Exists
from memory_fs.storage_fs.Storage_FS                    import Storage_FS
from osbot_utils.type_safe.Type_Safe                    import Type_Safe
from osbot_utils.decorators.methods.cache_on_self       import cache_on_self
from memory_fs.file_fs.actions.File_FS__Paths           import File_FS__Paths
from memory_fs.schemas.Schema__Memory_FS__File__Config  import Schema__Memory_FS__File__Config


class File_FS__Content(Type_Safe):
    file__config: Schema__Memory_FS__File__Config
    storage_fs  : Storage_FS

    ###### File_FS__* methods #######

    @cache_on_self
    def file_fs__exists(self):
        return File_FS__Exists(file__config=self.file__config, storage_fs=self.storage_fs)

    @cache_on_self                                                              # todo: add to project principles: the @cache_on_self can only be used in cases like this where we are getting the file__config value from the self.file__config , which means that it is always the same
    def file_fs__paths(self):
        return File_FS__Paths(file__config=self.file__config)

    @cache_on_self
    def file_fs__serializer(self):
        return File_FS__Serializer()

    ###### File_FS__Content Methods #######

    def bytes(self) -> bytes:
        for path in self.file_fs__paths().paths__content():                     # todo: see if we need something like Enum__Memory_FS__File__Exists_Strategy here, since at the moment this is going to go through all files, and return when we find some data
            file_bytes = self.storage_fs.file__bytes(path)
            if file_bytes:                                                      # todo: see if we should get this info from the metadata, or if it is ok to just load the first one we find , or if we should be following the Enum__Memory_FS__File__Exists_Strategy strategy
                return file_bytes

    def create(self, content: bytes) -> List[Safe_Str__File__Path]:
        return self.save(content=content)

    def content(self) -> Any:
        return self.load()

    def load(self) -> Any:
        file_type     = self.file__config.file_type
        content_bytes = self.bytes()
        file_data     = self.file_fs__serializer().deserialize(content_bytes, file_type)       # todo: see if we shouldn't be using File_FS__Load here
        return file_data

    def exists(self) -> bool:
        return self.file_fs__exists().content()

    def save(self, content:bytes) -> List[Safe_Str__File__Path]:
        files_to_save = self.file_fs__paths().paths__content()
        files_saved = []
        for file_to_save in files_to_save:
            if self.storage_fs.file__save(file_to_save, content):
                files_saved.append(file_to_save)
        return files_saved

    def update(self, content:bytes) -> List[Safe_Str__File__Path]:
        return self.save(content=content)




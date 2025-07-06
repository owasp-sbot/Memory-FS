from typing                                             import List, Any

from memory_fs.file_fs.data.File_FS__Config import File_FS__Config
from memory_fs.file_fs.data.File_FS__Content            import File_FS__Content
from memory_fs.file_fs.actions.File_FS__Serializer      import File_FS__Serializer
from memory_fs.file_fs.data.File_FS__Metadata           import File_FS__Metadata
from memory_fs.storage_fs.Storage_FS                    import Storage_FS
from osbot_utils.type_safe.decorators.type_safe         import type_safe
from osbot_utils.utils.Json                             import json_to_bytes
from memory_fs.file_fs.actions.File_FS__Exists          import File_FS__Exists
from memory_fs.file_fs.actions.File_FS__Paths           import File_FS__Paths
from osbot_utils.decorators.methods.cache_on_self       import cache_on_self
from memory_fs.schemas.Schema__Memory_FS__File__Config  import Schema__Memory_FS__File__Config
from osbot_utils.type_safe.Type_Safe                    import Type_Safe

# todo: move the note below to https://github.com/owasp-sbot/Memory-FS/blob/dev/docs/memory_fs/file/actions/Memory_FS__File__Create.md
#       this is where we are going to be storing details about each class

# note: config file can only be created or deleted (it cannot be edited)

class File_FS__Create(Type_Safe):                                                       # todo: refactor to file_fs__create
    file__config: Schema__Memory_FS__File__Config
    storage_fs  : Storage_FS

    ###### File_FS__* methods #######

    @cache_on_self
    def file_fs__config(self):
        return File_FS__Config(file__config=self.file__config, storage_fs=self.storage_fs)

    @cache_on_self
    def file_fs__content(self):
        return File_FS__Content(file__config=self.file__config, storage_fs=self.storage_fs)

    @cache_on_self
    def file_fs__exists(self):
        return File_FS__Exists(file__config=self.file__config, storage_fs=self.storage_fs)

    @cache_on_self
    def file_fs__metadata(self):
        return File_FS__Metadata(file__config=self.file__config, storage_fs=self.storage_fs)

    @cache_on_self
    def file_fs__paths(self):                                                                      # todo: refactor to file_fs__paths
        return File_FS__Paths(file__config=self.file__config)

    @cache_on_self
    def file_fs__serializer(self):
        return File_FS__Serializer()


    ###### File_FS__Create Methods #######

    def create(self, file_data: Any) -> List:
        file_type     = self.file__config.file_type
        content       = self.file_fs__serializer().serialize(file_data, file_type)
        files_created = (self.create__config  () +
                         self.create__content (content=content) +
                         self.create__metadata(content=content))
        return sorted(files_created)

    def create__config(self):
        return self.file_fs__config().create()

    @type_safe
    def create__content(self, content: bytes):
        return self.file_fs__content().create(content=content)

    def create__metadata(self, content: bytes):
        return self.file_fs__metadata().create(content=content)

    def delete(self):
        files_deleted = (self.delete__config   () +             # todo: should be file_fs__config().delete()
                         self.delete__content  () +             # todo: should be file_fs__content().delete()
                         self.file_fs__metadata().delete())
        return sorted(files_deleted)

    # todo refactor to return self.file_fs__config().delete()
    def delete__config(self):                                   # todo: # refactor to File_FS__Delete
        files_deleted = []                                      # todo: refactor with delete__content since the code is just about the same
        for file_path in self.file_fs__paths().paths__config():
            if self.storage_fs.file__delete(path=file_path):
                files_deleted.append(file_path)
        return files_deleted

    # todo refactor to return self.file_fs__content().delete()
    def delete__content(self):                                  # todo: refactor to File_FS__Delete
        files_deleted = []
        for file_path in self.file_fs__paths().paths__content():
            if self.storage_fs.file__delete(path=file_path):
                files_deleted.append(file_path)
        return files_deleted

    def exists(self) -> bool:
        return self.file_fs__exists().config()                  # we use the .config file to determine if the file exists

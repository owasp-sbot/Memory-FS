from typing                                                 import Any
from memory_fs.file_fs.actions.File_FS__Exists              import File_FS__Exists
from memory_fs.file_fs.actions.File_FS__Info                import File_FS__Info
from memory_fs.file_fs.actions.File_FS__Update              import File_FS__Update
from memory_fs.file_fs.data.File_FS__Data                   import File_FS__Data
from memory_fs.storage_fs.Storage_FS                        import Storage_FS
from osbot_utils.helpers.safe_str.Safe_Str__Hash            import safe_str_hash
from memory_fs.file_fs.actions.File_FS__Create              import File_FS__Create
from memory_fs.file_fs.actions.File_FS__Edit                import File_FS__Edit
from memory_fs.schemas.Schema__Memory_FS__File__Config      import Schema__Memory_FS__File__Config
from memory_fs.schemas.Schema__Memory_FS__File__Metadata    import Schema__Memory_FS__File__Metadata
from osbot_utils.decorators.methods.cache_on_self           import cache_on_self
from osbot_utils.type_safe.Type_Safe                        import Type_Safe



class File_FS(Type_Safe):
    file_config : Schema__Memory_FS__File__Config                   # todo: rename to file__config (for consistency with other classes)
    #storage     : Memory_FS__Storage
    storage_fs  : Storage_FS

    ###### File_FS__* methods #######

    @cache_on_self
    def file_fs__create(self):
        return File_FS__Create(file__config=self.file_config, storage_fs=self.storage_fs)

    @cache_on_self
    def file_fs__data(self):
        return File_FS__Data(file__config=self.file_config, storage_fs= self.storage_fs)

    @cache_on_self
    def file_fs__edit(self):
        return File_FS__Edit(file__config=self.file_config, storage_fs= self.storage_fs)

    @cache_on_self
    def file_fs__exists(self):
        return File_FS__Exists(file__config=self.file_config, storage_fs= self.storage_fs)

    @cache_on_self
    def file_fs__info(self):
        return File_FS__Info(file__config=self.file_config, storage_fs= self.storage_fs)

    @cache_on_self
    def file_fs__update(self):
        return File_FS__Update(file__config=self.file_config, storage_fs=self.storage_fs)


    ###### Class methods #######

    def create(self, file_data: Any):
        return self.file_fs__create().create(file_data=file_data)

    def create__config(self):
        return self.file_fs__create().create__config()

    def create__content(self, content: bytes):                                                   # todo: this is a temp method to help with some of the legacy unit tests, since we really shouldn't be doing this directly
        return self.file_fs__create().create__content(content=content)

    def create__metadata(self, content: bytes):                                                  # todo: this is a temp method to help with some of the legacy unit tests, since we really shouldn't be doing this directly
        return self.file_fs__create().create__metadata(content=content)

    # def create__both(self, file_data: Any):                                                     # todo: this is a temporary method, to simulate the creation of both files
    #     return sorted(self.create() + self.save(file_data=file_data))                           # todo: see if implications of doing this sort here

    def config(self) -> Schema__Memory_FS__File__Config:
        return self.file_fs__data().config()

    def content(self) -> bytes:                         # this is the raw content (i.e. bytes)
        return self.file_fs__data().content()           # todo: see if 'bytes' or 'raw_content' is a better name for this method

    def data(self) -> Any:
        return self.file_fs__data().data()                # this is the serialised data

    def delete(self):                                                                                   # BUG: the delete should delete all files not just the config
        return self.file_fs__create().delete()

    def delete__content(self):
        return self.file_fs__create().delete__content()

    def exists(self):
        return self.file_fs__exists().config()                                                          # use the .config() existence as the 'file exists' metric

    def exists__content(self):
        return self.file_fs__exists().content()                                                         # todo: see if (apart from unit tests) we need this method

    def exists__metadata(self):
        return self.file_fs__exists().metadata()                                                         # todo: see if (apart from unit tests) we need this method

    def info(self):
        return self.file_fs__info().info()

    def file_id(self):
        return self.file_config.file_id


    def metadata(self):
        content      = self.content()
        metadata = Schema__Memory_FS__File__Metadata()                                                  # todo: implement the logic to create, load and save the metadata file
        if content:
            metadata.content__hash = safe_str_hash(content)                                    # todo: this should be calculated on create/edit (and saved to storage)
        return metadata

    def save(self, file_data: Any):
        saved_files   = self.file_fs__update().update(file_data=file_data)                  # todo: see if this should still be .create_content (and not .update_content )
        return saved_files

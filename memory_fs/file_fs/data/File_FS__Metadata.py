from typing import List

from osbot_utils.utils.Dev import pprint

from memory_fs.file_fs.actions.File_FS__Exists import File_FS__Exists
from osbot_utils.utils.Json import json_to_bytes

from osbot_utils.helpers.safe_str.Safe_Str__File__Path import Safe_Str__File__Path

from memory_fs.file_fs.actions.File_FS__Paths import File_FS__Paths
from memory_fs.schemas.Schema__Memory_FS__File__Config      import Schema__Memory_FS__File__Config
from memory_fs.schemas.Schema__Memory_FS__File__Metadata    import Schema__Memory_FS__File__Metadata
from memory_fs.storage_fs.Storage_FS                        import Storage_FS
from osbot_utils.helpers.safe_str.Safe_Str__Hash            import safe_str_hash
from osbot_utils.decorators.methods.cache_on_self           import cache_on_self
from memory_fs.file_fs.data.File_FS__Content                import File_FS__Content
from osbot_utils.type_safe.Type_Safe                        import Type_Safe

# todo: most methods here need to be refactored with the other similar methods in File_FS__Config and File_FS__Content
class File_FS__Metadata(Type_Safe):
    file__config : Schema__Memory_FS__File__Config
    storage_fs  : Storage_FS

    ###### File_FS__* methods #######
    @cache_on_self
    def file_fs__exists(self):
        return File_FS__Exists(file__config=self.file__config, storage_fs=self.storage_fs)

    @cache_on_self
    def file_fs__paths(self):
        return File_FS__Paths(file__config=self.file__config)


    ###### File_FS__Metadata methods #######

    def create(self, content: bytes) -> List[Safe_Str__File__Path]:
        if self.exists() is False:
            file_metadata = self.default()
            self.update_metadata_obj(file_metadata=file_metadata, content=content)
            json_data     = file_metadata.json()
            content__bytes = json_to_bytes(json_data)
            files_to_save = self.file_fs__paths().paths__metadata()
            files_saved   = []
            for file_to_save in files_to_save:
                if self.storage_fs.file__save(file_to_save, content__bytes):
                    files_saved.append(file_to_save)
            return files_saved
        return []

    def delete(self):
        files_deleted = []
        for file_path in self.file_fs__paths().paths__metadata():
            if self.storage_fs.file__delete(path=file_path):
                files_deleted.append(file_path)
        return files_deleted

    def default(self):
        return Schema__Memory_FS__File__Metadata()

    def exists(self) -> bool:
        return self.file_fs__exists().metadata()

    def load(self) -> Schema__Memory_FS__File__Metadata:                                                                # todo: see if for consistency this should be called .data()
        if self.exists() is False:
            return self.default()

        for path in self.file_fs__paths().paths__metadata():
            json_data = self.storage_fs.file__json(path)
            if json_data:
                return Schema__Memory_FS__File__Metadata.from_json(json_data)

    def paths(self):
        return self.file_fs__paths().paths__metadata()

    @cache_on_self
    def file_fs__content(self):                                                                                         # todo: see if we should have this dependency here (or if this class should receive the file's bytes, data, and config)
        return File_FS__Content(file__config=self.file__config, storage_fs=self.storage_fs)

    def metadata(self) -> Schema__Memory_FS__File__Metadata:
        content_bytes = self.file_fs__content().bytes()
        metadata      = Schema__Memory_FS__File__Metadata()
        if content_bytes:
            metadata.content__hash = safe_str_hash(content_bytes.decode())                                  # todo: this should be calculated on create/edit (and saved to storage), and this need refactored into separate method (if not class)
        return metadata

    def update_metadata_obj(self, file_metadata: Schema__Memory_FS__File__Metadata, content:bytes):         # figure out a better way to implement this
        #if content is None:                                                                                        # todo: see if we need to support the case when content is None
        # else:
        #     content__hash = None
        #     content__size = 0
        content__hash = safe_str_hash(content.decode())
        content__size = len(content)

        file_metadata.content__hash = content__hash
        file_metadata.content__size = content__size
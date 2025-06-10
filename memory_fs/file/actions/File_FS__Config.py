from memory_fs.file.actions.File_FS__Data               import File_FS__Data
from memory_fs.file.actions.File_FS__Name               import File_FS__Name
from memory_fs.file.actions.File_FS__Paths              import File_FS__Paths
from memory_fs.schemas.Schema__Memory_FS__File__Config  import Schema__Memory_FS__File__Config
from memory_fs.storage.Memory_FS__Storage               import Memory_FS__Storage
from osbot_utils.type_safe.Type_Safe                    import Type_Safe

class File_FS__Config(Type_Safe):               # todo: refactor the methods from this class that are the same for the .content() and .metadata() files
    file__config : Schema__Memory_FS__File__Config
    storage      : Memory_FS__Storage


    def file_fs__data(self):
        return File_FS__Data(file__config=self.file__config, storage=self.storage)

    def file_fs__name(self):
        return File_FS__Name(file__config=self.file__config)

    def file_fs__paths(self):
        return File_FS__Paths(file__config=self.file__config)


    def file_config(self):                              # todo: see if this is the best name to call this method
        return self.file__config                        # todo: see if we should be loading this file at this time, since we already have a copy of the config object in self.file__config


    def file_id(self):
        return self.file__config.file_id

    def file_name(self):
        return self.file_fs__name().config()

    def exists(self):
        return self.file_fs__data().exists()


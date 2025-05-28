from memory_fs.file.Memory_FS__File                     import Memory_FS__File
from memory_fs.file.Memory_FS__File__Storage            import Memory_FS__File__Storage
from memory_fs.file_types.Memory_FS__File__Type__Txt    import Memory_FS__File__Type__Text
from memory_fs.storage.Memory_FS__Storage               import Memory_FS__Storage
from osbot_utils.helpers.Safe_Id                        import Safe_Id
from osbot_utils.type_safe.Type_Safe                    import Type_Safe


class Memory_FS__File__New(Type_Safe):
    storage     : Memory_FS__Storage
    file_storage: Memory_FS__File__Storage

    def txt(self, file_name:Safe_Id):
        with Memory_FS__File()  as file:
            with file.config() as _:
                _.file_type  = Memory_FS__File__Type__Text()
                _.file_paths = self.file_storage.file__paths()
                _.file_name  = file_name
            return file
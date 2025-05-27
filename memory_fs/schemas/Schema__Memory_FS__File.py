from osbot_utils.helpers.Random_Guid                     import Random_Guid
from osbot_utils.type_safe.Type_Safe                     import Type_Safe
from memory_fs.schemas.Schema__Memory_FS__File__Config   import Schema__Memory_FS__File__Config
from memory_fs.schemas.Schema__Memory_FS__File__Metadata import Schema__Memory_FS__File__Metadata


class Schema__Memory_FS__File(Type_Safe):
    config   : Schema__Memory_FS__File__Config
    file_id  : Random_Guid
    metadata : Schema__Memory_FS__File__Metadata
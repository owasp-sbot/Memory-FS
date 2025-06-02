# TODO and BUG Mapping

This document lists all TODO and BUG comments currently in the codebase.

## TODO Comments

| File | Line | Comment |
| ---- | ---- | ------- |
| [memory_fs/actions/Memory_FS__Data.py](https://github.com/owasp-sbot/Memory-FS/blob/main/memory_fs/actions/Memory_FS__Data.py#L21) | 21 | see if we need to add the default path (or to have a separate "exists strategy") |
| [memory_fs/actions/Memory_FS__Data.py](https://github.com/owasp-sbot/Memory-FS/blob/main/memory_fs/actions/Memory_FS__Data.py#L24) | 24 | refactor since this is going to be platform specific (specially since we shouldn't circle through all files to see if the file exists) |
| [memory_fs/actions/Memory_FS__Data.py](https://github.com/owasp-sbot/Memory-FS/blob/main/memory_fs/actions/Memory_FS__Data.py#L37) | 37 | this method should return a strongly typed class (ideally one from the file) |
| [memory_fs/actions/Memory_FS__Data.py](https://github.com/owasp-sbot/Memory-FS/blob/main/memory_fs/actions/Memory_FS__Data.py#L52) | 52 | see if we need this method |
| [memory_fs/actions/Memory_FS__Data.py](https://github.com/owasp-sbot/Memory-FS/blob/main/memory_fs/actions/Memory_FS__Data.py#L73) | 73 | this should return a python object (and most likely moved into a Memory_FS__Stats class) |
| [memory_fs/actions/Memory_FS__Data.py](https://github.com/owasp-sbot/Memory-FS/blob/main/memory_fs/actions/Memory_FS__Data.py#L77) | 77 | use the file size instead |
| [memory_fs/actions/Memory_FS__Edit.py](https://github.com/owasp-sbot/Memory-FS/blob/main/memory_fs/actions/Memory_FS__Edit.py#L20) | 20 | refactor this logic to storage |
| [memory_fs/actions/Memory_FS__Edit.py](https://github.com/owasp-sbot/Memory-FS/blob/main/memory_fs/actions/Memory_FS__Edit.py#L24) | 24 | refactor with logic in delete_content since 90% of the code is the same |
| [memory_fs/actions/Memory_FS__Edit.py](https://github.com/owasp-sbot/Memory-FS/blob/main/memory_fs/actions/Memory_FS__Edit.py#L29) | 29 | this needs to be abstracted out in the storage class |
| [memory_fs/actions/Memory_FS__Edit.py](https://github.com/owasp-sbot/Memory-FS/blob/main/memory_fs/actions/Memory_FS__Edit.py#L39) | 39 | this needs to be abstracted out in the storage class |
| [memory_fs/actions/Memory_FS__Edit.py](https://github.com/owasp-sbot/Memory-FS/blob/main/memory_fs/actions/Memory_FS__Edit.py#L44) | 44 | find a better name for this method and file ('fs' is okish, maybe 'config') |
| [memory_fs/actions/Memory_FS__Edit.py](https://github.com/owasp-sbot/Memory-FS/blob/main/memory_fs/actions/Memory_FS__Edit.py#L52) | 52 | this needs to be moved into the storage class |
| [memory_fs/actions/Memory_FS__Edit.py](https://github.com/owasp-sbot/Memory-FS/blob/main/memory_fs/actions/Memory_FS__Edit.py#L56) | 56 | need to updated the metadata file save the length in the metadata |
| [memory_fs/actions/Memory_FS__Edit.py](https://github.com/owasp-sbot/Memory-FS/blob/main/memory_fs/actions/Memory_FS__Edit.py#L62) | 62 | this needs to be moved into the storage class |
| [memory_fs/actions/Memory_FS__Edit.py](https://github.com/owasp-sbot/Memory-FS/blob/main/memory_fs/actions/Memory_FS__Edit.py#L67) | 67 | see if we need this, since now that we have multiple paths support, the logic in the copy is more complicated |
| [memory_fs/actions/Memory_FS__Edit.py](https://github.com/owasp-sbot/Memory-FS/blob/main/memory_fs/actions/Memory_FS__Edit.py#L78) | 78 | need to refactor the logic of the files and the support files |
| [memory_fs/actions/Memory_FS__Edit.py](https://github.com/owasp-sbot/Memory-FS/blob/main/memory_fs/actions/Memory_FS__Edit.py#L83) | 83 | see if we need this, since now that we have multiple paths support, the logic in the move is more complicated |
| [memory_fs/actions/Memory_FS__Paths.py](https://github.com/owasp-sbot/Memory-FS/blob/main/memory_fs/actions/Memory_FS__Paths.py#L18) | 18 | refactor this into a better location |
| [memory_fs/actions/Memory_FS__Paths.py](https://github.com/owasp-sbot/Memory-FS/blob/main/memory_fs/actions/Memory_FS__Paths.py#L22) | 22 | fix the use of this hard-coded + ".fs.json" |
| [memory_fs/actions/Memory_FS__Save.py](https://github.com/owasp-sbot/Memory-FS/blob/main/memory_fs/actions/Memory_FS__Save.py#L40) | 40 | see if we still need this (also this check should happen inside the _serialize_data method, since that is the one that needs this data) |
| [memory_fs/core/Memory_FS__File_System.py](https://github.com/owasp-sbot/Memory-FS/blob/main/memory_fs/core/Memory_FS__File_System.py#L6) | 6 | find better name for this class since this is the one that simulates the actually File System (and this is in the 'core' folder) |
| [memory_fs/file/Memory_FS__File.py](https://github.com/owasp-sbot/Memory-FS/blob/main/memory_fs/file/Memory_FS__File.py#L22) | 22 | see if we need them (i.e. are they really useful and make it easy for dev's experience) |
| [memory_fs/file/actions/Memory_FS__File__Edit.py](https://github.com/owasp-sbot/Memory-FS/blob/main/memory_fs/file/actions/Memory_FS__File__Edit.py#L29) | 29 | this logic should be inside the storage_data |
| [memory_fs/path_handlers/Path__Handler__Temporal.py](https://github.com/owasp-sbot/Memory-FS/blob/main/memory_fs/path_handlers/Path__Handler__Temporal.py#L10) | 10 | refactor to Path__Handler__Areas, this Path__Handler__Temporal should only have the date based path |
| [memory_fs/path_handlers/Path__Handler__Temporal.py](https://github.com/owasp-sbot/Memory-FS/blob/main/memory_fs/path_handlers/Path__Handler__Temporal.py#L12) | 12 | refactor to the more comprehensive date path generation we have in the HackerNews (where we can also control which date and time element to use (from year to miliseconds) |
| [memory_fs/path_handlers/__init__.py](https://github.com/owasp-sbot/Memory-FS/blob/main/memory_fs/path_handlers/__init__.py#L10) | 10 | change this logic, since the metadata file should always be stored in a particular location |
| [memory_fs/schemas/Schema__Memory_FS__File.py](https://github.com/owasp-sbot/Memory-FS/blob/main/memory_fs/schemas/Schema__Memory_FS__File.py#L6) | 6 | see if we still need this schema file, since we are going to have two files created |
| [memory_fs/schemas/Schema__Memory_FS__File__Metadata.py](https://github.com/owasp-sbot/Memory-FS/blob/main/memory_fs/schemas/Schema__Memory_FS__File__Metadata.py#L14) | 14 | refactor this logic into a better naming convention and class structure |
| [memory_fs/schemas/Schema__Memory_FS__File__Metadata.py](https://github.com/owasp-sbot/Memory-FS/blob/main/memory_fs/schemas/Schema__Memory_FS__File__Metadata.py#L15) | 15 | should we move this into an 'user_data' section (since this is the only part of this data object that us editable by the user |
| [memory_fs/storage/Memory_FS__Storage.py](https://github.com/owasp-sbot/Memory-FS/blob/main/memory_fs/storage/Memory_FS__Storage.py#L7) | 7 | we need to refactor this into class that has all the methods below, but has no access to the memory object (since each provider will have it's own version of it) |
| [memory_fs/storage/Memory_FS__Storage.py](https://github.com/owasp-sbot/Memory-FS/blob/main/memory_fs/storage/Memory_FS__Storage.py#L12) | 12 | review this usage since at the moment this is returning the file's .fs.json data |
| [memory_fs/storage/Memory_FS__Storage.py](https://github.com/owasp-sbot/Memory-FS/blob/main/memory_fs/storage/Memory_FS__Storage.py#L21) | 21 | see if we need this, this could be lots of data |
| [memory_fs/storage/Memory_FS__Storage.py](https://github.com/owasp-sbot/Memory-FS/blob/main/memory_fs/storage/Memory_FS__Storage.py#L24) | 24 | see if we need this method |
| [tests/unit/memory/test_Memory_FS__Memory__File_System.py](https://github.com/owasp-sbot/Memory-FS/blob/main/tests/unit/memory/test_Memory_FS__Memory__File_System.py#L15) | 15 | all this logic needs to be refactored into the new Memory_FS__* classes |
| [tests/unit/memory/test_Memory_FS__Memory__File_System.py](https://github.com/owasp-sbot/Memory-FS/blob/main/tests/unit/memory/test_Memory_FS__Memory__File_System.py#L130) | 130 | see if we need this, since now that we have multiple paths support, the logic in the move is more complicated |
| [tests/unit/memory/test_Memory_FS__Memory__File_System.py](https://github.com/owasp-sbot/Memory-FS/blob/main/tests/unit/memory/test_Memory_FS__Memory__File_System.py#L149) | 149 | see if we need this, since now that we have multiple paths support, the logic in the copy is more complicated |
| [tests/unit/memory/test_Memory_FS__Memory__Storage.py](https://github.com/owasp-sbot/Memory-FS/blob/main/tests/unit/memory/test_Memory_FS__Memory__Storage.py#L212) | 212 | figure out a better way to name this since these are the fs.json files (i.e. this all files doesn't include the content files, which could be an expectation) |
| [tests/unit/memory/test_Memory_FS__Memory__Storage.py](https://github.com/owasp-sbot/Memory-FS/blob/main/tests/unit/memory/test_Memory_FS__Memory__Storage.py#L250) | 250 | double check this value |

## BUG Comments

| File | Line | Comment |
| ---- | ---- | ------- |
| [tests/unit/file/actions/test_Memory_FS__File__Edit.py](https://github.com/owasp-sbot/Memory-FS/blob/main/tests/unit/file/actions/test_Memory_FS__File__Edit.py#L30) | 30 | but we are not handling ok when file_type.file_extension is not set |
| [tests/unit/memory/test_Memory_FS__Memory__File_System.py](https://github.com/owasp-sbot/Memory-FS/blob/main/tests/unit/memory/test_Memory_FS__Memory__File_System.py#L67) | 67 |  |
| [tests/unit/memory/test_Memory_FS__Memory__File_System.py](https://github.com/owasp-sbot/Memory-FS/blob/main/tests/unit/memory/test_Memory_FS__Memory__File_System.py#L68) | 68 |  |
| [tests/unit/memory/test_Memory_FS__Memory__File_System.py](https://github.com/owasp-sbot/Memory-FS/blob/main/tests/unit/memory/test_Memory_FS__Memory__File_System.py#L75) | 75 | todo: bug the size is not being captured on the save action |

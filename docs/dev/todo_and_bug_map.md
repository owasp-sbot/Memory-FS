# TODO and BUG Mapping

This document summarises all inline `TODO` and `BUG` comments currently present in the code base. Each entry points to the exact location in the repository so that open issues can easily be reviewed. The list is maintained manually and should be updated whenever comments are added, removed or resolved.

## TODO Comments

| File | Line | Comment |
| ---- | ---- | ------- |
| [memory_fs/actions/Memory_FS__Data.py](https://github.com/owasp-sbot/Memory-FS/blob/main/memory_fs/actions/Memory_FS__Data.py#L19) | 19 | see if we need to add the default path (or to have a separate "exists strategy") |
| [memory_fs/actions/Memory_FS__Data.py](https://github.com/owasp-sbot/Memory-FS/blob/main/memory_fs/actions/Memory_FS__Data.py#L22) | 22 | refactor since this is going to be platform specific (specially since we shouldn't circle through all files to see if the file exists) |
| [memory_fs/actions/Memory_FS__Data.py](https://github.com/owasp-sbot/Memory-FS/blob/main/memory_fs/actions/Memory_FS__Data.py#L35) | 35 | this method should return a strongly typed class (ideally one from the file) |
| [memory_fs/actions/Memory_FS__Data.py](https://github.com/owasp-sbot/Memory-FS/blob/main/memory_fs/actions/Memory_FS__Data.py#L50) | 50 | see if we need this method |
| [memory_fs/actions/Memory_FS__Data.py](https://github.com/owasp-sbot/Memory-FS/blob/main/memory_fs/actions/Memory_FS__Data.py#L71) | 71 | this should return a python object (and most likely moved into a Memory_FS__Stats class) |
| [memory_fs/actions/Memory_FS__Data.py](https://github.com/owasp-sbot/Memory-FS/blob/main/memory_fs/actions/Memory_FS__Data.py#L75) | 75 | use the file size instead |
| [memory_fs/actions/Memory_FS__Edit.py](https://github.com/owasp-sbot/Memory-FS/blob/main/memory_fs/actions/Memory_FS__Edit.py#L18) | 18 | refactor this logic to storage |
| [memory_fs/actions/Memory_FS__Edit.py](https://github.com/owasp-sbot/Memory-FS/blob/main/memory_fs/actions/Memory_FS__Edit.py#L22) | 22 | refactor with logic in delete_content since 90% of the code is the same |
| [memory_fs/actions/Memory_FS__Edit.py](https://github.com/owasp-sbot/Memory-FS/blob/main/memory_fs/actions/Memory_FS__Edit.py#L27) | 27 | this needs to be abstracted out in the storage class |
| [memory_fs/actions/Memory_FS__Edit.py](https://github.com/owasp-sbot/Memory-FS/blob/main/memory_fs/actions/Memory_FS__Edit.py#L37) | 37 | this needs to be abstracted out in the storage class |
| [memory_fs/actions/Memory_FS__Edit.py](https://github.com/owasp-sbot/Memory-FS/blob/main/memory_fs/actions/Memory_FS__Edit.py#L42) | 42 | find a better name for this method and file ('fs' is okish, maybe 'config') |
| [memory_fs/actions/Memory_FS__Edit.py](https://github.com/owasp-sbot/Memory-FS/blob/main/memory_fs/actions/Memory_FS__Edit.py#L50) | 50 | this needs to be moved into the storage class |
| [memory_fs/actions/Memory_FS__Edit.py](https://github.com/owasp-sbot/Memory-FS/blob/main/memory_fs/actions/Memory_FS__Edit.py#L54) | 54 | need to updated the metadata file save the length in the metadata |
| [memory_fs/actions/Memory_FS__Edit.py](https://github.com/owasp-sbot/Memory-FS/blob/main/memory_fs/actions/Memory_FS__Edit.py#L60) | 60 | this needs to be moved into the storage class |
| [memory_fs/actions/Memory_FS__Edit.py](https://github.com/owasp-sbot/Memory-FS/blob/main/memory_fs/actions/Memory_FS__Edit.py#L65) | 65 | see if we need this, since now that we have multiple paths support, the logic in the copy is more complicated |
| [memory_fs/actions/Memory_FS__Edit.py](https://github.com/owasp-sbot/Memory-FS/blob/main/memory_fs/actions/Memory_FS__Edit.py#L76) | 76 | need to refactor the logic of the files and the support files |
| [memory_fs/actions/Memory_FS__Edit.py](https://github.com/owasp-sbot/Memory-FS/blob/main/memory_fs/actions/Memory_FS__Edit.py#L81) | 81 | see if we need this, since now that we have multiple paths support, the logic in the move is more complicated |
| [memory_fs/actions/Memory_FS__Save.py](https://github.com/owasp-sbot/Memory-FS/blob/main/memory_fs/actions/Memory_FS__Save.py#L35) | 35 | see if we still need this (also this check should happen inside the _serialize_data method, since that is the one that needs this data) |
| [memory_fs/core/Memory_FS__File_System.py](https://github.com/owasp-sbot/Memory-FS/blob/main/memory_fs/core/Memory_FS__File_System.py#L6) | 6 | find better name for this class since this is the one that simulates the actually File System (and this is in the 'core' folder) |
| [memory_fs/file/Memory_FS__File.py](https://github.com/owasp-sbot/Memory-FS/blob/main/memory_fs/file/Memory_FS__File.py#L27) | 27 | see if we need them (i.e.are they really useful and make it easy for dev's experience) |
| [memory_fs/file/actions/Memory_FS__File__Create.py](https://github.com/owasp-sbot/Memory-FS/blob/main/memory_fs/file/actions/Memory_FS__File__Create.py#L9) | 9 | move the note below to separate documentation |
| [memory_fs/file/actions/Memory_FS__File__Edit.py](https://github.com/owasp-sbot/Memory-FS/blob/main/memory_fs/file/actions/Memory_FS__File__Edit.py#L31) | 31 | remove since this is covered by file__paths |
| [memory_fs/file/actions/Memory_FS__File__Edit.py](https://github.com/owasp-sbot/Memory-FS/blob/main/memory_fs/file/actions/Memory_FS__File__Edit.py#L37) | 37 | this logic should be inside the storage_data |
| [memory_fs/file/actions/Memory_FS__File__Name.py](https://github.com/owasp-sbot/Memory-FS/blob/main/memory_fs/file/actions/Memory_FS__File__Name.py#L36) | 36 | see if need the str(..) here |
| [memory_fs/file/actions/Memory_FS__File__Paths.py](https://github.com/owasp-sbot/Memory-FS/blob/main/memory_fs/file/actions/Memory_FS__File__Paths.py#L8) | 8 |  |
| [memory_fs/file/actions/Memory_FS__File__Paths.py](https://github.com/owasp-sbot/Memory-FS/blob/main/memory_fs/file/actions/Memory_FS__File__Paths.py#L21) | 21 | this file should return all paths (config, content and metadata), not just the config ones |
| [memory_fs/file/storage_fs/Storage_FS__Local_Disk.py](https://github.com/owasp-sbot/Memory-FS/blob/main/memory_fs/file/storage_fs/Storage_FS__Local_Disk.py#L4) | 4 | need implementation |
| [memory_fs/file/storage_fs/Storage_FS__Memory.py](https://github.com/owasp-sbot/Memory-FS/blob/main/memory_fs/file/storage_fs/Storage_FS__Memory.py#L7) | 7 | see if this class shouldn't be leveraging the Serialisation and DeSerialisation classes/logic |
| [memory_fs/file/storage_fs/Storage_FS__Memory.py](https://github.com/owasp-sbot/Memory-FS/blob/main/memory_fs/file/storage_fs/Storage_FS__Memory.py#L35) | 35 | add content type to this decode |
| [memory_fs/file/storage_fs/Storage_FS__Sqlite.py](https://github.com/owasp-sbot/Memory-FS/blob/main/memory_fs/file/storage_fs/Storage_FS__Sqlite.py#L4) | 4 | need implementation |
| [memory_fs/file/storage_fs/Storage_FS__Zip.py](https://github.com/owasp-sbot/Memory-FS/blob/main/memory_fs/file/storage_fs/Storage_FS__Zip.py#L4) | 4 | need implementation |
| [memory_fs/path_handlers/Path__Handler__Temporal.py](https://github.com/owasp-sbot/Memory-FS/blob/main/memory_fs/path_handlers/Path__Handler__Temporal.py#L10) | 10 | refactor to Path__Handler__Areas, this Path__Handler__Temporal should only have the date based path |
| [memory_fs/path_handlers/Path__Handler__Temporal.py](https://github.com/owasp-sbot/Memory-FS/blob/main/memory_fs/path_handlers/Path__Handler__Temporal.py#L12) | 12 | refactor to the more comprehensive date path generation we have in the HackerNews |
| [memory_fs/schemas/Schema__Memory_FS__File.py](https://github.com/owasp-sbot/Memory-FS/blob/main/memory_fs/schemas/Schema__Memory_FS__File.py#L6) | 6 | see if we still need this schema file, since we are going to have two files created |
| [memory_fs/schemas/Schema__Memory_FS__File__Metadata.py](https://github.com/owasp-sbot/Memory-FS/blob/main/memory_fs/schemas/Schema__Memory_FS__File__Metadata.py#L14) | 14 | refactor this logic into a better naming convention and class structure |
| [memory_fs/schemas/Schema__Memory_FS__File__Metadata.py](https://github.com/owasp-sbot/Memory-FS/blob/main/memory_fs/schemas/Schema__Memory_FS__File__Metadata.py#L15) | 15 | should we move this into an 'user_data' section |
| [memory_fs/storage/Memory_FS__Storage.py](https://github.com/owasp-sbot/Memory-FS/blob/main/memory_fs/storage/Memory_FS__Storage.py#L9) | 9 | we need to refactor this into class that has all the methods below, but has no access to the memory object |
| [memory_fs/storage/Memory_FS__Storage.py](https://github.com/owasp-sbot/Memory-FS/blob/main/memory_fs/storage/Memory_FS__Storage.py#L24) | 24 | see if we need this, this could be lots of data |
| [memory_fs/storage/Memory_FS__Storage.py](https://github.com/owasp-sbot/Memory-FS/blob/main/memory_fs/storage/Memory_FS__Storage.py#L27) | 27 | see if we need this method |
| [tests/unit/actions/test_Memory_FS__Paths.py](https://github.com/owasp-sbot/Memory-FS/blob/main/tests/unit/actions/test_Memory_FS__Paths.py#L145) | 145 | Test areas marked with TODO comments |
| [tests/unit/actions/test_Memory_FS__Paths.py](https://github.com/owasp-sbot/Memory-FS/blob/main/tests/unit/actions/test_Memory_FS__Paths.py#L146) | 146 | TODO items mentioned in the code: |
| [tests/unit/file/actions/test_Memory_FS__File__Create.py](https://github.com/owasp-sbot/Memory-FS/blob/main/tests/unit/file/actions/test_Memory_FS__File__Create.py#L13) | 13 | find a better way to use the Storage_FS__Memory as default in these tests |
| [tests/unit/file/actions/test_Memory_FS__File__Create.py](https://github.com/owasp-sbot/Memory-FS/blob/main/tests/unit/file/actions/test_Memory_FS__File__Create.py#L38) | 38 | refactor once "storage" class is replaced with just storage_fs |
| [tests/unit/memory/test_Memory_FS__Memory__File_System.py](https://github.com/owasp-sbot/Memory-FS/blob/main/tests/unit/memory/test_Memory_FS__Memory__File_System.py#L16) | 16 | all this logic needs to be refactored into the new Memory_FS__* classes |
| [tests/unit/memory/test_Memory_FS__Memory__File_System.py](https://github.com/owasp-sbot/Memory-FS/blob/main/tests/unit/memory/test_Memory_FS__Memory__File_System.py#L76) | 76 | BUG: todo: bug the size is not being captured on the save action |
| [tests/unit/memory/test_Memory_FS__Memory__File_System.py](https://github.com/owasp-sbot/Memory-FS/blob/main/tests/unit/memory/test_Memory_FS__Memory__File_System.py#L131) | 131 | see if we need this, since now that we have multiple paths support, the logic in the move is more complicated |
| [tests/unit/memory/test_Memory_FS__Memory__File_System.py](https://github.com/owasp-sbot/Memory-FS/blob/main/tests/unit/memory/test_Memory_FS__Memory__File_System.py#L150) | 150 | see if we need this, since now that we have multiple paths support, the logic in the copy is more complicated |
| [tests/unit/memory/test_Memory_FS__Memory__Storage.py](https://github.com/owasp-sbot/Memory-FS/blob/main/tests/unit/memory/test_Memory_FS__Memory__Storage.py#L213) | 213 | figure out a better way to name this since these are the fs.json files |
| [tests/unit/memory/test_Memory_FS__Memory__Storage.py](https://github.com/owasp-sbot/Memory-FS/blob/main/tests/unit/memory/test_Memory_FS__Memory__Storage.py#L251) | 251 | double check this value |

## BUG Comments

| File | Line | Comment |
| ---- | ---- | ------- |
| [memory_fs/file/actions/Memory_FS__File__Name.py](https://github.com/owasp-sbot/Memory-FS/blob/main/memory_fs/file/actions/Memory_FS__File__Name.py#L34) | 34 | BUG: need to handle null values in file_extension |
| [tests/unit/file/actions/test_Memory_FS__File__Data.py](https://github.com/owasp-sbot/Memory-FS/blob/main/tests/unit/file/actions/test_Memory_FS__File__Data.py#L29) | 29 | BUG: this should be |
| [tests/unit/file/test_Memory_FS__File.py](https://github.com/owasp-sbot/Memory-FS/blob/main/tests/unit/file/test_Memory_FS__File.py#L32) | 32 | BUG: Should be true |
| [tests/unit/file/test_Memory_FS__File.py](https://github.com/owasp-sbot/Memory-FS/blob/main/tests/unit/file/test_Memory_FS__File.py#L33) | 33 | BUG: Should be false |
| [tests/unit/memory/test_Memory_FS__Memory__File_System.py](https://github.com/owasp-sbot/Memory-FS/blob/main/tests/unit/memory/test_Memory_FS__Memory__File_System.py#L68) | 68 | BUG |
| [tests/unit/memory/test_Memory_FS__Memory__File_System.py](https://github.com/owasp-sbot/Memory-FS/blob/main/tests/unit/memory/test_Memory_FS__Memory__File_System.py#L69) | 69 | BUG |
| [tests/unit/memory/test_Memory_FS__Memory__File_System.py](https://github.com/owasp-sbot/Memory-FS/blob/main/tests/unit/memory/test_Memory_FS__Memory__File_System.py#L76) | 76 | BUG: todo: bug the size is not being captured on the save action |

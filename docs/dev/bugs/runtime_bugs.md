# Runtime Bugs

This file lists open defects observed directly in the source code.

## File management

### Memory_FS__Delete.delete returns wrong type
File: [`memory_fs/actions/Memory_FS__Delete.py`](https://github.com/owasp-sbot/Memory-FS/blob/dev/memory_fs/actions/Memory_FS__Delete.py)
The function advertises `Dict[Safe_Id, bool]` but concatenates two lists of paths, yielding a list instead.

### File name with null extension
File: [`memory_fs/file/actions/File_FS__Name.py`](https://github.com/owasp-sbot/Memory-FS/blob/dev/memory_fs/file/actions/File_FS__Name.py)
When `file_type.file_extension` is `None` the resulting path may include the string `"None"`. The implementation needs to skip adding the extension when not set.

## Metadata

### Content size not captured
Tests show `content__size` remains `0` after saving. The metadata update in [`Memory_FS__Edit.save`](https://github.com/owasp-sbot/Memory-FS/blob/dev/memory_fs/actions/Memory_FS__Edit.py) and related helpers is incomplete.

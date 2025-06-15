# Archived Notes

The following bugs and TODOs were mentioned in early documentation but are no longer present in the code base.

## Removed bugs
- `Memory_FS__File__Create.create` returned `False` when a file already existed. The class has since been refactored and the issue does not appear in `File_FS__Create`.

## Removed TODOs
- `memory_fs/file/Memory_FS__File.py` contained a note questioning certain helper methods. The file itself was removed.
- An old comment in `Memory_FS__File__Edit` referencing `storage_data` is no longer in the current `File_FS__Edit` implementation.

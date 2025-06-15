# Core TODOs

Collected TODO comments for the main API and data management classes.

## Memory_FS__Data
- Review existence checks and consider a default path/"exists" strategy.
- The inline logic for determining file existence is platform specific and should be refactored.
- `get_file_info` should return a strongly typed object.
- Evaluate whether `list_files` is needed.
- The `stats` helper should return a Python object (likely moved to `Memory_FS__Stats`) and rely on file size rather than loading content.

## Memory_FS__Edit
- Several methods are placeholders for future storage refactoring.
- `delete` and `delete_content` share logic that should be combined.
- Saving files should be delegated to the storage classes, including metadata size updates.
- Copy and move helpers are commented out pending a multiple-paths implementation.

## Memory_FS__Save
- Check if validation of `file_type` should happen inside `_serialize_data`.

## Memory_FS__File_System
- The class name needs improvement to better reflect its role as the in-memory file system implementation.

## Memory_FS__Storage
- Requires a redesign to decouple storage operations from the memory object and to leverage `Storage_FS` providers directly.
- Some helper methods (`files__paths`, etc.) may be unnecessary.

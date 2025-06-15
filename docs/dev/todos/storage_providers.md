# Storage Provider TODOs

Items related to the concrete storage backends and helper schemas.

## File actions
- Notes in `File_FS__Create` mention moving documentation elsewhere and refactoring the method naming.
- `File_FS__Edit.storage_paths` should be removed in favour of `file__paths`.
- `File_FS__Name.content` questions whether `str(...)` is required when adding the extension.
- `File_FS__Paths` currently returns only config paths; it should also return content and metadata paths.

## Storage_FS providers
- `Storage_FS__Local_Disk`, `Storage_FS__Sqlite` and `Storage_FS__Zip` require full implementations.
- `Storage_FS__Memory` may need to leverage serialization helpers and include content type when decoding bytes.

## Path handlers
- `Path__Handler__Temporal` should become `Path__Handler__Areas` and reuse improved date path generation.

## Schemas
- Review the need for `Schema__Memory_FS__File` as separate config and metadata files already exist.
- `Schema__Memory_FS__File__Metadata` fields like `previous_version_path` and `tags` require a clearer structure.

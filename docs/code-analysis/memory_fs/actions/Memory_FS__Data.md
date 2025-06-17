# actions/Memory_FS__Data.py


## Description
Implements `Memory_FS__Data` which provides low level operations for reading file metadata and raw content from storage.
## Classes
### Memory_FS__Data
Methods:
- `paths`
- `exists`
- `exists_content`
- `get_file_info`
- `list_files`
- `load`
- `load_content`
- `stats`

```mermaid
flowchart TD
    A[exists(config)] --> B[paths(config)]
    B --> C{found?}
    C -- yes --> D[True]
    C -- no --> E[False]
    A2[list_files(prefix)] --> F[iterate storage files]
    A3[load_content(path)] --> G[storage.file__content(path)]
```

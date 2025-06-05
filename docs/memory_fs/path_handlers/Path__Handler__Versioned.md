# path_handlers/Path__Handler__Versioned.py


## Description
Adds an incremental integer to paths so multiple versions can be saved.
## Classes
### Path__Handler__Versioned
Methods:
- `generate_path`

```mermaid
flowchart TD
    A[generate_path(file_id,ext,version)] --> B[format "v{version}/{file_id}{ext}"]
```

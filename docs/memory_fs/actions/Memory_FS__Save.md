# actions/Memory_FS__Save.py


## Description
High level save routine that serializes data and writes both metadata and content to all configured locations.
## Classes
### Memory_FS__Save
Methods:
- `memory_fs__edit`
- `memory_fs__serialize`
- `save`

```mermaid
flowchart TD
    A[save(data, config)] --> B[_serialize_data]
    B --> C[build metadata]
    C --> D[edit.save(file)]
    C --> E[edit.save_content(bytes)]
    D --> F[paths]
    E --> F
    F --> G[sorted list of paths]
```

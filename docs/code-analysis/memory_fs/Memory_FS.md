# Memory_FS.py


## Description
The main entry point to the in-memory file system. The `Memory_FS` class wires together all action classes such as load, save and delete.
## Classes
### Memory_FS
Methods:
- `data`
- `delete`
- `edit`
- `load`
- `save`

```mermaid
flowchart TD
    A[Memory_FS instance]
    A --> B[data()]
    A --> C[delete()]
    A --> D[edit()]
    A --> E[load()]
    A --> F[save()]
```

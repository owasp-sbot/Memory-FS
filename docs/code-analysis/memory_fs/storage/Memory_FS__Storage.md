# storage/Memory_FS__Storage.py


## Description
Implements the in-memory storage backend used by the rest of the system.
## Classes
### Memory_FS__Storage
Methods:
- `content_data`
- `file`
- `file__content`
- `files`
- `files__contents`
- `files__names`

```mermaid
flowchart TD
    A[Memory_FS__Storage]
    A --> B[files dict]
    A --> C[content_data dict]
    subgraph Access
        D[files()] --> B
        E[file(path)] --> B
        F[file__content(path)] --> C
        G[files__names()] --> B
    end
```

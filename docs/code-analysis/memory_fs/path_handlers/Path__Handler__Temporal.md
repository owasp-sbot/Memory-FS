# path_handlers/Path__Handler__Temporal.py


## Description
Builds a path that embeds a timestamp creating a simple history of versions.
## Classes
### Path__Handler__Temporal
Methods:
- `generate_path`
- `path_now`

```mermaid
flowchart TD
    A[path_now()] --> B[format current time]
    C[generate_path()] --> A
    C --> D[append areas if provided]
```

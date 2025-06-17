# Raw `str` Usages

This page lists all locations in `memory_fs` where plain Python `str` types are used instead of the `Safe_Str` helpers. These spots should be reviewed to determine if they require a safer type.

| File | Line | Code |
| --- | --- | --- |
| [memory_fs/path_handlers/Path__Handler__Custom.py](https://github.com/owasp-sbot/Memory-FS/blob/dev/memory_fs/path_handlers/Path__Handler__Custom.py) | 10 | `def generate_path(self, file_id: str, file_ext: str, is_metadata: bool = True) -> Safe_Str__File__Path:` |
| [memory_fs/path_handlers/Path__Handler__Versioned.py](https://github.com/owasp-sbot/Memory-FS/blob/dev/memory_fs/path_handlers/Path__Handler__Versioned.py) | 10 | `def generate_path(self, file_id: str, file_ext: str, is_metadata: bool = True, version: int = 1) -> Safe_Str__File__Path:` |
| [memory_fs/storage_fs/Storage_FS.py](https://github.com/owasp-sbot/Memory-FS/blob/dev/memory_fs/storage_fs/Storage_FS.py) | 14 | `def file__str    (self, path: Safe_Str__File__Path             ) -> str:` (allowed by design) |
| [memory_fs/schemas/Enum__Memory_FS__File__Content_Type.py](https://github.com/owasp-sbot/Memory-FS/blob/dev/memory_fs/schemas/Enum__Memory_FS__File__Content_Type.py) | 4-10 | enum members typed as `str` (allowed by design) |
| [memory_fs/schemas/Enum__Memory_FS__File__Exists_Strategy.py](https://github.com/owasp-sbot/Memory-FS/blob/dev/memory_fs/schemas/Enum__Memory_FS__File__Exists_Strategy.py) | 5-7 | enum members typed as `str` (allowed by design) |

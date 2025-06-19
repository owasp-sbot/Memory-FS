# Test Suite TODOs

Several tests contain TODO notes for future improvements.

- [`tests/unit/actions/test_Memory_FS__Paths.py`](https://github.com/owasp-sbot/Memory-FS/blob/dev/tests/unit/actions/test_Memory_FS__Paths.py) documents expected behaviour for path generation and lists outstanding items.
- [`tests/unit/file/actions/test_Memory_FS__File__Create.py`](https://github.com/owasp-sbot/Memory-FS/blob/dev/tests/unit/file/actions/test_Memory_FS__File__Create.py) uses `Storage_FS__Memory` by default and should revisit once the storage abstraction is finalised.
- [`tests/unit/memory/test_Memory_FS__Memory__File_System.py`](https://github.com/owasp-sbot/Memory-FS/blob/dev/tests/unit/memory/test_Memory_FS__Memory__File_System.py) still relies on early prototypes and will be refactored when the new `Memory_FS__*` classes stabilize.
- [`tests/unit/memory/test_Memory_FS__Memory__Storage.py`](https://github.com/owasp-sbot/Memory-FS/blob/dev/tests/unit/memory/test_Memory_FS__Memory__Storage.py) flags naming issues for the generated `.fs.json` files and includes a value check that needs verifying.

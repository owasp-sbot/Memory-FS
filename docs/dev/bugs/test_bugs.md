# Test Suite Bugs

Some unit tests contain BUG comments that highlight inconsistencies.

## File data tests
- `tests/unit/file/actions/test_Memory_FS__File__Data.py` shows an expected path mismatch.
- `tests/unit/file/test_Memory_FS__File.py` includes assertions commented with "Should be true/false" indicating behaviour disagreements.

## Memory file system tests
- `tests/unit/memory/test_Memory_FS__Memory__File_System.py` contains several BUG notes around the `content__size` field remaining zero after saving.

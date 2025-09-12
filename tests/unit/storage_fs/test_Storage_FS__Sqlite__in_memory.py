import tempfile
from unittest                                                                   import TestCase
from osbot_utils.type_safe.primitives.domains.files.safe_str.Safe_Str__File__Path  import Safe_Str__File__Path
from osbot_utils.utils.Files                                                    import file_exists, file_delete
from memory_fs.storage_fs.providers.Storage_FS__Sqlite                          import Storage_FS__Sqlite


class test_Storage_FS__Sqlite_in_memory(TestCase):          # Test SQLite storage with in-memory mode

    def test_in_memory_mode_basic(self):                    # Test basic in-memory operation
        storage = Storage_FS__Sqlite(in_memory=True).setup()

        with storage.database as _:
            assert _.in_memory           is True
            assert _.db_path             == ''
            assert _.connection_string() == ':memory:'

        test_path = Safe_Str__File__Path("test.txt")
        test_data = b"test content"

        # Basic operations should work
        assert storage.file__save(test_path, test_data) is True
        assert storage.file__exists(test_path) is True
        assert storage.file__bytes(test_path) == test_data

        # No physical file should exist
        assert storage.db_path == ""

        storage.database.close()

    def test_in_memory_persistence(self):                   # Test that in-memory database doesn't persist after close
        test_path = Safe_Str__File__Path("test.txt")
        test_data = b"test content"

        # Create and populate in-memory storage
        storage1 = Storage_FS__Sqlite(in_memory=True).setup()
        storage1.file__save(test_path, test_data)
        assert storage1.file__exists(test_path) is True
        storage1.database.close()

        # Create new in-memory storage - should be empty
        storage2 = Storage_FS__Sqlite(in_memory=True).setup()
        assert storage2.file__exists(test_path) is False
        assert storage2.files__paths() == []
        storage2.database.close()

    def test_in_memory_vs_disk_performance(self):               # Test performance difference between in-memory and disk
        import time

        temp_dir = tempfile.mkdtemp()
        db_path = f"{temp_dir}/test.db"

        # Test with disk-based storage
        disk_storage = Storage_FS__Sqlite(db_path=db_path, in_memory=False).setup()

        start_time = time.time()
        for i in range(100):
            path = Safe_Str__File__Path(f"file_{i}.txt")
            disk_storage.file__save(path, f"content_{i}".encode())
        disk_time = time.time() - start_time

        disk_storage.clear()
        disk_storage.database.close()

        # Test with in-memory storage
        mem_storage = Storage_FS__Sqlite(in_memory=True).setup()

        start_time = time.time()
        for i in range(100):
            path = Safe_Str__File__Path(f"file_{i}.txt")
            mem_storage.file__save(path, f"content_{i}".encode())
        mem_time = time.time() - start_time

        mem_storage.database.close()

        # In-memory should generally be faster
        print(f"Disk time: {disk_time:.4f}s, Memory time: {mem_time:.4f}s")
        # Note: Not asserting timing as it can vary by system

        # Clean up
        file_delete(db_path)

    def test_in_memory_large_data(self):            # Test in-memory storage with large data
        storage = Storage_FS__Sqlite(in_memory=True).setup()

        # Store 10MB of data across multiple files
        for i in range(10):
            path = Safe_Str__File__Path(f"large_{i}.bin")
            data = bytes(1024 * 1024)  # 1MB per file
            assert storage.file__save(path, data) is True
            assert storage.file__bytes(path) == data

        assert len(storage.files__paths()) == 10

        # Clear should free memory
        assert storage.clear() is True
        assert len(storage.files__paths()) == 0

        storage.database.close()

    def test_in_memory_concurrent_access(self):     # Test concurrent operations on in-memory database
        storage = Storage_FS__Sqlite(in_memory=True).setup()

        # Rapid successive operations
        paths = []
        for i in range(50):
            path = Safe_Str__File__Path(f"concurrent_{i}.txt")
            paths.append(path)
            storage.file__save(path, f"data_{i}".encode())

        # Verify all files exist
        for path in paths:
            assert storage.file__exists(path) is True

        # Delete every other file
        for i in range(0, 50, 2):
            assert storage.file__delete(paths[i]) is True

        # Verify correct files remain
        remaining = storage.files__paths()
        assert len(remaining) == 25

        storage.database.close()

    def test_in_memory_with_physical_path(self):            # Test that in_memory flag overrides physical path
        temp_dir = tempfile.mkdtemp()
        db_path = f"{temp_dir}/should_not_exist.db"

        # Create storage with physical path but in_memory=True
        storage = Storage_FS__Sqlite(db_path=db_path, in_memory=True).setup()

        test_path = Safe_Str__File__Path("test.txt")
        storage.file__save(test_path, b"content")

        # Physical file should not be created when in_memory=True
        assert file_exists(db_path) is False

        # But storage should work
        assert storage.file__exists(test_path) is True

        storage.database.close()

    def test_in_memory_table_operations(self):          # Test table operations work correctly in memory
        storage = Storage_FS__Sqlite(in_memory=True).setup()

        # Test table creation and schema
        assert storage.table.exists() is True
        schema = storage.table.schema__by_name_type()
        assert 'path' in schema
        assert 'data' in schema

        # Test indexes
        indexes = storage.table.indexes()
        assert f'idx__{storage.table_name}__path' in indexes

        # Test vacuum/optimize
        for i in range(10):
            path = Safe_Str__File__Path(f"file_{i}.txt")
            storage.file__save(path, b"content")

        for i in range(0, 10, 2):
            storage.file__delete(Safe_Str__File__Path(f"file_{i}.txt"))

        assert storage.optimize() is True  # Should work in memory

        storage.database.close()

    def test_switching_between_modes(self):     # Test switching between in-memory and disk modes
        temp_dir = tempfile.mkdtemp()
        db_path = f"{temp_dir}/test.db"
        test_path = Safe_Str__File__Path("persistent.txt")
        test_data = b"persistent content"

        # First, create disk-based storage
        disk_storage = Storage_FS__Sqlite(db_path=db_path, in_memory=False).setup()
        disk_storage.file__save(test_path, test_data)
        assert file_exists(db_path) is True
        disk_storage.database.close()

        # Now create in-memory storage (ignoring the disk file)
        mem_storage = Storage_FS__Sqlite(in_memory=True).setup()
        assert mem_storage.file__exists(test_path) is False  # Should not see disk data

        # Add different data to memory
        mem_path = Safe_Str__File__Path("memory_only.txt")
        mem_storage.file__save(mem_path, b"memory content")
        mem_storage.database.close()

        # Reopen disk storage - should still have original data only
        disk_storage2 = Storage_FS__Sqlite(db_path=db_path, in_memory=False).setup()
        assert disk_storage2.file__exists(test_path) is True
        assert disk_storage2.file__bytes(test_path) == test_data
        assert disk_storage2.file__exists(mem_path) is False  # Memory data not persisted
        disk_storage2.database.close()

        # Clean up
        file_delete(db_path)
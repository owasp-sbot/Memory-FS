import tempfile
from unittest                                                                   import TestCase
from osbot_utils.type_safe.primitives.safe_str.filesystem.Safe_Str__File__Path  import Safe_Str__File__Path
from osbot_utils.utils.Files                                                    import file_exists, file_delete, folder_delete_all, file_size
from osbot_utils.utils.Json                                                     import json_to_bytes
from memory_fs.storage_fs.providers.Storage_FS__Zip                             import Storage_FS__Zip


class test_Storage_FS__Zip__in_disk(TestCase):                                              # Test Storage_FS__Zip with disk persistence features

    def setUp(self):                                                                    # Initialize test data
        self.temp_dir     = tempfile.mkdtemp()
        self.zip_path     = Safe_Str__File__Path(f"{self.temp_dir}/test.zip")
        self.test_path    = Safe_Str__File__Path("test/file.txt")
        self.test_content = b"test content"
        self.test_json    = {"key": "value", "number": 42}

    def tearDown(self):                                                                 # Clean up temp directory
        folder_delete_all(self.temp_dir)


    # Core disk persistence tests

    def test_in_memory_only_mode(self):                                                 # Test pure in-memory mode (default behavior)
        storage = Storage_FS__Zip().setup()

        assert storage.is_in_memory_only()          is True
        assert storage.zip_path                     is None
        assert storage.file__save(self.test_path, self.test_content) is True           # Should work normally
        assert storage.file__bytes(self.test_path)  == self.test_content
        assert storage.save_to_disk()               is False                           # Save to disk should fail without path

    def test_disk_mode_initialization(self):                                            # Test initialization with disk path
        storage = Storage_FS__Zip(zip_path=self.zip_path).setup()

        assert storage.is_in_memory_only()          is False
        assert storage.zip_path                     == self.zip_path
        assert file_exists(str(self.zip_path))      is False                           # File shouldn't exist yet

        storage.file__save(self.test_path, self.test_content)                          # Add content and save
        assert storage.save_to_disk()               is True
        assert file_exists(str(self.zip_path))      is True                            # Now file should exist


    # Auto-save functionality tests (using in_memory flag)

    def test_in_memory_true_by_default(self):                                           # Test that in_memory is True by default (no auto-save)
        storage = Storage_FS__Zip(zip_path=self.zip_path, in_memory=True).setup()

        storage.file__save(self.test_path, self.test_content)                          # Add content
        assert file_exists(str(self.zip_path))      is False                           # File should not be created automatically

        assert storage.save_to_disk()               is True                            # Manually save
        assert file_exists(str(self.zip_path))      is True

    def test_in_memory_false_auto_saves(self):                                          # Test auto-save when in_memory=False
        storage = Storage_FS__Zip(zip_path=self.zip_path, in_memory=False).setup()

        storage.file__save(self.test_path, self.test_content)                          # File operations should auto-save
        assert file_exists(str(self.zip_path))      is True

        initial_size = file_size(str(self.zip_path))                                   # Check file size

        storage.file__save(Safe_Str__File__Path("another.txt"), b"more content")       # Add another file - should auto-save
        new_size = file_size(str(self.zip_path))
        assert new_size > initial_size

        storage.file__delete(self.test_path)                                           # Delete should also auto-save
        assert file_exists(str(self.zip_path))      is True

    def test_enable_disable_in_memory(self):                                            # Test enabling and disabling in_memory mode
        storage = Storage_FS__Zip(zip_path=self.zip_path).setup()

        assert storage.in_memory                    is True                            # Default is True

        storage.disable_in_memory()                                                    # Disable in_memory (enable auto-save)
        assert storage.in_memory                    is False

        storage.file__save(self.test_path, self.test_content)
        assert file_exists(str(self.zip_path))      is True

        storage.enable_in_memory()                                                     # Enable in_memory (disable auto-save)
        assert storage.in_memory                    is True

        initial_size = file_size(str(self.zip_path))                                   # New changes shouldn't auto-save
        storage.file__save(Safe_Str__File__Path("new.txt"), b"new content")
        assert file_size(str(self.zip_path))        == initial_size                    # Size unchanged

    def test_clear_with_auto_save(self):                                                # Test that clear triggers auto-save when in_memory=False
        storage = Storage_FS__Zip(zip_path=self.zip_path, in_memory=False).setup()

        storage.file__save(self.test_path, self.test_content)                          # Add content
        assert file_exists(str(self.zip_path))      is True
        initial_size = file_size(str(self.zip_path))
        assert initial_size == 138
        storage.clear()                                                                 # Clear should auto-save empty state
        assert file_exists(str(self.zip_path))      is True
        new_size = file_size(str(self.zip_path))
        assert new_size == 0                                                           # Empty zip_bytes is b""


    # Load and save operations

    def test_load_from_disk(self):                                                      # Test loading existing zip from disk
        storage1 = Storage_FS__Zip(zip_path=self.zip_path).setup()                     # Create initial storage and save
        storage1.file__save(self.test_path, self.test_content)
        storage1.file__save(Safe_Str__File__Path("file2.txt"), b"content2")
        assert storage1.save_to_disk()              is True

        storage2 = Storage_FS__Zip().setup()                                           # Create new storage and load from disk
        assert storage2.file_count()                == 0
        assert storage2.load_from_disk(self.zip_path) is True

        assert storage2.file_count()                == 2                               # Should have loaded the content
        assert storage2.file__bytes(self.test_path) == self.test_content
        assert storage2.file__bytes(Safe_Str__File__Path("file2.txt")) == b"content2"
        assert storage2.zip_path                    == self.zip_path                   # zip_path should be updated

    def test_auto_load_on_init(self):                                                   # Test auto-loading from disk on initialization
        storage1 = Storage_FS__Zip(zip_path=self.zip_path).setup()                     # Create and save initial data
        storage1.file__save(self.test_path, self.test_content)
        storage1.save_to_disk()

        storage2 = Storage_FS__Zip(zip_path=self.zip_path).setup()                     # New storage with same path should auto-load
        assert storage2.file_count()                == 1
        assert storage2.file__bytes(self.test_path) == self.test_content

    def test_save_to_different_path(self):                                              # Test saving to a different path
        storage = Storage_FS__Zip(zip_path=self.zip_path).setup()
        storage.file__save(self.test_path, self.test_content)

        assert storage.save_to_disk()               is True                            # Save to original path
        assert file_exists(str(self.zip_path))      is True

        alt_path = Safe_Str__File__Path(f"{self.temp_dir}/alternate.zip")              # Save to different path
        assert storage.save_to_disk(alt_path)       is True
        assert file_exists(str(alt_path))           is True
        assert storage.zip_path                     == self.zip_path                   # Original path should still be set

    def test_sync_to_disk(self):                                                        # Test explicit sync to disk
        storage = Storage_FS__Zip(zip_path=self.zip_path).setup()

        storage.file__save(self.test_path, self.test_content)                          # Add initial content
        assert storage.sync_to_disk()               is True

        storage2 = Storage_FS__Zip(zip_path=self.zip_path).setup()                     # Load in another storage to verify
        assert storage2.file__bytes(self.test_path) == self.test_content


    # Delete and cleanup operations

    def test_delete_from_disk(self):                                                    # Test deleting zip file from disk
        storage = Storage_FS__Zip(zip_path=self.zip_path).setup()
        storage.file__save(self.test_path, self.test_content)
        storage.save_to_disk()

        assert file_exists(str(self.zip_path))      is True
        assert storage.delete_from_disk()           is True
        assert file_exists(str(self.zip_path))      is False
        assert storage.file__exists(self.test_path) is True                            # Storage should still work in memory
        assert storage.delete_from_disk()           is False                           # Trying to delete again should return False


    # Import with merge modes

    def test_import_bytes_merge_mode(self):                                             # Test importing with merge mode
        storage = Storage_FS__Zip().setup()                                            # Create initial storage
        storage.file__save(Safe_Str__File__Path("existing.txt"), b"existing")

        import_storage = Storage_FS__Zip().setup()                                     # Create zip to import
        import_storage.file__save(Safe_Str__File__Path("imported.txt"), b"imported")
        import_storage.file__save(Safe_Str__File__Path("existing.txt"), b"updated")
        import_bytes = import_storage.export_bytes()

        assert storage.import_bytes(import_bytes, merge=True) is True                  # Import with merge

        assert storage.file_count()                 == 2                               # Should have both files, with existing file updated
        assert storage.file__bytes(Safe_Str__File__Path("existing.txt")) == b"updated"
        assert storage.file__bytes(Safe_Str__File__Path("imported.txt")) == b"imported"

    def test_import_bytes_replace_mode(self):                                           # Test importing with replace mode (default)
        storage = Storage_FS__Zip().setup()                                            # Create initial storage
        storage.file__save(Safe_Str__File__Path("existing.txt"), b"existing")

        import_storage = Storage_FS__Zip().setup()                                     # Create zip to import
        import_storage.file__save(Safe_Str__File__Path("imported.txt"), b"imported")
        import_bytes = import_storage.export_bytes()

        assert storage.import_bytes(import_bytes, merge=False) is True                 # Import without merge (replace)

        assert storage.file_count()                 == 1                               # Should only have imported files
        assert storage.file__exists(Safe_Str__File__Path("existing.txt")) is False
        assert storage.file__bytes(Safe_Str__File__Path("imported.txt"))  == b"imported"


    # Complex persistence scenarios

    def test_persistence_across_instances(self):                                        # Test that data persists across different instances
        files = { "root.txt"                  : b"root content"                ,        # Create complex structure
                  "folder1/file1.txt"          : b"file1 content"              ,
                  "folder1/folder2/file2.txt"  : b"file2 content"              ,
                  "folder3/file3.json"         : json_to_bytes({"data": "value"})}

        storage1 = Storage_FS__Zip(zip_path=self.zip_path).setup()                     # First instance - save data
        for path, content in files.items():
            storage1.file__save(Safe_Str__File__Path(path), content)
        storage1.save_to_disk()

        storage2 = Storage_FS__Zip(zip_path=self.zip_path).setup()                     # Second instance - load and verify
        assert storage2.file_count()                == len(files)
        for path, content in files.items():
            assert storage2.file__bytes(Safe_Str__File__Path(path)) == content

        storage3 = Storage_FS__Zip(zip_path=self.zip_path).setup()                     # Third instance - modify and save
        storage3.file__delete(Safe_Str__File__Path("root.txt"))
        storage3.file__save(Safe_Str__File__Path("new.txt"), b"new content")
        storage3.save_to_disk()

        storage4 = Storage_FS__Zip(zip_path=self.zip_path).setup()                     # Fourth instance - verify modifications
        assert storage4.file__exists(Safe_Str__File__Path("root.txt"))   is False
        assert storage4.file__bytes(Safe_Str__File__Path("new.txt"))     == b"new content"
        assert storage4.file_count()                == len(files)                      # Same count (deleted one, added one)

    def test_nested_directory_creation(self):                                           # Test that parent directories are handled in zip path
        nested_zip_path = Safe_Str__File__Path(f"{self.temp_dir}/sub1/sub2/nested.zip")

        storage = Storage_FS__Zip(zip_path=nested_zip_path).setup()
        storage.file__save(self.test_path, self.test_content)

        assert storage.save_to_disk()               is True                            # Save should create parent directories
        assert file_exists(str(nested_zip_path))    is True

    def test_concurrent_disk_operations(self):                                          # Test multiple operations with disk persistence
        storage = Storage_FS__Zip(zip_path=self.zip_path, in_memory=False).setup()     # in_memory=False for auto-save

        for i in range(20):                                                            # Rapid operations that should all persist
            path = Safe_Str__File__Path(f"file_{i}.txt")
            storage.file__save(path, f"content_{i}".encode())

        for i in range(0, 20, 3):                                                      # Delete some files
            storage.file__delete(Safe_Str__File__Path(f"file_{i}.txt"))

        storage2 = Storage_FS__Zip(zip_path=self.zip_path).setup()                     # Load in new instance to verify

        for i in range(20):                                                            # Verify correct files exist
            path = Safe_Str__File__Path(f"file_{i}.txt")
            if i % 3 == 0:
                assert storage2.file__exists(path)  is False
            else:
                assert storage2.file__exists(path)  is True
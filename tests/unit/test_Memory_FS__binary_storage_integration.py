import os
from unittest                                                                   import TestCase
from osbot_utils.testing.Temp_Folder                                            import Temp_Folder
from osbot_utils.type_safe.primitives.safe_str.identifiers.Safe_Id              import Safe_Id
from osbot_utils.type_safe.primitives.safe_str.filesystem.Safe_Str__File__Path  import Safe_Str__File__Path
from osbot_utils.utils.Files                                                    import folder_delete_all
from memory_fs.Memory_FS                                                        import Memory_FS
import pytest


class test_Memory_FS__binary_storage_integration(TestCase):                            # Test binary files with different storage backends

    def setUp(self):                                                                   # Per-test setup
        self.test_binary_data = b'\x89PNG\r\n\x1a\n\x00\x00\x00\rIHDR'               # Sample PNG header
        self.test_file_id = Safe_Id("test-binary-storage")
        self.memory_fs_instances = []                                                 # Track instances for cleanup

    def tearDown(self):                                                               # Clean up all created Memory_FS instances
        for memory_fs in self.memory_fs_instances:
            if memory_fs.storage_fs:
                memory_fs.storage_fs.clear()                                          # Clear all files from storage

    def test_binary_with_memory_storage(self):                                        # Test binary files with in-memory storage
        with Memory_FS() as memory_fs:
            self.memory_fs_instances.append(memory_fs)                                # Track for cleanup
            memory_fs.set_storage__memory()
            memory_fs.add_handler__latest()

            binary_file = memory_fs.file__binary(self.test_file_id)

            # Create and verify
            binary_file.create(self.test_binary_data)
            assert binary_file.exists() is True
            assert binary_file.content() == self.test_binary_data

            # Update and verify
            new_data = b'\xFF\xD8\xFF\xE0'                                           # JPEG header
            binary_file.update(new_data)
            assert binary_file.content() == new_data

            # Delete and verify
            binary_file.delete()
            assert binary_file.exists() is False

            # Verify storage is empty after delete
            assert len(memory_fs.storage_fs.files__paths()) == 0

    def test_binary_with_local_disk_storage(self):                                    # Test binary files with local disk storage
        with Temp_Folder() as temp_folder:
            tmp_dir = temp_folder.full_path
            try:
                with Memory_FS() as memory_fs:
                    self.memory_fs_instances.append(memory_fs)                        # Track for cleanup
                    root_path = Safe_Str__File__Path(tmp_dir)
                    memory_fs.set_storage__local_disk(root_path)
                    memory_fs.add_handler__latest()

                    binary_file = memory_fs.file__binary(self.test_file_id)

                    # Create and verify
                    binary_file.create(self.test_binary_data)
                    assert binary_file.exists() is True
                    assert binary_file.content() == self.test_binary_data

                    # Files should exist on disk
                    expected_path = os.path.join(tmp_dir, "latest", f"{self.test_file_id}.bin")
                    assert os.path.exists(expected_path)

                    # Read directly from disk to verify
                    with open(expected_path, 'rb') as f:
                        disk_content = f.read()
                    assert disk_content == self.test_binary_data

                    # Clean up files
                    binary_file.delete()
                    assert binary_file.exists() is False

            finally:
                # Ensure temp folder is cleaned up
                folder_delete_all(tmp_dir)

    def test_binary_with_sqlite_storage(self):                                        # Test binary files with SQLite storage
        with Memory_FS() as memory_fs:
            self.memory_fs_instances.append(memory_fs)                                # Track for cleanup
            storage = memory_fs.set_storage__sqlite(in_memory=True)                  # Use in-memory SQLite
            memory_fs.add_handler__latest()

            binary_file = memory_fs.file__binary(self.test_file_id)

            # Create and verify
            binary_file.create(self.test_binary_data)
            assert binary_file.exists() is True
            assert binary_file.content() == self.test_binary_data

            # Large binary data
            large_data = bytes(range(256)) * 100                                     # 25.6KB
            binary_file.update(large_data)
            assert binary_file.content() == large_data
            assert len(binary_file.content()) == len(large_data)

            # Clean up
            binary_file.delete()
            assert binary_file.exists() is False

            # Verify database is clean
            assert len(storage.files__paths()) == 0

    def test_binary_with_zip_storage(self):                                          # Test binary files with ZIP storage
        with Memory_FS() as memory_fs:
            self.memory_fs_instances.append(memory_fs)                                # Track for cleanup
            storage = memory_fs.set_storage__zip(in_memory=True)                     # Use in-memory ZIP
            memory_fs.add_handler__latest()

            binary_file = memory_fs.file__binary(self.test_file_id)

            # Create and verify
            binary_file.create(self.test_binary_data)
            assert binary_file.exists() is True
            assert binary_file.content() == self.test_binary_data

            # Verify it's stored correctly in the ZIP
            files_in_zip = storage.files__paths()
            assert Safe_Str__File__Path(f"latest/{self.test_file_id}.bin") in files_in_zip

            # Export ZIP and verify binary integrity
            zip_bytes = storage.export_bytes()
            assert type(zip_bytes) is bytes
            assert len(zip_bytes) > 0

            # Clean up
            binary_file.delete()
            assert binary_file.exists() is False
            assert len(storage.files__paths()) == 0

    def test_binary_storage_switching(self):                                         # Test switching storage backends with binary files
        file_id = Safe_Id("storage-switch")
        test_data = b'\x00\xFF\x00\xFF' * 100                                       # 400 bytes pattern

        # Create in memory storage
        with Memory_FS() as memory_fs:
            self.memory_fs_instances.append(memory_fs)                               # Track for cleanup
            memory_fs.set_storage__memory()
            memory_fs.add_handler__latest()

            binary_file = memory_fs.file__binary(file_id)
            binary_file.create(test_data)

            # Get the raw bytes from memory storage
            memory_storage = memory_fs.storage_fs
            stored_bytes = memory_storage.file__bytes(Safe_Str__File__Path(f"latest/{file_id}.bin"))
            assert stored_bytes == test_data

            # Clean up first instance
            binary_file.delete()
            assert len(memory_storage.files__paths()) == 0

        # Create new Memory_FS with ZIP storage
        with Memory_FS() as memory_fs_zip:
            self.memory_fs_instances.append(memory_fs_zip)                           # Track for cleanup
            memory_fs_zip.set_storage__zip(in_memory=True)
            memory_fs_zip.add_handler__latest()

            # Manually copy the data
            zip_storage = memory_fs_zip.storage_fs
            zip_storage.file__save(Safe_Str__File__Path(f"latest/{file_id}.bin"), test_data)

            # Verify we can read it back
            binary_file_zip = memory_fs_zip.file__binary(file_id)
            retrieved = binary_file_zip.content()
            assert retrieved == test_data

            # Clean up ZIP storage
            zip_storage.clear()
            assert len(zip_storage.files__paths()) == 0

    def test_binary_concurrent_storage_types(self):                                  # Test different file types in same storage
        with Memory_FS() as memory_fs:
            self.memory_fs_instances.append(memory_fs)                                # Track for cleanup
            memory_fs.set_storage__memory()
            memory_fs.add_handler__latest()

            # Create files of different types with related IDs
            base_id = "mixed-content"
            created_files = []                                                        # Track all created files

            # Binary file
            binary_file = memory_fs.file__binary(Safe_Id(f"{base_id}-binary"))
            binary_data = b'\x89PNG\r\n\x1a\n'
            binary_file.create(binary_data)
            created_files.append(binary_file)

            # JSON file
            json_file = memory_fs.file__json(Safe_Id(f"{base_id}-json"))
            json_data = {"type": "config", "version": 1}
            json_file.create(json_data)
            created_files.append(json_file)

            # Text file
            text_file = memory_fs.file__text(Safe_Id(f"{base_id}-text"))
            text_data = "This is plain text content"
            text_file.create(text_data)
            created_files.append(text_file)

            # Verify all coexist properly
            assert binary_file.content() == binary_data
            assert json_file.content()   == json_data
            assert text_file.content()   == text_data

            # Verify they have correct extensions
            assert binary_file.paths()[0].endswith(".bin")
            assert json_file.paths()[0].endswith(".json")
            assert text_file.paths()[0].endswith(".txt")

            # Verify metadata shows correct content types
            assert binary_file.info()[Safe_Id('content_type')] == 'application/octet-stream'
            assert json_file.info()[Safe_Id('content_type')]   == 'application/json; charset=utf-8'
            assert text_file.info()[Safe_Id('content_type')]   == 'text/plain; charset=utf-8'

            # Clean up all created files
            for file_obj in created_files:
                file_obj.delete()
                assert file_obj.exists() is False

            # Verify storage is completely clean
            assert len(memory_fs.storage_fs.files__paths()) == 0

    def test_binary_error_handling(self):                                            # Test error handling for binary operations
        with Memory_FS() as memory_fs:
            self.memory_fs_instances.append(memory_fs)                                # Track for cleanup
            memory_fs.set_storage__memory()
            memory_fs.add_handler__latest()

            binary_file = memory_fs.file__binary(Safe_Id("test-errors"))

            # Reading non-existent file
            assert binary_file.exists() is False
            assert binary_file.content() == None
            assert binary_file.info() is None

            # Deleting non-existent file
            deleted = binary_file.delete()
            assert deleted == []                                                     # No files deleted

            # Create then try invalid operations
            binary_file.create(b'test data')

            try:
                # These should raise errors for type violations
                with pytest.raises(ValueError, match="Binary serialization expects bytes"):
                    binary_file.update(123)                                          # Not bytes

                with pytest.raises(ValueError, match="Binary serialization expects bytes"):
                    binary_file.update([1, 2, 3])                                   # Not bytes
            finally:
                # Clean up the created file
                binary_file.delete()
                assert binary_file.exists() is False

        # Verify all storages are clean after tearDown will be called
        for memory_fs in self.memory_fs_instances:
            if memory_fs.storage_fs:
                assert len(memory_fs.storage_fs.files__paths()) == 0
from unittest                                                                      import TestCase
from osbot_utils.type_safe.primitives.domains.cryptography.safe_str.Safe_Str__Hash  import safe_str_hash
from osbot_utils.type_safe.primitives.domains.identifiers.Safe_Id                 import Safe_Id
from memory_fs.Memory_FS                                                           import Memory_FS
from memory_fs.file_types.Memory_FS__File__Type__Binary                            import Memory_FS__File__Type__Binary
from memory_fs.schemas.Enum__Memory_FS__File__Content_Type                         import Enum__Memory_FS__File__Content_Type
from memory_fs.schemas.Enum__Memory_FS__Serialization                              import Enum__Memory_FS__Serialization


class test_Memory_FS__binary_workflow(TestCase):                                        # Test complete binary file workflow

    @classmethod
    def setUpClass(cls):                                                                # One-time setup for all tests
        cls.memory_fs = Memory_FS()
        cls.memory_fs.set_storage__memory()                                            # Use in-memory storage
        cls.memory_fs.add_handler__latest()                                            # Add latest path handler

        # Create test binary data
        cls.test_binary_data     = b'\x89PNG\r\n\x1a\n\x00\x00\x00\rIHDR'            # PNG header bytes
        cls.test_image_data      = bytes([0xFF, 0xD8, 0xFF, 0xE0])                    # JPEG header bytes
        cls.test_pdf_data        = b'%PDF-1.4'                                        # PDF header bytes
        cls.test_large_binary    = bytes(range(256)) * 10                            # 2560 bytes of test data
        cls.test_empty_binary    = b''                                                # Empty binary data

    def test_file__binary_method(self):                                                # Test file__binary() method creates correct type
        with self.memory_fs as _:
            file_id = Safe_Id("test-binary-1")
            binary_file = _.file__binary(file_id)

            assert binary_file.file_id() == file_id
            assert type(binary_file.file__config.file_type) is Memory_FS__File__Type__Binary
            assert binary_file.file__config.file_type.content_type == Enum__Memory_FS__File__Content_Type.BINARY
            assert binary_file.file__config.file_type.serialization == Enum__Memory_FS__Serialization.BINARY
            assert binary_file.file__config.file_type.file_extension == Safe_Id('bin')
            assert binary_file.file__config.file_type.encoding is None                # No encoding for binary

    def test_binary_file_create_and_read(self):                                       # Test creating and reading binary files
        with self.memory_fs as _:
            file_id = Safe_Id("test-png")
            binary_file = _.file__binary(file_id)

            # Create with PNG header data
            created_files = binary_file.create(self.test_binary_data)
            assert created_files == [f"latest/{file_id}.bin"         ,
                                    f"latest/{file_id}.bin.config"  ,
                                    f"latest/{file_id}.bin.metadata"]

            # Verify file exists
            assert binary_file.exists() is True

            # Read back the binary content
            content = binary_file.content()
            assert type(content) is bytes
            assert content == self.test_binary_data
            assert len(content) == len(self.test_binary_data)

    def test_binary_file_update(self):                                                # Test updating binary file content
        with self.memory_fs as _:
            file_id = Safe_Id("test-update-binary")
            binary_file = _.file__binary(file_id)

            # Create with initial data
            binary_file.create(self.test_image_data)
            assert binary_file.content() == self.test_image_data

            # Update with new data
            updated_files = binary_file.update(self.test_pdf_data)
            assert updated_files == [f"latest/{file_id}.bin"         ,
                                    f"latest/{file_id}.bin.metadata"]                 # Config not updated

            # Verify updated content
            assert binary_file.content() == self.test_pdf_data
            assert binary_file.content() != self.test_image_data                      # Old data replaced

    def test_binary_file_metadata(self):                                              # Test metadata for binary files
        with self.memory_fs as _:
            file_id = Safe_Id("test-metadata")
            binary_file = _.file__binary(file_id)

            # Create with known data
            binary_file.create(self.test_large_binary)

            # Check metadata
            metadata = binary_file.metadata()
            assert metadata.content__size == len(self.test_large_binary)              # 2560 bytes

            # Verify hash is calculated correctly for binary data
            expected_hash = safe_str_hash(self.test_large_binary)
            assert metadata.content__hash == expected_hash

            # Check file info
            info = binary_file.info()
            assert info[Safe_Id('size')]         == len(self.test_large_binary)
            assert info[Safe_Id('content_type')] == 'application/octet-stream'        # BINARY content type
            assert info[Safe_Id('content_hash')] == expected_hash

    def test_binary_file_delete(self):                                                # Test deleting binary files
        with self.memory_fs as _:
            file_id = Safe_Id("test-delete-binary")
            binary_file = _.file__binary(file_id)

            # Create and verify exists
            binary_file.create(self.test_binary_data)
            assert binary_file.exists() is True

            # Delete all files
            deleted_files = binary_file.delete()
            assert deleted_files == [f"latest/{file_id}.bin"         ,
                                    f"latest/{file_id}.bin.config"  ,
                                    f"latest/{file_id}.bin.metadata"]

            # Verify deleted
            assert binary_file.exists () is False
            assert binary_file.content() is None

    def test_binary_empty_data(self):                                                   # Test handling empty binary data
        with self.memory_fs as _:
            file_id = Safe_Id("test-empty")
            binary_file = _.file__binary(file_id)

            # Create with empty data
            binary_file.create(self.test_empty_binary)

            # Should handle empty bytes correctly
            assert binary_file.exists ()  is True
            assert binary_file.content()  is None

            metadata = binary_file.metadata()
            assert metadata.content__size == 0

    def test_binary_type_enforcement(self):                                           # Test that only bytes are accepted
        with self.memory_fs as _:
            file_id = Safe_Id("test-type-check")
            binary_file = _.file__binary(file_id)

            # Should accept bytes
            binary_file.create(b'valid bytes')
            assert binary_file.content() == b'valid bytes'

            # Should reject non-bytes (serializer will raise ValueError)
            import pytest
            with pytest.raises(ValueError, match="Binary serialization expects bytes"):
                binary_file.update("string not bytes")                                # Strings rejected

            with pytest.raises(ValueError, match="Binary serialization expects bytes"):
                binary_file.update(12345)                                             # Numbers rejected

            with pytest.raises(ValueError, match="Binary serialization expects bytes"):
                binary_file.update({"dict": "data"})                                  # Dicts rejected

    def test_binary_large_file(self):                                                 # Test handling larger binary files
        with self.memory_fs as _:
            file_id = Safe_Id("test-large")
            binary_file = _.file__binary(file_id)

            # Create a larger binary file (1MB)
            large_data = bytes(range(256)) * 4096                                     # 1MB of data

            binary_file.create(large_data)

            # Verify it handles large data correctly
            retrieved = binary_file.content()
            assert len(retrieved) == len(large_data)
            assert retrieved == large_data

            # Check metadata reflects correct size
            metadata = binary_file.metadata()
            assert metadata.content__size == 1048576                                  # 1MB in bytes

    def test_binary_file_paths(self):                                                 # Test binary file paths have .bin extension
        with self.memory_fs as _:
            file_id = Safe_Id("test-paths")
            binary_file = _.file__binary(file_id)

            paths = binary_file.paths()

            # Should have .bin extension for content file
            assert f"latest/{file_id}.bin"          in paths                          # Content file
            assert f"latest/{file_id}.bin.config"   in paths                          # Config file
            assert f"latest/{file_id}.bin.metadata" in paths                          # Metadata file

            # No other extensions
            assert f"latest/{file_id}.json" not in paths
            assert f"latest/{file_id}.txt"  not in paths

    def test_binary_vs_other_file_types(self):                                       # Test binary files are distinct from json/text
        with self.memory_fs as _:
            file_id = Safe_Id("test-compare")

            # Create three different file types with same ID
            json_file   = _.file__json(file_id)
            text_file   = _.file__text(file_id)
            binary_file = _.file__binary(file_id)

            # They should have different extensions
            assert json_file.paths()[0]   == f"latest/{file_id}.json"
            assert text_file.paths()[0]   == f"latest/{file_id}.txt"
            assert binary_file.paths()[0] == f"latest/{file_id}.bin"

            # And different content types
            json_file.create({"key": "value"})
            text_file.create("plain text")
            binary_file.create(b'binary data')

            assert json_file.info()[Safe_Id('content_type')]   == 'application/json; charset=utf-8'
            assert text_file.info()[Safe_Id('content_type')]   == 'text/plain; charset=utf-8'
            assert binary_file.info()[Safe_Id('content_type')] == 'application/octet-stream'

    def test_binary_file_with_multiple_handlers(self):                                # Test binary files with multiple path handlers
        with Memory_FS() as memory_fs:
            memory_fs.set_storage__memory()
            memory_fs.add_handler__latest()
            memory_fs.add_handler__versioned()

            file_id = Safe_Id("multi-path-binary")
            binary_file = memory_fs.file__binary(file_id)

            # Create binary file
            created_files = binary_file.create(self.test_binary_data)

            # Should create in both latest and versioned paths
            assert f"latest/{file_id}.bin" in created_files
            assert f"v1/{file_id}.bin"     in created_files
            assert len(created_files) == 6                                            # 3 files x 2 handlers

            # Content should be accessible from either path
            assert binary_file.content() == self.test_binary_data

    def test_binary_roundtrip_integrity(self):                                        # Test binary data integrity through create/read cycle
        with self.memory_fs as _:
            file_id = Safe_Id("test-integrity")
            binary_file = _.file__binary(file_id)

            # Test various binary patterns
            test_cases = [
                (b'\x00' * 100        , "null bytes"       ),
                (b'\xFF' * 100        , "max bytes"        ),
                (bytes(range(256))    , "all byte values"  ),
                (b'\x00\xFF' * 50     , "alternating bytes"),
                (b'Mixed\x00\xFF\x7Fdata', "mixed ascii and binary")
            ]

            for test_data, description in test_cases:
                with self.subTest(description):
                    # Create new file for each test
                    test_file = _.file__binary(Safe_Id(f"integrity-{description.replace(' ', '-')}"))
                    test_file.create(test_data)

                    # Read back and verify exact match
                    retrieved = test_file.content()
                    assert retrieved == test_data
                    assert len(retrieved) == len(test_data)
                    assert type(retrieved) is bytes

                    # Verify hash integrity
                    expected_hash = safe_str_hash(test_data)
                    metadata = test_file.metadata()
                    assert metadata.content__hash == expected_hash
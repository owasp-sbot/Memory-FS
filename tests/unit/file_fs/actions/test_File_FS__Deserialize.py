import base64
import json
from unittest                                               import TestCase
from memory_fs.file_fs.actions.File_FS__Deserialize         import File_FS__Deserialize
from memory_fs.schemas.Enum__Memory_FS__Serialization       import Enum__Memory_FS__Serialization
from memory_fs.schemas.Enum__Memory_FS__File__Encoding      import Enum__Memory_FS__File__Encoding


# todo: review the use of these MockFileType in this test since I think there will be a better way to do using (using current File_FS_* classes)
class MockFileType:                                                                     # Mock file type for testing
    def __init__(self, serialization, encoding=Enum__Memory_FS__File__Encoding.UTF_8):
        self.serialization = serialization
        self.encoding      = encoding


class test_File_FS__Deserialize(TestCase):                                           # Test deserialization functionality

    def setUp(self):                                                                    # Initialize test data
        self.deserializer = File_FS__Deserialize()

    def test__init__(self):                                                             # Test initialization
        with self.deserializer as _:
            assert type(_) is File_FS__Deserialize

    def test_deserialize_string(self):                                                  # Test STRING deserialization
        file_type = MockFileType(Enum__Memory_FS__Serialization.STRING)

        with self.deserializer as _:
            # Test basic string
            content = b"Hello, World!"
            result = _._deserialize_data(content, file_type)
            assert result == "Hello, World!"

            # Test with different encoding
            file_type_utf16 = MockFileType(Enum__Memory_FS__Serialization.STRING    ,
                                           Enum__Memory_FS__File__Encoding.UTF_16   )
            content = "Hello".encode('utf-16')
            result = _._deserialize_data(content, file_type_utf16)
            assert result == "Hello"

    def test_deserialize_json(self):                                                    # Test JSON deserialization
        file_type = MockFileType(Enum__Memory_FS__Serialization.JSON)

        with self.deserializer as _:
            # Test dict
            data = {"key": "value", "number": 42}
            content = json.dumps(data).encode('utf-8')
            result = _._deserialize_data(content, file_type)
            assert result == data

            # Test list
            data = [1, 2, 3]
            content = json.dumps(data).encode('utf-8')
            result = _._deserialize_data(content, file_type)
            assert result == data

            # Test invalid JSON
            content = b"not valid json"
            try:
                _._deserialize_data(content, file_type)
                assert False, "Should raise json.JSONDecodeError"
            except json.JSONDecodeError:
                pass                                                                    # Expected

    def test_deserialize_binary(self):                                                  # Test BINARY deserialization
        file_type = MockFileType(Enum__Memory_FS__Serialization.BINARY)

        with self.deserializer as _:
            # Binary data should be returned as-is
            content = b"Binary \x00 data \xff"
            result = _._deserialize_data(content, file_type)
            assert result == content
            assert type(result) is bytes

    def test_deserialize_base64(self):                                                  # Test BASE64 deserialization
        file_type = MockFileType(Enum__Memory_FS__Serialization.BASE64)

        with self.deserializer as _:
            # Test valid base64
            original = b"Test data"
            content = base64.b64encode(original)
            result = _._deserialize_data(content, file_type)
            assert result == original

            # Test invalid base64
            content = b"not valid base64!"
            try:
                _._deserialize_data(content, file_type)
                assert False, "Should raise base64 error"
            except:
                pass                                                                    # Expected

    def test_deserialize_type_safe(self):                                               # Test TYPE_SAFE deserialization
        file_type = MockFileType(Enum__Memory_FS__Serialization.TYPE_SAFE)

        with self.deserializer as _:
            # Currently just returns the JSON string
            content = b'{"data": "test_value"}'
            result = _._deserialize_data(content, file_type)
            assert result == '{"data": "test_value"}'

            # TODO: This should actually deserialize to Type_Safe object
            # when the implementation is complete

    def test_deserialize_unknown(self):                                                 # Test unknown serialization method
        file_type = MockFileType("UNKNOWN")                                             # Invalid serialization

        with self.deserializer as _:
            try:
                _._deserialize_data(b"data", file_type)
                assert False, "Should raise ValueError"
            except ValueError as e:
                assert "Unknown serialization method: UNKNOWN" in str(e)

    def test_deserialize_with_different_encodings(self):                               # Test different encodings
        # UTF-8
        file_type = MockFileType(Enum__Memory_FS__Serialization.STRING              ,
                                 Enum__Memory_FS__File__Encoding.UTF_8               )
        content = "Hello © World".encode('utf-8')
        result = self.deserializer._deserialize_data(content, file_type)
        assert result == "Hello © World"

        # UTF-16
        file_type = MockFileType(Enum__Memory_FS__Serialization.STRING              ,
                                 Enum__Memory_FS__File__Encoding.UTF_16              )
        content = "Hello © World".encode('utf-16')
        result = self.deserializer._deserialize_data(content, file_type)
        assert result == "Hello © World"

        # Latin-1
        file_type = MockFileType(Enum__Memory_FS__Serialization.STRING              ,
                                 Enum__Memory_FS__File__Encoding.LATIN_1             )
        content = "Hello World".encode('latin-1')
        result = self.deserializer._deserialize_data(content, file_type)
        assert result == "Hello World"

    def test_roundtrip_serialization(self):                                             # Test serialize -> deserialize roundtrip
        from memory_fs.file_fs.actions.File_FS__Serialize import File_FS__Serialize
        serializer = File_FS__Serialize()

        # Test various data types and serialization methods
        test_cases = [
            ({"test": "data"}, Enum__Memory_FS__Serialization.JSON),
            ("Hello World", Enum__Memory_FS__Serialization.STRING),
            (b"Binary data", Enum__Memory_FS__Serialization.BINARY),
            ("Base64 test", Enum__Memory_FS__Serialization.BASE64),
        ]

        for original_data, serialization_method in test_cases:
            file_type = MockFileType(serialization_method)

            # Serialize
            serialized = serializer._serialize_data(original_data, file_type)

            # Deserialize
            deserialized = self.deserializer._deserialize_data(serialized, file_type)

            # Verify roundtrip
            if serialization_method == Enum__Memory_FS__Serialization.BASE64:
                # BASE64 returns bytes, so we need to decode
                assert deserialized == original_data.encode('utf-8')
            else:
                assert deserialized == original_data
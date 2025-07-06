import base64
import json
from unittest                                               import TestCase
from typing                                                 import Any

import pytest

from memory_fs.file_fs.actions.File_FS__Serializer          import File_FS__Serializer
from memory_fs.schemas.Enum__Memory_FS__Serialization       import Enum__Memory_FS__Serialization
from memory_fs.schemas.Enum__Memory_FS__File__Encoding      import Enum__Memory_FS__File__Encoding
from osbot_utils.type_safe.Type_Safe                        import Type_Safe

# todo: review the use of these MockFile* in this test since I think there will be a better way to do using (using current File_FS_* classes)

class MockFileType:                                                                     # Mock file type for testing
    def __init__(self, serialization, encoding=Enum__Memory_FS__File__Encoding.UTF_8):
        self.serialization = serialization
        self.encoding      = encoding


class MockTypeSafeObject(Type_Safe):                                                    # Mock Type_Safe object for testing
    data : Any

    def json(self):
        return f'{{"data": "{self.data}"}}'


class test_File_FS__Serializer(TestCase):                                              # Test serialization functionality

    def setUp(self):                                                                    # Initialize test data
        self.serializer = File_FS__Serializer()

    def test__init__(self):                                                             # Test initialization
        with self.serializer as _:
            assert type(_) is File_FS__Serializer

    def test_serialize_string(self):                                                    # Test STRING serialization
        file_type = MockFileType(Enum__Memory_FS__Serialization.STRING)

        with self.serializer as _:
            # Test with string input
            result = _.serialize("Hello, World!", file_type)
            assert result == b"Hello, World!"

            # Test with non-string input (should convert to string)
            result = _.serialize(12345, file_type)
            assert result == b"12345"

            # Test with different encoding
            file_type_utf16 = MockFileType(Enum__Memory_FS__Serialization.STRING    ,
                                           Enum__Memory_FS__File__Encoding.UTF_16   )
            result = _.serialize("Hello", file_type_utf16)
            assert result == "Hello".encode('utf-16')

    def test_serialize_json(self):                                                      # Test JSON serialization
        file_type = MockFileType(Enum__Memory_FS__Serialization.JSON)

        with self.serializer as _:
            # Test with dict
            data = {"key": "value", "number": 42}
            result = _.serialize(data, file_type)
            expected = b'{\n  "key": "value",\n  "number": 42\n}'
            assert result == expected

            # Test with list
            data = [1, 2, 3]
            result = _.serialize(data, file_type)
            expected = b'[\n  1,\n  2,\n  3\n]'
            assert result == expected

            # Test with bytes input (should decode first)
            data = b'{"already": "json"}'
            result = _.serialize(data, file_type)
            assert result == b'"{\\"already\\": \\"json\\"}"'                                     # Should re-format the JSON

    def test_serialize_binary(self):                                                    # Test BINARY serialization
        file_type = MockFileType(Enum__Memory_FS__Serialization.BINARY)

        with self.serializer as _:
            # Test with bytes input
            data = b"Binary data"
            result = _.serialize(data, file_type)
            assert result == data

            # Test with non-bytes input (should raise error)
            try:
                _.serialize("Not bytes", file_type)
                assert False, "Should raise ValueError"
            except ValueError as e:
                assert "Binary serialization expects bytes" in str(e)

    def test_serialize_base64(self):                                                    # Test BASE64 serialization
        file_type = MockFileType(Enum__Memory_FS__Serialization.BASE64)

        with self.serializer as _:
            # Test with bytes input
            data = b"Test data"
            result = _.serialize(data, file_type)
            expected = base64.b64encode(data)
            assert result == expected

            # Test with string input
            data = "Test string"
            result = _.serialize(data, file_type)
            expected = base64.b64encode(data.encode('utf-8'))
            assert result == expected

    def test_serialize_type_safe(self):                                                 # Test TYPE_SAFE serialization
        file_type = MockFileType(Enum__Memory_FS__Serialization.TYPE_SAFE)

        with self.serializer as _:
            # Test with Type_Safe object
            obj = MockTypeSafeObject(data="test_value")
            with pytest.raises(NotImplementedError):  # todo: need to add Type_Safe support (and test round trip here)
                result = _.serialize(obj, file_type)
            # expected = b'{"data": "test_value"}'
            # assert result == expected

            # # Test with non-Type_Safe object (should raise error)
            # try:
            #     _.serialize({"not": "type_safe"}, file_type)
            #     assert False, "Should raise ValueError"
            # except ValueError as e:
            #     assert "TYPE_SAFE serialization requires object with json() method" in str(e)

    def test_serialize_unknown(self):                                                   # Test unknown serialization method
        file_type = MockFileType("UNKNOWN")                                             # Invalid serialization

        with self.serializer as _:
            try:
                _.serialize("data", file_type)
                assert False, "Should raise ValueError"
            except ValueError as e:
                assert "Unknown serialization method: UNKNOWN" in str(e)

    def test_serialize_with_different_encodings(self):                                 # Test different encodings
        test_string = "Hello © World"

        # UTF-8
        file_type = MockFileType(Enum__Memory_FS__Serialization.STRING              ,
                                 Enum__Memory_FS__File__Encoding.UTF_8               )
        result = self.serializer.serialize(test_string, file_type)
        assert result == test_string.encode('utf-8')

        # ASCII (should fail with copyright symbol)
        file_type = MockFileType(Enum__Memory_FS__Serialization.STRING              ,
                                 Enum__Memory_FS__File__Encoding.ASCII               )
        try:
            self.serializer.serialize(test_string, file_type)
            assert False, "Should raise encoding error"
        except UnicodeEncodeError:
            pass                                                                        # Expected
        
        
    # ##### Deserialisation tests
    
    def test_deserialize_string(self):                                                  # Test STRING deserialization
        file_type = MockFileType(Enum__Memory_FS__Serialization.STRING)

        with self.serializer as _:
            # Test basic string
            content = b"Hello, World!"
            result = _.deserialize(content, file_type)
            assert result == "Hello, World!"

            # Test with different encoding
            file_type_utf16 = MockFileType(Enum__Memory_FS__Serialization.STRING    ,
                                           Enum__Memory_FS__File__Encoding.UTF_16   )
            content = "Hello".encode('utf-16')
            result = _.deserialize(content, file_type_utf16)
            assert result == "Hello"

    def test_deserialize_json(self):                                                    # Test JSON deserialization
        file_type = MockFileType(Enum__Memory_FS__Serialization.JSON)

        with self.serializer as _:
            # Test dict
            data = {"key": "value", "number": 42}
            content = json.dumps(data).encode('utf-8')
            result = _.deserialize(content, file_type)
            assert result == data

            # Test list
            data = [1, 2, 3]
            content = json.dumps(data).encode('utf-8')
            result = _.deserialize(content, file_type)
            assert result == data

            # Test invalid JSON
            content = b"not valid json"
            try:
                _.deserialize(content, file_type)
                assert False, "Should raise json.JSONDecodeError"
            except json.JSONDecodeError:
                pass                                                                    # Expected

    def test_deserialize_binary(self):                                                  # Test BINARY deserialization
        file_type = MockFileType(Enum__Memory_FS__Serialization.BINARY)

        with self.serializer as _:
            # Binary data should be returned as-is
            content = b"Binary \x00 data \xff"
            result = _.deserialize(content, file_type)
            assert result == content
            assert type(result) is bytes

    def test_deserialize_base64(self):                                                  # Test BASE64 deserialization
        file_type = MockFileType(Enum__Memory_FS__Serialization.BASE64)

        with self.serializer as _:
            # Test valid base64
            original = b"Test data"
            content = base64.b64encode(original)
            result = _.deserialize(content, file_type)
            assert result == original

            # Test invalid base64
            content = b"not valid base64!"
            try:
                _.deserialize(content, file_type)
                assert False, "Should raise base64 error"
            except:
                pass                                                                    # Expected

    def test_deserialize_type_safe(self):                                               # Test TYPE_SAFE deserialization
        file_type = MockFileType(Enum__Memory_FS__Serialization.TYPE_SAFE)

        with self.serializer as _:
            # Currently just returns the JSON string
            content = b'{"data": "test_value"}'
            with pytest.raises(NotImplementedError):                                    # todo: need to add Type_Safe support (and test round trip here)
                result = _.deserialize(content, file_type)
            #assert result == '{"data": "test_value"}'


    def test_deserialize_unknown(self):                                                 # Test unknown serialization method
        file_type = MockFileType("UNKNOWN")                                             # Invalid serialization

        with self.serializer as _:
            try:
                _.deserialize(b"data", file_type)
                assert False, "Should raise ValueError"
            except ValueError as e:
                assert "Unknown serialization method: UNKNOWN" in str(e)

    def test_deserialize_with_different_encodings(self):                               # Test different encodings
        # UTF-8
        file_type = MockFileType(Enum__Memory_FS__Serialization.STRING              ,
                                 Enum__Memory_FS__File__Encoding.UTF_8               )
        content = "Hello © World".encode('utf-8')
        result = self.serializer.deserialize(content, file_type)
        assert result == "Hello © World"

        # UTF-16
        file_type = MockFileType(Enum__Memory_FS__Serialization.STRING              ,
                                 Enum__Memory_FS__File__Encoding.UTF_16              )
        content = "Hello © World".encode('utf-16')
        result = self.serializer.deserialize(content, file_type)
        assert result == "Hello © World"

        # Latin-1
        file_type = MockFileType(Enum__Memory_FS__Serialization.STRING              ,
                                 Enum__Memory_FS__File__Encoding.LATIN_1             )
        content = "Hello World".encode('latin-1')
        result = self.serializer.deserialize(content, file_type)
        assert result == "Hello World"

    def test_roundtrip_serialization(self):                                             # Test serialize -> deserialize roundtrip        
        serializer = File_FS__Serializer()

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
            serialized = serializer.serialize(original_data, file_type)

            # Deserialize
            deserialized = self.serializer.deserialize(serialized, file_type)

            # Verify roundtrip
            if serialization_method == Enum__Memory_FS__Serialization.BASE64:
                # BASE64 returns bytes, so we need to decode
                assert deserialized == original_data.encode('utf-8')
            else:
                assert deserialized == original_data
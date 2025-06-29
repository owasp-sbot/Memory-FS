import base64
from unittest                                               import TestCase
from typing                                                 import Any
from memory_fs.file_fs.actions.File_FS__Serialize           import File_FS__Serialize
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


class test_File_FS__Serialize(TestCase):                                              # Test serialization functionality

    def setUp(self):                                                                    # Initialize test data
        self.serializer = File_FS__Serialize()

    def test__init__(self):                                                             # Test initialization
        with self.serializer as _:
            assert type(_) is File_FS__Serialize

    def test_serialize_string(self):                                                    # Test STRING serialization
        file_type = MockFileType(Enum__Memory_FS__Serialization.STRING)

        with self.serializer as _:
            # Test with string input
            result = _._serialize_data("Hello, World!", file_type)
            assert result == b"Hello, World!"

            # Test with non-string input (should convert to string)
            result = _._serialize_data(12345, file_type)
            assert result == b"12345"

            # Test with different encoding
            file_type_utf16 = MockFileType(Enum__Memory_FS__Serialization.STRING    ,
                                           Enum__Memory_FS__File__Encoding.UTF_16   )
            result = _._serialize_data("Hello", file_type_utf16)
            assert result == "Hello".encode('utf-16')

    def test_serialize_json(self):                                                      # Test JSON serialization
        file_type = MockFileType(Enum__Memory_FS__Serialization.JSON)

        with self.serializer as _:
            # Test with dict
            data = {"key": "value", "number": 42}
            result = _._serialize_data(data, file_type)
            expected = b'{\n  "key": "value",\n  "number": 42\n}'
            assert result == expected

            # Test with list
            data = [1, 2, 3]
            result = _._serialize_data(data, file_type)
            expected = b'[\n  1,\n  2,\n  3\n]'
            assert result == expected

            # Test with bytes input (should decode first)
            data = b'{"already": "json"}'
            result = _._serialize_data(data, file_type)
            assert result == b'"{\\"already\\": \\"json\\"}"'                                     # Should re-format the JSON

    def test_serialize_binary(self):                                                    # Test BINARY serialization
        file_type = MockFileType(Enum__Memory_FS__Serialization.BINARY)

        with self.serializer as _:
            # Test with bytes input
            data = b"Binary data"
            result = _._serialize_data(data, file_type)
            assert result == data

            # Test with non-bytes input (should raise error)
            try:
                _._serialize_data("Not bytes", file_type)
                assert False, "Should raise ValueError"
            except ValueError as e:
                assert "Binary serialization expects bytes" in str(e)

    def test_serialize_base64(self):                                                    # Test BASE64 serialization
        file_type = MockFileType(Enum__Memory_FS__Serialization.BASE64)

        with self.serializer as _:
            # Test with bytes input
            data = b"Test data"
            result = _._serialize_data(data, file_type)
            expected = base64.b64encode(data)
            assert result == expected

            # Test with string input
            data = "Test string"
            result = _._serialize_data(data, file_type)
            expected = base64.b64encode(data.encode('utf-8'))
            assert result == expected

    def test_serialize_type_safe(self):                                                 # Test TYPE_SAFE serialization
        file_type = MockFileType(Enum__Memory_FS__Serialization.TYPE_SAFE)

        with self.serializer as _:
            # Test with Type_Safe object
            obj = MockTypeSafeObject(data="test_value")
            result = _._serialize_data(obj, file_type)
            expected = b'{"data": "test_value"}'
            assert result == expected

            # Test with non-Type_Safe object (should raise error)
            try:
                _._serialize_data({"not": "type_safe"}, file_type)
                assert False, "Should raise ValueError"
            except ValueError as e:
                assert "TYPE_SAFE serialization requires object with json() method" in str(e)

    def test_serialize_unknown(self):                                                   # Test unknown serialization method
        file_type = MockFileType("UNKNOWN")                                             # Invalid serialization

        with self.serializer as _:
            try:
                _._serialize_data("data", file_type)
                assert False, "Should raise ValueError"
            except ValueError as e:
                assert "Unknown serialization method: UNKNOWN" in str(e)

    def test_serialize_with_different_encodings(self):                                 # Test different encodings
        test_string = "Hello © World"

        # UTF-8
        file_type = MockFileType(Enum__Memory_FS__Serialization.STRING              ,
                                 Enum__Memory_FS__File__Encoding.UTF_8               )
        result = self.serializer._serialize_data(test_string, file_type)
        assert result == test_string.encode('utf-8')

        # ASCII (should fail with copyright symbol)
        file_type = MockFileType(Enum__Memory_FS__Serialization.STRING              ,
                                 Enum__Memory_FS__File__Encoding.ASCII               )
        try:
            self.serializer._serialize_data(test_string, file_type)
            assert False, "Should raise encoding error"
        except UnicodeEncodeError:
            pass                                                                        # Expected
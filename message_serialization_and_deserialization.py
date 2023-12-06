def contains_new_line_characters(data):
    new_line_characters = {'\r', '\n', '\r\n'}
    return any(char in new_line_characters for char in data)

def serialize_response(data):
    if data is None:
        return b'$-1\r\n'
    elif isinstance(data, str):
        if(contains_new_line_characters(data) is False and len(data) <= 2 and data != ""):
            return f"+{data}\r\n".encode('utf-8')
        elif('error' in data.lower()):
            return f"-{data}\r\n".encode('utf-8')
        else:
            return f"${len(data)}\r\n{data}\r\n".encode('utf-8')
    elif isinstance(data, int):
        return f":{data}\r\n".encode('utf-8')
    elif isinstance(data, list):
        array_content = ''.join(serialize_response(item).decode('utf-8') for item in data)
        return f"*{len(data)}\r\n{array_content}".encode('utf-8')
    else:
        raise ValueError(f"Unsupported data type: {type(data)}")

def deserialize_response(data):
    if data.startswith(b'+'):
        simple_string, rest = data[1:].split(b'\r\n', 1)
        return simple_string.decode('utf-8'), rest
    elif data.startswith(b'-'):
        error_string, rest = data[1:].split(b'\r\n', 1)
        return error_string.decode('utf-8'), rest
    elif data.startswith(b':'):
        return int(data[1:].strip())
    elif data.startswith(b'$'):
        if data[1] == ord('-'):
            return None, None
        else:
            length, rest = data[1:].split(b'\r\n', 1)
            length = int(length)
            return rest[:length].decode('utf-8'), rest[length+ 2:]
    elif data.startswith(b'*'):
        count, rest = data[1:].split(b'\r\n', 1)
        count = int(count)
        result = []
        for _ in range(count):
            item, rest = deserialize_response(rest)
            result.append(item)
        return result, rest
    else:
        raise ValueError("Invalid RESP format")


test_cases = [
    (None, b'$-1\r\n'),
    ("ping", b"$4\r\nping\r\n"),
    (["echo", "hello world"], b"*2\r\n$4\r\necho\r\n$11\r\nhello world\r\n"),
    (["get", "key"], b"*2\r\n$3\r\nget\r\n$3\r\nkey\r\n"),
    ("OK", b"+OK\r\n"),
    ("Error message", b"-Error message\r\n"),
    ("", b"$0\r\n\r\n"),
    ("hello world", b"$11\r\nhello world\r\n")
]


for data, expected_result in test_cases:
    serialized_data = serialize_response(data)
    print(serialized_data)
    assert serialized_data == expected_result, f"Failed: {data} -> {serialized_data}"

    deserialized_data, _ = deserialize_response(expected_result)
    print(deserialized_data)
    assert deserialized_data == data, f"Failed: {expected_result} -> {deserialized_data}"

print("--------------------------------------------------\nAll tests passed!")
import pytest

from lzss import compress, decompress
from lzss.lzss import get_wrapped_slice


@pytest.mark.parametrize(
    "data, expected_compressed_bytes",
    [
        (b"a" * 5, 4),  # 9 + 17 = 26 bits, padded to 32
        (b"a" * 18, 4),
        (b"a" * 19, 5),
        (b"abc" * 100, 42),
        (b"abc" * 100 + b"random string" + b"g" * 10, 59),
    ],
)
def test_lzss(data: bytes, expected_compressed_bytes: int) -> None:
    compressed_data = compress(data)
    assert len(compressed_data) < len(data)
    assert len(compressed_data) == expected_compressed_bytes
    assert data == decompress(compressed_data)


@pytest.mark.parametrize(
    "data, slice_length, expected",
    [
        (b"1", 0, b""),
        (b"1", 1, b"1"),
        (b"1", 2, b"11"),
        (b"123", 5, b"12312"),
        (b"1234567", 5, b"12345"),
    ],
)
def test_get_wrapped_slice(data: bytes, slice_length: int, expected: bytes) -> None:
    assert expected == get_wrapped_slice(data, slice_length)

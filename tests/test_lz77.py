from pathlib import Path

import pytest

from lz77 import compress, decompress
from lz77.lz77 import get_wrapped_slice


@pytest.mark.parametrize(
    "text, expected_compressed_bytes",
    [
        ("a" * 5, 4),  # 9 + 17 = 26 bits, padded to 32
        ("a" * 16, 4),
        ("a" * 17, 5),
        ("abc" * 100, 46),
        ("abc" * 100 + "random string" + "g" * 10, 63),
    ],
)
def test_LZ77(tmp_path: Path, text: str, expected_compressed_bytes: int) -> None:
    input_filename = tmp_path / "raw.txt"
    intermediate_filename = tmp_path / "compressed.bin"
    output_filename = tmp_path / "decompressed.txt"

    open(input_filename, "w").write(text)

    compress(input_file_path=input_filename, output_file_path=intermediate_filename)

    num_compressed_bytes = len(open(intermediate_filename, "rb").read())
    assert num_compressed_bytes < len(text)
    assert num_compressed_bytes == expected_compressed_bytes

    decompress(intermediate_filename, output_file_path=output_filename)

    assert open(output_filename).read() == text


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

from pathlib import Path

import pytest

from lz77 import LZ77


def test_LZ77_init() -> None:
    LZ77()


@pytest.mark.parametrize(
    "text, expected_compressed_bytes",
    [
        ("abc" * 100, 46),
        ("abc" * 100 + "random string" + "g" * 10, 63),
    ],
)
def test_LZ77(tmp_path: Path, text: str, expected_compressed_bytes: int) -> None:
    lz77 = LZ77()

    input_filename = tmp_path / "raw.txt"
    intermediate_filename = tmp_path / "compressed.bin"
    output_filename = tmp_path / "decompressed.txt"

    open(input_filename, "w").write(text)

    lz77.compress(input_file_path=input_filename, output_file_path=intermediate_filename)

    num_compressed_bytes = len(open(intermediate_filename, "rb").read())
    assert num_compressed_bytes < len(text)
    assert num_compressed_bytes == expected_compressed_bytes

    lz77.decompress(intermediate_filename, output_file_path=output_filename)

    assert open(output_filename).read() == text

from pathlib import Path

from lz77 import LZ77


def test_LZ77_init() -> None:
    LZ77()


def test_LZ77(tmp_path: Path) -> None:
    lz77 = LZ77()
    text = "abc" * 100

    input_filename = tmp_path / "raw.txt"
    intermediate_filename = tmp_path / "compressed.bin"
    output_filename = tmp_path / "decompressed.txt"

    open(input_filename, "w").write(text)

    lz77.compress(input_file_path=input_filename, output_file_path=intermediate_filename)

    num_compressed_bytes = len(open(intermediate_filename, "rb").read())
    assert num_compressed_bytes < len(text)
    assert num_compressed_bytes == 51

    lz77.decompress(intermediate_filename, output_file_path=output_filename)

    assert open(output_filename).read() == text

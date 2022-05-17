from typing import Final, Optional, Tuple

from bitarray import bitarray


MATCH_LENGTH_MASK: Final[int] = 0xF
WINDOW_SIZE: Final[int] = 0xFFF


def compress(input_file_path, output_file_path=None, verbose=False):
    """
    Given the path of an input file, its content is compressed by applying a simple
    LZ77 compression algorithm.

    The compressed format is:
    0 bit followed by 8 bits (1 byte character) when there are no previous matches
            within window
    1 bit followed by 12 bits pointer (distance to the start of the match from the
            current position) and 4 bits (length of the match)

    If a path to the output file is provided, the compressed data is written into
    a binary file. Otherwise, it is returned as a bitarray

    if verbose is enabled, the compression description is printed to standard output
    """
    data = None
    i = 0
    output_buffer = bitarray(endian="big")

    # read the input file
    try:
        with open(input_file_path, "rb") as input_file:
            data = input_file.read()
    except IOError:
        print("Could not open input file ...")
        raise

    while i < len(data):
        match = find_longest_match(data, i)

        if match:
            # Add 1 bit flag, followed by 12 bit for distance and 4 bit for the match length
            (bestMatchDistance, bestMatchLength) = match

            output_buffer.append(True)
            output_buffer.frombytes(bytes([bestMatchDistance >> 4]))
            output_buffer.frombytes(bytes([((bestMatchDistance & 0xF) << 4) | bestMatchLength]))

            if verbose:
                print("<1, %i, %i>" % (bestMatchDistance, bestMatchLength), end="")

            i += bestMatchLength

        else:
            # No useful match was found. Add 0 bit flag, followed by 8 bit for the character
            output_buffer.append(False)
            output_buffer.frombytes(bytes([data[i]]))

            if verbose:
                print("<0, %s>" % data[i], end="")

            i += 1

    # fill the buffer with zeros if the number of bits is not a multiple of 8
    output_buffer.fill()

    # write the compressed data into a binary file if a path is provided
    if output_file_path:
        try:
            with open(output_file_path, "wb") as output_file:
                output_file.write(output_buffer.tobytes())
                print("File was compressed successfully and saved to output path ...")
                return None
        except IOError:
            print("Could not write to output file path. Please check if the path is correct ...")
            raise

    # an output file path was not provided, return the compressed data
    return output_buffer


def decompress(input_file_path, output_file_path=None):
    """
    Given a string of the compressed file path, the data is decompressed back to its
    original form, and written into the output file path if provided. If no output
    file path is provided, the decompressed data is returned as a string
    """
    data = bitarray(endian="big")
    output_buffer = []

    # read the input file
    try:
        with open(input_file_path, "rb") as input_file:
            data.fromfile(input_file)
    except IOError:
        print("Could not open input file ...")
        raise

    while len(data) >= 9:

        flag = data.pop(0)

        if not flag:
            byte = data[0:8].tobytes()

            output_buffer.append(byte)
            del data[0:8]
        else:
            byte1 = ord(data[0:8].tobytes())
            byte2 = ord(data[8:16].tobytes())

            del data[0:16]
            distance = (byte1 << 4) | (byte2 >> 4)
            length = byte2 & 0xF

            for i in range(length):
                output_buffer.append(output_buffer[-distance])
    out_data = b"".join(output_buffer)

    if output_file_path:
        try:
            with open(output_file_path, "wb") as output_file:
                output_file.write(out_data)
                print("File was decompressed successfully and saved to output path ...")
                return None
        except IOError:
            print("Could not write to output file path. Please check if the path is correct ...")
            raise
    return out_data


def find_longest_match(data: bytes, current_position: int) -> Optional[Tuple[int, int]]:
    """
    Finds the longest match to a substring starting at the current_position
    in the lookahead buffer from the history window
    """
    end_of_buffer = min(current_position + MATCH_LENGTH_MASK, len(data))
    start_index = max(0, current_position - WINDOW_SIZE)

    # Optimization: Only consider substrings of length 2 and greater, and just
    # output any substring of length 1 (8 bits uncompressed is better than 13 bits
    # for the flag, distance, and length)
    for j in range(end_of_buffer, current_position + 3, -1):
        substring = data[current_position:j]
        for i in range(start_index, current_position):
            if substring == get_wrapped_slice(data[i:current_position], len(substring)):
                return current_position - i, len(substring)


def get_wrapped_slice(x: bytes, num_bytes: int) -> bytes:
    """
    Examples:
        f(b"1234567", 5) -> b"12345"
        f(b"123", 5) -> b"12312"
    """
    repetitions = num_bytes // len(x)
    remainder = num_bytes % len(x)
    return x * repetitions + x[:remainder]

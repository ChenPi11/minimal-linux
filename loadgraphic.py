#!/usr/bin/env python3

"""Load Data Graphic"""

# Format:
# 1: X ((0, 0, 0) or (255, 255, 255))  ---- File head. (0, 0, 0) for 2-colors
#   graphic, (255, 255, 255) for 256-colors graphic.
# 2: GREET_MSG                         ---- Greet message. Ends with \x00.
# 3: FILE_NAME                         ---- File name. Ends with \x00.
# 4: FILE_PERM                         ---- File permission. (6 bytes)
# 5: FILE_SIZE                         ---- File size in little-endian format.
# (6 bytes)
# 6: FILE_DATA                         ---- Raw file data.

import io
from pathlib import Path
import time
import sys
import locale
import PIL.Image

CHARSET = "UTF-8"


def uint6_to_int(data: bytes) -> int:
    """Converts a 6-byte little-endian representation to an integer.

    Args:
        data (bytes): Little-endian input data.

    Returns:
        int: Output data.
    """

    return int.from_bytes(data, byteorder="little")


def read_until_null(fp: io.BytesIO, output: bool = False) -> str:
    """Read data from the buffer until a null byte is found.

    Args:
        fp (io.BytesIO): Input data buffer.
        output (bool): Output read bytes. Defaults to False.

    Returns:
        str: Output data.
    """

    result = b""
    while (byte := fp.read(1)) != b"\x00":
        result += byte
        if len(byte) == 0:
            raise ValueError("Null byte not found.")
        if output:
            print(byte.decode(CHARSET), end="", flush=True)
            time.sleep(0.005)
    return result.decode(CHARSET)


def load_raw_io_2colors(filepath: Path) -> io.BytesIO:
    """Return a IO buffer that contains file data by 2-colors graphic.

    Args:
        filepath (Path): The graphic file path.

    Returns:
        io.BytesIO: A IO buffer that contains all data. Include file name,
            greet message and so on.
    """

    img = PIL.Image.open(filepath)
    raw_data: list[int] = []
    img_width, img_height = img.size
    byte = ""
    bit_pos = 0
    cur_x_pos = 1  # Skip file header.
    cur_y_pos = 0

    while cur_y_pos < img_height:
        pixel = img.getpixel((cur_x_pos, cur_y_pos))
        if not isinstance(pixel, tuple):
            raise ValueError("Image is not in RGB mode.")
        if pixel == (0, 0, 0):
            byte += "1"
        else:
            byte += "0"
        bit_pos += 1
        if bit_pos == 8:
            raw_data.append(int(byte, 2))
            byte = ""
            bit_pos = 0
        cur_x_pos += 1
        if cur_x_pos == img_width:
            cur_x_pos = 0
            cur_y_pos += 1

    return io.BytesIO(bytes(raw_data))


def load_raw_io_256colors(filepath: Path) -> io.BytesIO:
    """Return a IO buffer that contains file data by 256-colors graphic.

    Args:
        filepath (Path): The graphic file path.

    Returns:
        io.BytesIO: A IO buffer that contains all data. Include file name,
            greet message and so on.
    """

    img = PIL.Image.open(filepath)
    raw_data: list[int] = []
    img_width, img_height = img.size
    cur_x_pos = 1  # Skip file header.
    cur_y_pos = 0

    while cur_y_pos < img_height:
        pixel = img.getpixel((cur_x_pos, cur_y_pos))
        if not isinstance(pixel, tuple):
            raise ValueError("Image is not in RGB mode.")
        raw_data.extend(pixel)
        cur_x_pos += 1
        if cur_x_pos == img_width:
            cur_x_pos = 0
            cur_y_pos += 1

    return io.BytesIO(bytes(raw_data))


def is_256colors_graphic(imgpath: Path) -> bool:
    """Check if the graphic file is 256-colors.

    Args:
        imgpath (Path): The graphic file path.

    Returns:
        bool: True if the graphic file is 256-colors.
    """

    with PIL.Image.open(imgpath) as img:
        pixel = img.getpixel((0, 0))
        if not isinstance(pixel, tuple):
            raise ValueError("Image is not in RGB mode.")
        return pixel == (255, 255, 255)


def unpack_graphic(imgpath: Path) -> None:
    """Unpack the graphic file.

    Args:
        imgpath (Path): The graphic file path.
    """

    raw_io: io.BytesIO
    if is_256colors_graphic(imgpath):
        print("Loading the graphic file as 256-colors ...")
        raw_io = load_raw_io_256colors(imgpath)
    else:
        print("Loading the graphic file as 2-colors ...")
        raw_io = load_raw_io_2colors(imgpath)
    print("=" * 20, flush=True)
    read_until_null(raw_io, True)
    print("\n" + "=" * 20, flush=True)
    print("Unpacking file: ", end="", flush=True)
    file_name = Path(read_until_null(raw_io, True))
    print(flush=True)
    # Security check: file name should not be a absolute path.
    if file_name.is_absolute():
        raise ValueError("File name is absolute path. This is not allowed.")
    perm_data = raw_io.read(6)
    file_perm = uint6_to_int(perm_data)
    print(f"File permission: {file_perm:o}")
    size_data = raw_io.read(6)
    file_size = uint6_to_int(size_data)
    print(f"File size: {file_size} bytes.")
    with file_name.open("wb") as fp:
        fp.write(raw_io.read(file_size))
    file_name.chmod(file_perm)
    print("File unpacked.")


if __name__ == "__main__":
    # Set locale to the user's default setting.
    locale.setlocale(locale.LC_ALL, locale.setlocale(locale.LC_ALL, ""))
    if len(sys.argv) != 2:
        print(f"Usage: {sys.argv[0]} <graphic file>")
        sys.exit(1)
    unpack_graphic(Path(sys.argv[1]))

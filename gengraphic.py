#!/usr/bin/env python3

"""Generate Data Graphic"""

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
import math
import sys
import locale
import PIL.Image

COMPRESSED_IMG_FILE = "disk.img.xz"

GREET_MSG_2COLORS = """This is a 2-colors graphic.
You should read it from top to bottom, left to right.
The black pixel is 0, and the white pixel is 1.
The first data is the greet message, followed by a null byte.
Then, the file name is added, followed by a null byte.
Then, the file permission is added in little-endian format. (6 bytes)
After that, the file size is added in little-endian format. (6 bytes)
Finally, the file data is added."""

GREET_MSG_256COLORS = """This is a 256-colors graphic.
You should read it from top to bottom, left to right.
A pixel is represented by 3 bytes. (R=byte0, G=byte1, B=byte2)
The next 3 bytes represent the RGB color of the second pixel, and so on.
If the file size is not a multiple of 3, the last pixel will be padded
with zeros.
The first data is the greet message, followed by a null byte.
Then, the file name is added, followed by a null byte.
Then, the file permission is added in little-endian format. (6 bytes)
After that, the file size is added in little-endian format. (6 bytes)
Finally, the file data is added."""

CHARSET = "UTF-8"


def convert_to_uint6(x: int) -> bytes:
    """Converts an integer to a 6-byte little-endian representation.

    Args:
        x (int): Input data.

    Returns:
        bytes: Little-endian output data.
    """

    return x.to_bytes(6, byteorder="little")


def get_data_io(
    filepath: Path,
    greet_msg: str,
) -> tuple[io.BytesIO, int]:
    """Return a IO buffer that contains greet message, size data and file data.

    Args:
        filepath (Path): File path.
        greet_msg (str): Greet message.

    Returns:
        tuple[io.BytesIO, int]: IO buffer and file size.
    """

    size_data = convert_to_uint6(filepath.stat().st_size)
    perm_data = convert_to_uint6(filepath.stat().st_mode)

    with filepath.open("rb") as fp:
        all_data = (
            greet_msg.encode(CHARSET)
            + b"\x00"
            + filepath.name.encode(CHARSET)
            + b"\x00"
            + perm_data
            + size_data
            + fp.read()
        )
        return (
            io.BytesIO(all_data),
            len(all_data),
        )


def gen_2_colors_graphic(
    fp: io.BytesIO, width: int, height: int
) -> PIL.Image.Image:  # noqa: E501
    """Generate 2 colors graphic.

    Args:
        fp (io.BytesIO): Input data buffer.
        width (int): Image width.
        height (int): Image height.

    Returns:
        PIL.Image.Image: Result image.
    """

    img = PIL.Image.new("RGB", (width, height))
    pixels = img.load()
    data = fp.read()
    data_len = len(data)

    img.putpixel((0, 0), (0, 0, 0))  # Header. Black pixel means 2-colors.

    cur_x_pos = 1
    cur_y_pos = 0

    for idx in range(data_len):
        byte = bin(data[idx])[2:].rjust(8, "0")
        for bit in byte:
            pixels[cur_x_pos, cur_y_pos] = (
                (0, 0, 0) if bit == "1" else (255, 255, 255)  # noqa: E501
            )
            cur_x_pos += 1
            if cur_x_pos == width:
                cur_x_pos = 0
                cur_y_pos += 1

    return img


def gen_256_colors_graphic(
    fp: io.BytesIO, width: int, height: int
) -> PIL.Image.Image:  # noqa: E501
    """Generate 256 colors graphic.

    Args:
        fp (io.BytesIO): Input data buffer.
        width (int): Image width.
        height (int): Image height.

    Returns:
        PIL.Image.Image: Result image.
    """

    img = PIL.Image.new("RGB", (width, height))
    pixels = img.load()

    # Header. White pixel means 256-colors.
    fp = io.BytesIO(b"\xff\xff\xff" + fp.read())

    for y in range(height):
        for x in range(width):
            pixel = tuple(fp.read(3))
            if len(pixel) == 0:
                pixel = (0, 0, 0)
            elif len(pixel) == 1:
                pixel = (pixel[0], 0, 0)
            elif len(pixel) == 2:
                pixel = (pixel[0], pixel[1], 0)
            pixels[x, y] = pixel

    return img


if __name__ == "__main__":
    # Set locale to the user's default setting.
    locale.setlocale(locale.LC_ALL, locale.setlocale(locale.LC_ALL, ""))
    if len(sys.argv) != 2:
        print(f"Usage: {sys.argv[0]} <file>")
        sys.exit(1)

    source_file = Path(sys.argv[1])

    # Generate 2 colors graphic
    data_io, file_size = get_data_io(
        source_file,
        GREET_MSG_2COLORS,
    )
    graphic_width = math.ceil(math.sqrt(file_size * 8))
    graphic_height = graphic_width
    print(f"Generating 2 colors graphic: {graphic_width}x{graphic_height}")
    graphic = gen_2_colors_graphic(data_io, graphic_width, graphic_height)
    graphic.save(f"{source_file.name}-2colors.png")
    print(f"Saved to {source_file.name}-2colors.png")

    # Generate 256 colors graphic
    data_io, file_size = get_data_io(
        source_file,
        GREET_MSG_256COLORS,
    )
    graphic_width = math.ceil(math.sqrt(file_size / 3))
    graphic_height = graphic_width
    print(f"Generating 256 colors graphic: {graphic_width}x{graphic_height}")
    graphic = gen_256_colors_graphic(data_io, graphic_width, graphic_height)
    graphic.save(f"{source_file.name}-256colors.png")
    print(f"Saved to {source_file.name}-256colors.png")

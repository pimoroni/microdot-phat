from microdotphat.font import font

from PIL import Image

char_width = 5
char_height = 7

image_width = (char_width + 1) * 16 + 1
image_height = (char_height + 1) * 16 + 1

ascii_image = Image.open("font-ascii.png")

if not ascii_image.size == (image_width, image_height):
    raise RuntimeError("Image size must be {}x{}".format(image_width, image_height))

for char in range(32, 256):
    char_x = char % 16
    char_y = char // 16
    char_px = (char_width + 1) * char_x + 1
    char_py = (char_height + 1) * char_y + 1
    for fx in range(5):
        col = 0
        for fy in range(7):
            p = ascii_image.getpixel((char_px + fx, char_py + fy)) == (0, 0, 0)
            col |= (p << fy)
    if char not in font:
        font[char] = [0, 0, 0, 0, 0]
    font[char][fx] = col

print("font = {")
font_keys = list(font.keys())
font_keys.sort()
for key in font_keys:
    c0, c1, c2, c3, c4 = font[key]
    char = "???"
    if key > 32:
        char = chr(key)
    if key == 32:
        char = "(space)"
    print(f"    {key}: [0x{c0:02x}, 0x{c1:02x}, 0x{c2:02x}, 0x{c3:02x}, 0x{c4:02x}], # {char}")
print("}")
from microdotphat.font import font

from PIL import Image

char_width = 5
char_height = 7

image_width = (char_width + 1) * 16 + 1
image_height = (char_height + 1) * 16 + 1

ascii_image = Image.new("RGB", (image_width, image_height), (255, 255, 255))

for char in range(256):
    char_x = char % 16
    char_y = char // 16
    char_px = (char_width + 1) * char_x + 1
    char_py = (char_height + 1) * char_y + 1
    if char in font:
        cols = font[char]
        for fx in range(5):
            for fy in range(7):
                p = cols[fx] & (1 << fy)
                if p:
                    ascii_image.putpixel((char_px + fx, char_py + fy), (0, 0, 0))

ascii_image.save("font-ascii.png")



from PIL import Image, ImageDraw
import string
import os

symbols = ''.join(sorted(set(string.printable + string.whitespace)))
symbols = symbols[:256]

def rgb_bg(r, g, b):
    return f"\033[48;2;{r};{g};{b}m"

def encode(text):
    while len(text) % 3 != 0:
        text += ' '

    W = min(len(text) // 3, 256)
    if W == 0:
        W = 1
    H = (len(text) // 3) // W + (1 if (len(text) // 3) % W != 0 else 0)

    if W == 256 and H == 256:
        W += 1
        H += 1

    encoded = Image.new("RGB", (W, H), (255, 255, 255))
    draw = ImageDraw.Draw(encoded)

    for i in range(0, len(text), 3):
        color = tuple(symbols.index(c) if c in symbols else 0 for c in text[i:i + 3])
        while len(color) < 3:
            color += (0,)
        x, y = (i // 3) % W, (i // 3) // W
        draw.point((x, y), color)

        r, g, b = color
        print(f"Pixel {(i // 3):2}: {rgb_bg(r, g, b)}     \033[0m {color} | {symbols[r],symbols[g],symbols[b]}")

    encoded.save("encoded.png")

def decode(image_path):
    encoded = Image.open(image_path)
    width, height = encoded.size
    pixels = encoded.load()

    decoded_text = ""

    for y in range(height):
        for x in range(width):
            r, g, b = pixels[x, y]
            if (r, g, b) == (255, 255, 255):
                continue
            for value in (r, g, b):
                if value < len(symbols):
                    decoded_text += symbols[value]

    return decoded_text

print("TXT2IMG (by viitlk)")
print("1. Text to Image")
print("2. Image to Text")
v = input("> ")
if v == "1":
    print("Enter text [Type \"stoptype\" to finish and encode your text] ")
    text = ""
    while True:
        i = input("> ")
        if i == "stoptype":
            break
        text += i + "\n"
    encode(text)
    print("Done! Encoded text is saved as encoded.png")
elif v == "2":
    print("Enter path of the image ")
    path = input("> ")
    if os.path.isfile(path):
        print(f"Decoded text:\n{decode(path)}")
    elif os.path.isdir(path):
        print("I can't decode folder, sorry")
    else:
        print("Seems like this path doesn't exist, check again your input please")
else:
    exit()

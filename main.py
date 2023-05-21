import json
import os
from colorsys import rgb_to_hsv
from colorama import Fore
from PIL import Image, ImageOps

# HAHAHAHA LMAO SHITTY CODE (i mean it works so nice :D)

def save_pixels_to_json(image_path, output_path):
    image = Image.open(image_path)
    width, height = image.size

    # too lazy to fix the mirror bug lmaoooo
    image = ImageOps.flip(image)

    # modify this for image resizing
    new_width = 70
    # DONT MODIFY THIS, THIS IS FOR KEEPING THE ASPECT RATIO
    new_height = int(height * new_width / width)

    print(new_width, new_height)

    image = image.resize((new_width, new_height))

    # image.save("./images/converted/debug.jpg")

    pixels = []
    pixel_number = 0

    for y in range(new_height):
        for x in range(new_width):
            r, g, b = image.getpixel((x, y))
            color = rgb_to_hsv(r, g, b)
            # print(color)
            pixel = {
                    'posx': x,
                    'posy': y,
                    'hsv': f"{color[0] * 360}a{color[1]}a{color[2] / 255}a0a0"
                    # 'red': r,
                    # 'green': g,
                    # 'blue': b
                }
            pixels.append(pixel)

    with open(output_path, "w") as json_file:
        json.dump(pixels, json_file, indent=4)

name = input("Select the file you want to convert (you must add the file extension): ")

if os.path.exists(f"./images/{name}"):
    if "." in name:
        if (name.endswith(".jpg")):
            image_path = f"./images/{name}"
        else:
            im = Image.open(f"./images/{name}").convert("RGB")
            im.save("./images/converted/image.jpg")
            image_path = "./images/converted/image.jpg"
else:
    print(Fore.YELLOW + "File not found")
    exit()

output_path = "./output.json"

try:
    save_pixels_to_json(image_path, output_path)
except Exception as err:
    print(Fore.RED + f"Error: {err}")

os.system("spwn build ./lib/convert.spwn --allow readfile")
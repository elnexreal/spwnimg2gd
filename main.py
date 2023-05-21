import json
import os
from colorsys import rgb_to_hsv
from colorama import Fore
from PIL import Image, ImageOps

# HAHAHAHA LMAO SHITTY CODE (i mean it works, so i don't rlly care :3)

def save_pixels_to_json(image_path, output_path):
    image = Image.open(image_path)
    width, height = image.size

    # too lazy to fix the mirror bug lmaoooo
    image = ImageOps.flip(image)

    # modify this for image resizing (bigger value = more objects)
    new_width = 50
    # DONT MODIFY THIS, THIS IS FOR KEEPING THE ASPECT RATIO
    new_height = int(height * new_width / width)
    image = image.resize((new_width, new_height))

    # iterates for every pixel
    pixels = []
    for y in range(new_height):
        for x in range(new_width):
            # gets current RGB for the current pixel in the iteration
            r, g, b = image.getpixel((x, y))
            # converts the RGB color to HSV
            color = rgb_to_hsv(r, g, b)
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

# check if the file name provided by the user is correct
if os.path.exists(f"./images/{name}"):
    # if the image is in jpg format don't convert
    if (name.endswith(".jpg")):
        image_path = f"./images/{name}"
    # if the image is rgb or another format convert it to jpg
    else:
        im = Image.open(f"./images/{name}").convert("RGB")
        im.save("./images/converted/image.jpg")
        image_path = "./images/converted/image.jpg"
else:
    print(Fore.YELLOW + "File not found")
    exit()

try:
    save_pixels_to_json(image_path, "./output.json")
except Exception as err:
    print(Fore.RED + f"Error: {err}")
else:
    print("Successfully converted to raw data, executing the spwn script... \n")

# spwn script execution
os.system("spwn build ./lib/convert.spwn --allow readfile")

# remove the output json (comment this line if you want to keep the file to see it)
os.remove('./output.json')
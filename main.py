import json
import os
from time import sleep
from colorsys import rgb_to_hsv
from colorama import Fore
from PIL import Image, ImageOps

# HAHAHAHA LMAO SHITTY CODE (i mean it works, so i don't rlly care :3)

# variables
output_path = "./output.json"
settings_path = "./settings.json"

os.system("cls")
print("SPWN Image to GD - by elnexreal")
print("Check out my github at https://github.com/elnexreal")
print("\n" + "Wait 1 second")

sleep(1)
os.system("cls")

def save_pixels_to_json(image_path, output_path, settings_path):

    with open(settings_path) as settingsfile:
        settings = json.loads(settingsfile.read())

    image = Image.open(image_path).convert("RGB")
    width, height = image.size

    # too lazy to fix the mirror bug lmaoooo
    image = ImageOps.flip(image)

    new_width = settings["resizeimg"]
    # DONT MODIFY THIS, THIS IS FOR KEEPING THE ASPECT RATIO
    new_height = int(height * new_width / width)
    image = image.resize((new_width, new_height))

    # iterates for every pixel
    pix = []
    out = {
        "pixels": pix,
        "channel": colchannel
    }
    for y in range(new_height):
        for x in range(new_width):
            # gets current RGB for the current pixel in the iteration
            r, g, b = image.getpixel((x, y))
            # print(f"RGBA: {r} {g} {b} {a} POSXY: {x} {y}")
            # converts the RGB color to HSV
            color = rgb_to_hsv(r, g, b)
            obj = {
                "posx": x,
                "posy": y,
                "hsv": f"{color[0] * 360}a{color[1]}a{color[2] / 255}a0a0",
            }
            pix.append(obj)

    with open(output_path, "w") as json_file:
        json.dump(out, json_file, indent=4)

name = input("Select the file you want to convert (you must add the file extension): ")
try:
    colchannel = int(input("Select the color channel you want to use for the objects: (1-999): "))
except ValueError as err:
    print(Fore.RED + "You must select a integer value (example: 51)")
    exit()

# check if the file name provided by the user is correct
if os.path.exists(f"./images/{name}"):
    image_path = f"./images/{name}"
    print(image_path)
else:
    print(Fore.YELLOW + "File not found")
    exit()

save_pixels_to_json(image_path, output_path, settings_path)

print("Successfully converted to raw data, executing the spwn script... \n")

# spwn script execution
try:
    os.system("spwn build ./lib/convert.spwn --allow readfile")
except Exception as err:
    print(Fore.RED + err)

# remove the output json
os.remove("./output.json")
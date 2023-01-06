'''Everything required to generate thumbnails for HatDatabase'''
import os
import json
from enum import Enum
from PIL import Image, UnidentifiedImageError

class GeneratedStatus(Enum):
    '''Enum returned after generating a thumbnail'''
    SUCCESS = 1
    FAILED_UNIDENTIFIED_IMAGE = 2
    FAILED_IO_ERROR = 3
    SKIPPED_EXISTS = 4
    SKIPPED_PREVIEW_OR_TEMPLATE = 5
    SKIPPED_NO_JSON = 6

def remove_colour(image: Image.Image, red: int, green: int, blue: int):
    '''Make a colour transparent in an image'''
    image = image.convert("RGBA")
    data = image.getdata()
    new_data = []
    for item in data:
        if item[0] == red and item[1] == green and item[2] == blue:
            new_data.append((255, 255, 255, 0))
        else:
            new_data.append(item)
    image.putdata(new_data)
    return image

def wipe_folders(confirm_first: bool = True):
    '''Wipe all thumbnail folders'''
    if confirm_first:
        print("This will delete all files from the following folders:")
        print("./static/thumbs/ ./static/thumbs-large/ ./static/quack-thumbs/ ./static/quack-thumbs-large/ ./static/capes/ ./static/rocks/")
        print('\033[91m' + "ARE YOU SURE YOU WANT TO DELETE ALL THUMBNAILS?" + '\u001b[0m' + " (y/*): ", end='')
        if input() != 'y':
            print("\nAborting...")
            exit()
    print("\nWiping thumbail folders...")
    for filename in os.listdir('./static/thumbs/'):
        os.remove('./static/thumbs/' + filename)
    for filename in os.listdir('./static/thumbs-large/'):
        os.remove('./static/thumbs-large/' + filename)
    for filename in os.listdir('./static/quack-thumbs/'):
        os.remove('./static/quack-thumbs/' + filename)
    for filename in os.listdir('./static/quack-thumbs-large/'):
        os.remove('./static/quack-thumbs-large/' + filename)
    for filename in os.listdir('./static/capes/'):
        os.remove('./static/capes/' + filename)
    for filename in os.listdir('./static/rocks/'):
        os.remove('./static/rocks/' + filename)

try:
    img_head = Image.open('./static/duck.png').convert("RGBA")
    img_quack = Image.open('./static/quack.png').convert("RGBA")
    img_rock= Image.open('./static/rock.png').convert("RGBA")
    json_file: list[dict] = json.load(open('./src/hats.json', encoding='utf-8'))
    print("\u001b[32m[generate_thumbs]:\u001b[0m Loaded duck heads and json\n")
except IOError:
    print("\u001b[31m [generate_thumbs]: Error: Could not find images requred to generate thumbnails")
    print("Please make sure the following files exist:")
    print("./static/duck_head.png ./static/duck_head_quack.png ./static/duck_head_large.png ./static/duck_head_quack_large.png \u001b[0m")
    exit()

def generate_thumbnail(filename: str, regen: bool = False) -> GeneratedStatus:
    '''Generates a thumbnail for a hat'''
    if (not os.path.exists('./static/thumbs/' + filename) or regen):
        try:
            entry = next(item for item in json_file if item["id"] == filename.removesuffix('.png'))
        except StopIteration:
            return GeneratedStatus.SKIPPED_NO_JSON
        if entry['name'] == 'preview' or entry['name'] == 'template':
            return GeneratedStatus.SKIPPED_PREVIEW_OR_TEMPLATE
        try:
            img_bad = Image.open('./static/hats/' + filename)
        except UnidentifiedImageError:
            return GeneratedStatus.FAILED_UNIDENTIFIED_IMAGE
        except IOError:
            return GeneratedStatus.FAILED_IO_ERROR
        
        img = remove_colour(img_bad, 255, 0, 255)
        img_bad.close()
        head = img.crop((0, 0, 32, 32))
        head_bg = img_head.copy()
        head_bg.alpha_composite(head)
        head_bg.resize((128, 128), Image.Resampling.NEAREST).save('./static/thumbs/' + filename)
        head.close()
        head_bg.close()
        head_large = img.crop((0, 0, 32, 32))
        head_large_bg = img_head.copy()
        head_large_bg.alpha_composite(head_large)
        head_large_bg.resize((256, 256), Image.Resampling.NEAREST).save('./static/thumbs-large/' + filename)
        head_large.close()
        head_large_bg.close()
        if img.width > 32:
            quack = img.crop((32, 0, 64, 32))
            quack_bg = img_quack.copy()
            quack_bg.alpha_composite(quack)
            quack_bg.resize((128, 128), Image.Resampling.NEAREST).save('./static/quack-thumbs/' + filename)
            quack.close()
            quack_bg.close()
            quack_large = img.crop((32, 0, 64, 32))
            quack_large_bg = img_quack.copy()
            quack_large_bg.alpha_composite(quack_large)
            quack_large_bg.resize((256, 256), Image.Resampling.NEAREST).save('./static/quack-thumbs-large/' + filename)
            quack_large.close()
            quack_large_bg.close()
            cape = img.crop((64, 0, 96, 32))
            if cape.getcolors() != [(65536, (0, 0, 0, 0))]:
                cape.resize((256, 256), Image.Resampling.NEAREST).save('./static/capes/' + filename)
            cape.close()
            if img.height > 32:
                rock = img.crop((0, 32, 24, 56))
                if rock.getcolors() != [(82944, (0, 0, 0, 0))]:
                    rock_bg = img_rock.copy()
                    rock_bg.alpha_composite(rock)
                    rock_bg.resize((288, 288), Image.Resampling.NEAREST).save('./static/rocks/' + filename)
                    rock_bg.close()
                rock.close()
        else:
            no_quack = img.crop((0, 0, 32, 32))
            no_quack_bg = img_quack.copy()
            no_quack_bg.alpha_composite(no_quack)
            no_quack_bg.resize((256, 256), Image.Resampling.NEAREST).save('./static/quack-thumbs/' + filename)
            no_quack.close()
            no_quack_bg.close()
        img.close()
        return GeneratedStatus.SUCCESS
    else:
        return GeneratedStatus.SKIPPED_EXISTS

def dispose_images():
    '''Dispose images used for generating thumbnails'''
    img_head.close()
    img_quack.close()
    img_rock.close()
    
import os
import json
import shutil
import generate_thumbs as gt

def main():
    '''Generates thumbnails and json data required for new hats'''
    if not os.path.exists('./static/hats/'):
        print("'./static/hats/' folder not found. Make sure you're running this script from the root of the repository.")
        exit()

    if not os.path.exists('./static/thumbs/'):
        os.mkdir('./static/thumbs/')
    if not os.path.exists('./static/thumbs-large/'):
        os.mkdir('./static/thumbs-large/')
    if not os.path.exists('./static/quack-thumbs/'):
        os.mkdir('./static/quack-thumbs/')
    if not os.path.exists('./static/quack-thumbs-large/'):
        os.mkdir('./static/quack-thumbs-large/')
    if not os.path.exists('./static/capes/'):
        os.mkdir('./static/capes/')
    if not os.path.exists('./static/rocks/'):
        os.mkdir('./static/rocks/')

    entries = 0
    progress = success = skipped = failed = 0

    if os.path.exists('./src/hats.json'):
        json_data = json.load(open('./src/hats.json', encoding='utf-8'))
        entries = len(json_data)
        print("Using existing hats.json")
    else:
        print("Couldn't find hats.json, a new one will be created")
        
    print("")
    hats = os.listdir('./static/hats-in/')
    for hat in hats:
        progress += 1
        
        if not hat.endswith('.png'):
            skipped += 1
            break
            
        entries += 1
        new_hat = str(entries) + '.png'
        shutil.copyfile('./static/hats-in/' + hat, './static/hats/' + new_hat)
        json_data.append({'id': entries, 'name': hat.removesuffix('.png')})
        print(f"Added {hat} as {new_hat}")
            
        result = gt.generate_thumbnail(new_hat)
        if result == gt.GeneratedStatus.SUCCESS:
            success += 1
            os.remove('./static/hats-in/' + hat)
        elif result == gt.GeneratedStatus.SKIPPED_EXISTS:
            skipped += 1
        elif result == gt.GeneratedStatus.SKIPPED_PREVIEW_OR_TEMPLATE:
            skipped += 1
            print("\033[A                             \033[A")
            print('\033[93m' + f"Skipping Template / Preview ({new_hat})\n")
        elif result == gt.GeneratedStatus.SKIPPED_NO_JSON:
            skipped += 1
            print("\033[A                             \033[A")
            print('\033[93m' + f"Skipping hat with no associated json data ({new_hat})\n")
        elif result == gt.GeneratedStatus.FAILED_UNIDENTIFIED_IMAGE:
            failed += 1
            print("\033[A                             \033[A")
            print('\033[91m' + f"PIL.UnidentifiedImageError: Unable to open as image ({new_hat})\n")
        elif result == gt.GeneratedStatus.FAILED_IO_ERROR:
            print("\033[A                             \033[A")
            print('\033[91m' + f"IOError: An error occured while reading / writing to file {new_hat}\n")
            failed += 1
        print("\033[A                             \033[A")
        print('\u001b[0m' + f"Progress {progress}/{len(hats)}")
    if (success + skipped + failed) == 0:
        print("No hats were added")
    elif success > 0:
        json.dump(json_data, open('./src/hats.json', 'w', encoding='utf-8'))

if __name__ == '__main__':
    main()

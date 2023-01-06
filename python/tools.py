import os
import sys
import generate_thumbs as gt

def main():
    '''Script for managing thumbnails and json data'''
    hats = os.listdir('./static/hats/')
    progress = success = skipped = failed = 0
    nowarn = False

    if '-wipe' in sys.argv:
        gt.wipe_folders()
    if '-nowarn' in sys.argv:
        nowarn = True
    for hat in hats:
        result = gt.generate_thumbnail(hat)
        progress += 1
        if result == gt.GeneratedStatus.SUCCESS:
            success += 1
        elif result == gt.GeneratedStatus.SKIPPED_EXISTS:
            skipped += 1
        elif result == gt.GeneratedStatus.SKIPPED_PREVIEW_OR_TEMPLATE:
            skipped += 1
            if not nowarn:
                print("\033[A                             \033[A")
                print('\033[93m' + f"Skipping Template / Preview ({hat})\n")
        elif result == gt.GeneratedStatus.FAILED_UNIDENTIFIED_IMAGE:
            failed += 1
            print("\033[A                             \033[A")
            print('\033[91m' + f"PIL.UnidentifiedImageError: Unable to open as image ({hat})\n")
        elif result == gt.GeneratedStatus.FAILED_IO_ERROR:
            print("\033[A                             \033[A")
            print('\033[91m' + f"IOError: An error occured while reading / writing to file {hat}\n")
            failed += 1
        print("\033[A                             \033[A")
        print('\u001b[0m' + f"Progress {progress}/{len(hats)}")
    gt.dispose_images()
    print('\u001b[0m' + f'{success} thumbnails generated, {failed} failed, {skipped} skipped')
    print("'-wipe' Wipe all thumbnail folders before generating thumbnails")
    print("'-nowarn' Surpress warnings about preview and template hats")

if __name__ == "__main__":
    main()

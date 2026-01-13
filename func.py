import os
import time as t
from PIL import Image, ImageEnhance
import easyocr
import random as r
import subprocess

reader = easyocr.Reader(['en'])

devices = "emulator-"

def tap(x, y, port):
    os.system(f'adb -s {devices}{str(port)} shell input tap {str(x)} {str(y)}')

def swipe(port): 
    os.system(f'adb -s {devices}{str(port)} shell input touchscreen swipe 1450 150 900 650 500 ')

def swipe2(port): 
    os.system(f'adb -s {devices}{str(port)} shell input touchscreen swipe 1900 850 100 850 500 ')

def find(port): 
    tap(110, 785, port)
    t.sleep(0.3)
    tap(300, 650, port)
    t.sleep(0.3)
    tap(1435, 800, port)

def next(port):
    tap(1470, 650, port)

def do_return_home(port):
    tap(800, 770, port)

def check_loot(port):
    screenshoot(port=port, filename='val')
    pull_file(port=port)
    print("captured")
    t.sleep(2)

    with Image.open("Pictures/"+port+'val.png') as photo:
        (left, upper, right, lower) = (50, 120, 285, 295)
        loot = photo.crop((left, upper, right, lower))

        # Convert to grayscale
        loot = loot.convert('L')
        # Increase contrast
        loot = ImageEnhance.Contrast(loot).enhance(2.0)
        # Binarize (convert to black and white)
        loot = loot.point(lambda x: 0 if x < 250 else 255)

        loot = loot.save("Pictures/"+ port +"val.png")

        check_loot.result = reader.readtext(("Pictures/"+ port +"val.png"), allowlist='0123456789', detail = 0)
        check_loot.status = True
        if len(check_loot.result) < 3:
            print("not enough loot values detected, checking screen state")
            
            is_return_home = check_return_home(port)
            if is_return_home:
                print("returning home")
                do_return_home(port)

            is_attack_button = check_attack_button(port)
            if is_attack_button:
                print("attack button detected, going to next base")
                find(port)
            
            # find(port)
            check_loot.result = ["0", "0", "0"]  # Default values if OCR fails
            check_loot.status = False

def checktrophies(port):
    screenshoot(port=port, filename='trophies')
    pull_file(port=port)
    print("captured")
    t.sleep(2)

    with Image.open("Pictures/"+port+'trophies.png') as photo:
        (left, upper, right, lower) = (130, 160, 255, 210)
        trophies = photo.crop((left, upper, right, lower))

        # Convert to grayscale
        trophies = trophies.convert('L')
        # Increase contrast
        trophies = ImageEnhance.Contrast(trophies).enhance(2.0)
        # Binarize (convert to black and white)
        trophies = trophies.point(lambda x: 0 if x < 240 else 255)

        trophies = trophies.save("Pictures/"+ port +"trophies.png")

        checktrophies.result = reader.readtext(("Pictures/"+ port +"trophies.png"), allowlist='0123456789', detail = 0)

def check_pixel(port):
    screenshoot(port=port, filename='return')
    pull_file(port=port)

    checkp = Image.open("Pictures/"+ port +'return.png')
    if checkp.getpixel((898, 909)) == checkp.getpixel((969, 938)):
        return(True)
    else:
        return(False)

def checkpixelBB(port, x, y):
    screenshoot(port=port, filename='return')
    pull_file(port=port)

    checkp = Image.open("Pictures/" + port + 'return.png')
    print(f"Image size: {checkp.size}")  # Print the size of the image

    process_image_for_ocr(port, 'return_fix', (741, 740, 859, 797), enhance_factor=1.0, binarize_threshold=250)
    ocr_result = perform_ocr(port, 'return_fix_crop', None)

    if len(ocr_result) == 0:
        ocr_result = ["0", "0", "0"]  # Default values if OCR fails

    print(f"OCR Result: {ocr_result}")  # Debug print to see OCR results
    return str(checkp.getpixel((x, y)))

def screenshoot(port, filename):
    os.system(f'adb -s {devices}{str(port)} shell screencap -p /sdcard/Pictures/{port}{filename}.png ')

def pull_file(port):
    os.system(f'adb -s {devices}{str(port)} pull sdcard/Pictures/')

def check_return_home(port) -> bool:
    print("Checking for Return Home button...")
    screenshoot(port=port, filename='return')
    pull_file(port=port)

    checkp = Image.open("Pictures/" + port + 'return.png')
    print(f"Image size: {checkp.size}")  # Print the size of the image

    process_image_for_ocr(port, 'return', (741, 740, 859, 797), enhance_factor=1.0, binarize_threshold=250)
    ocr_result = perform_ocr(port, 'return_crop', None)

    if len(ocr_result) == 0:
        ocr_result = ["0", "0", "0"]  # Default values if OCR fails

    print(f"OCR Result: {ocr_result}")  # Debug print to see OCR results
    if ocr_result[0] == 'RetuRN' and ocr_result[1] == 'Home':
        return True

    return False

def check_attack_button(port) -> bool:
    print("Checking for Attack button...")
    screenshoot(port=port, filename='attack')
    pull_file(port=port)

    checkp = Image.open("Pictures/" + port + 'attack.png')
    print(f"Image size: {checkp.size}")  # Print the size of the image

    process_image_for_ocr(port, 'attack', (43, 831, 167, 866), enhance_factor=1.0, binarize_threshold=250)
    ocr_result = perform_ocr(port, 'attack_crop', 'atck')

    if len(ocr_result) == 0:
        ocr_result = ["0", "0", "0"]  # Default values if OCR fails

    print(f"OCR Result: {ocr_result}")  # Debug print to see OCR results
    if ocr_result[0] == "attack":
        return True

    return False

def process_image_for_ocr(port, filename, crop_coords, enhance_factor=1.0, binarize_threshold=250):
    with Image.open("Pictures/" + port + filename + ".png") as photo:
        loot = photo.crop(crop_coords)

        # Convert to grayscale
        loot = loot.convert('L')
        # Increase contrast
        loot = ImageEnhance.Contrast(loot).enhance(enhance_factor)
        # Binarize (convert to black and white)
        loot = loot.point(lambda x: 0 if x < binarize_threshold else 255)

        loot.save("Pictures/" + port + filename + "_crop.png")

def perform_ocr(port, filename, allowlist=None):
    return reader.readtext(image=("Pictures/" + port + filename + ".png"), allowlist=allowlist, detail=0)


import func as f
from func import screenshoot, pull_file, process_image_for_ocr_new, perform_ocr_new
from PIL import Image

p = '5554' # port

def test_ocr(filename):
    checkp = Image.open(filename)
    print(f"Image size: {checkp.size}")  # Print the size of the image

    process_image_for_ocr_new(
        image_path=filename, 
        result_path=filename.replace(".png", "_crop.png"), 
        crop_coords=(78, 124, 259, 259), 
        enhance_factor=2.5, 
        binarize_threshold=250
    )
    ocr_result = perform_ocr_new(filename.replace(".png", "_crop.png"), allowlist="0123456789")

    if len(ocr_result) == 0:
        ocr_result = ["0", "0", "0"]  # Default values if OCR fails

    print(f"OCR Result: {ocr_result}")  # Debug print to see OCR results
    return None

def get_screenshoot(port, filename):
    f.screenshoot(port=port, filename=filename)
    f.pull_file(port=port, filename=filename)

    checkp = Image.open("Pictures/" + port + filename + ".png")
    print(f"Image size: {checkp.size}")  # Print the size of the image
    return checkp

if __name__ == "__main__":
    test_ocr("example_find_state2.png")
    # get_screenshoot(port=p, filename='welcome-back')

# return @ 888 900 = (180, 230, 125, 255)
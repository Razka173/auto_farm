import cv2
import os

TEMPLATE_DIR = "references"   # where your template images are

THRESHOLD = 0.97  # strict for maximum accuracy

def detect_state_template(screen_img, state_name):
    template_path = os.path.join(TEMPLATE_DIR, f"ref_{state_name}.png")

    template = cv2.imread(template_path)
    if template is None:
        return False, 0.0

    screen_gray = cv2.cvtColor(screen_img, cv2.COLOR_BGR2GRAY)
    template_gray = cv2.cvtColor(template, cv2.COLOR_BGR2GRAY)

    result = cv2.matchTemplate(
        screen_gray,
        template_gray,
        cv2.TM_CCOEFF_NORMED
    )

    _, max_val, _, _ = cv2.minMaxLoc(result)

    return max_val >= THRESHOLD, max_val

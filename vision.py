import cv2
import numpy as np
import pyautogui
from windowCapture import get_frame

# Load the template image
template = cv2.imread("exclamation.png", cv2.IMREAD_COLOR)
template_gray = cv2.cvtColor(template, cv2.COLOR_BGR2GRAY)
template_width, template_height = template_gray.shape[::-1]

def detect_exclamation(frame):
    frame_gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    result = cv2.matchTemplate(frame_gray, template_gray, cv2.TM_CCOEFF_NORMED)
    threshold = 0.7
    locations = np.where(result >= threshold)
    clicked = False
    for pt in zip(*locations[::-1]):
        cv2.rectangle(frame, pt, (pt[0] + template_width, pt[1] + template_height), (0, 255, 0), 2)
        
        if not clicked:  # Only click once per detection loop
            pyautogui.click()  # Click at the current mouse position
            clicked = True  # Prevents multiple clicks in a single frame detection
    return frame

def main():
    window_title = "Roblox"  # Replace with the actual window title
    while True:
        frame = get_frame(window_title)
        frame_with_detection = detect_exclamation(frame)
        cv2.imshow("Live Window Feed with Detection", frame_with_detection)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    cv2.destroyAllWindows()

# Uncomment to run
main()

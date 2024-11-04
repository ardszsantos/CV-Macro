import cv2
import numpy as np
import pyautogui
import keyboard
import time
from windowCapture import get_frame

# Load templates in grayscale (black and white)
template1 = cv2.imread("exclamation.png", cv2.IMREAD_GRAYSCALE)
template1_width, template1_height = template1.shape[::-1]

template2 = cv2.imread("fishCaught2.png", cv2.IMREAD_GRAYSCALE)
template2_width, template2_height = template2.shape[::-1]

# Define thresholds for each template
THRESHOLD1 = 0.7  # Threshold for the first image (exclamation mark)
THRESHOLD2 = 0.6  # Threshold for the second image (stopping condition)

# Variables to manage state
clicking_active = False
primary_rect = None
secondary_rect = None
sequence_executed = True
frame_count = 0
secondary_check_interval = 5  # Check for the secondary image every 5 frames

# Security check timer
last_detection_time = time.time()
security_check_interval = 120  # 2 minutes in seconds

# Detect primary image and manage clicking
def detect_primary(frame_gray):
    global clicking_active, primary_rect, last_detection_time
    result = cv2.matchTemplate(frame_gray, template1, cv2.TM_CCOEFF_NORMED)
    locations = np.where(result >= THRESHOLD1)
    
    if len(locations[0]) > 0:  # Primary image detected
        clicking_active = True
        pt = (locations[1][0], locations[0][0])
        primary_rect = (pt, (pt[0] + template1_width, pt[1] + template1_height))
        last_detection_time = time.time()  # Reset security timer
    else:
        primary_rect = None  # Clear rectangle if image not detected

# Detect secondary image, run sequence if image disappears
def detect_secondary(frame_gray):
    global clicking_active, secondary_rect, sequence_executed, last_detection_time
    result = cv2.matchTemplate(frame_gray, template2, cv2.TM_CCOEFF_NORMED)
    locations = np.where(result >= THRESHOLD2)
    
    if len(locations[0]) > 0:  # Secondary image detected
        clicking_active = False
        pt = (locations[1][0], locations[0][0])
        secondary_rect = (pt, (pt[0] + template2_width, pt[1] + template2_height))
        sequence_executed = False  # Reset sequence for when image disappears
        last_detection_time = time.time()  # Reset security timer
    else:
        secondary_rect = None  # Clear secondary rectangle if image not detected
        if not sequence_executed:  # Execute only once after image disappears
            execute_sequence()
            sequence_executed = True

# Sequence to execute after secondary image detection
def execute_sequence():
    time.sleep(5)
    keyboard.press_and_release("3")
    for _ in range(3):
        pyautogui.click()
        time.sleep(0.3)
    time.sleep(2)
    keyboard.press_and_release("1")
    pyautogui.click()

# Security sequence to run if no detection occurs within the time interval
def security_check():
    keyboard.press_and_release("1")
    time.sleep(2)
    keyboard.press_and_release("1")
    time.sleep(1)
    pyautogui.click()

def main():
    global primary_rect, secondary_rect, frame_count, last_detection_time
    window_title = "Roblox"
    
    while True:
        frame = get_frame(window_title)
        frame_gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)  # Convert frame to grayscale

        # Run security check if no detection has occurred within the specified interval
        if time.time() - last_detection_time > security_check_interval:
            security_check()
            last_detection_time = time.time()  # Reset timer after security check

        detect_primary(frame_gray)  # Check primary image
        if frame_count % secondary_check_interval == 0:
            detect_secondary(frame_gray)  # Check secondary image less frequently

        # Draw rectangles only when images are detected
        if primary_rect is not None:
            cv2.rectangle(frame, primary_rect[0], primary_rect[1], (0, 255, 0), 2)
        if secondary_rect is not None:
            cv2.rectangle(frame, secondary_rect[0], secondary_rect[1], (0, 0, 255), 2)

        if clicking_active:
            pyautogui.click()

        cv2.imshow("Live Window Feed with Detection (Black and White)", frame_gray)  # Display in grayscale
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

        frame_count += 1

    cv2.destroyAllWindows()

# Uncomment to run
main()

import cv2
import numpy as np
import win32gui
import mss

def get_window_position(window_title):
    window_handle = win32gui.FindWindow(None, window_title)
    if window_handle == 0:
        raise ValueError("Window not found.")
    left, top, right, bottom = win32gui.GetWindowRect(window_handle)
    width = right - left
    height = bottom - top
    return left, top, width, height

def capture_screen_region(left, top, width, height):
    with mss.mss() as sct:
        monitor = {"left": left, "top": top, "width": width, "height": height}
        screenshot = sct.grab(monitor)
        img = np.array(screenshot)
        return cv2.cvtColor(img, cv2.COLOR_BGRA2BGR)

def get_frame(window_title):
    left, top, width, height = get_window_position(window_title)
    return capture_screen_region(left, top, width, height)

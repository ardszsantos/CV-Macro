import numpy as np
import win32gui, win32ui, win32con
import cv2

class WindowCapture:

    # constructor
    def __init__(self, window_name=None):
        # Set properties
        self.hwnd = None
        self.window_name = window_name
        self.w = 0
        self.h = 0
        self.cropped_x = 0
        self.cropped_y = 0
        self.offset_x = 0
        self.offset_y = 0

        # Find the window if a name is given, else default to full screen
        if window_name:
            self.hwnd = win32gui.FindWindow(None, window_name)
            if not self.hwnd:
                raise Exception(f'Window not found: {window_name}')

            # Get window size and position
            window_rect = win32gui.GetWindowRect(self.hwnd)
            self.w = window_rect[2] - window_rect[0]
            self.h = window_rect[3] - window_rect[1]

            # Account for window borders
            border_pixels = 8
            titlebar_pixels = 30
            self.w -= (border_pixels * 2)
            self.h -= titlebar_pixels + border_pixels
            self.cropped_x = border_pixels
            self.cropped_y = titlebar_pixels

            # Calculate offsets to translate coordinates
            self.offset_x = window_rect[0] + self.cropped_x
            self.offset_y = window_rect[1] + self.cropped_y
        else:
            # Capture the entire screen if no window name provided
            screen_rect = win32gui.GetWindowRect(win32gui.GetDesktopWindow())
            self.w = screen_rect[2] - screen_rect[0]
            self.h = screen_rect[3] - screen_rect[1]

    def get_screenshot(self):
        # Capture full screen
        wDC = win32gui.GetWindowDC(win32gui.GetDesktopWindow())
        dcObj = win32ui.CreateDCFromHandle(wDC)
        cDC = dcObj.CreateCompatibleDC()
        dataBitMap = win32ui.CreateBitmap()
        dataBitMap.CreateCompatibleBitmap(dcObj, self.w, self.h)
        cDC.SelectObject(dataBitMap)

        # Capture the screen image
        cDC.BitBlt((0, 0), (self.w, self.h), dcObj, (0, 0), win32con.SRCCOPY)

        # Convert to numpy array
        signedIntsArray = dataBitMap.GetBitmapBits(True)
        img = np.frombuffer(signedIntsArray, dtype='uint8')
        img.shape = (self.h, self.w, 4)

        # Free resources
        dcObj.DeleteDC()
        cDC.DeleteDC()
        win32gui.ReleaseDC(self.hwnd, wDC)
        win32gui.DeleteObject(dataBitMap.GetHandle())

        # Convert to BGR and drop the alpha channel
        img = img[..., :3]
        img = np.ascontiguousarray(img)

        # Crop to the window if a specific window was selected
        if self.window_name:
            img = img[self.offset_y:self.offset_y + self.h, self.offset_x:self.offset_x + self.w]

        return img

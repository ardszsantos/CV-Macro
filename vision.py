import cv2 as cv
import numpy as np
import pyautogui
import time
import keyboard


class Vision:
    # properties
    needle_img = None
    needle_w = 0
    needle_h = 0
    method = None

    # constructor
    def __init__(self, needle_img_path, method=cv.TM_CCOEFF_NORMED):
        # load the image we're trying to match
        # Load the image in grayscale directly
        self.needle_img = cv.imread(needle_img_path, cv.IMREAD_GRAYSCALE)

        # Save the dimensions of the needle image
        self.needle_w = self.needle_img.shape[1]
        self.needle_h = self.needle_img.shape[0]

        # There are 6 methods to choose from:
        # TM_CCOEFF, TM_CCOEFF_NORMED, TM_CCORR, TM_CCORR_NORMED, TM_SQDIFF, TM_SQDIFF_NORMED
        self.method = method


    def realizar_cliques(self, tempo_total):
        tempo_inicial = time.time()

        while (time.time() - tempo_inicial) < tempo_total:
            pyautogui.tripleClick(button='left')
            pyautogui.click(clicks=200)

            # Aguarde um curto período de tempo entre cliques (ajuste conforme necessário)
            time.sleep(0.1)

    def find(self, haystack_img, threshold=0.5, debug_mode=None):
        # Convert haystack_img to grayscale (CV_8U)
        haystack_img = cv.cvtColor(haystack_img, cv.COLOR_BGR2GRAY)

        # Ensure images have the same data type (CV_8U)
        haystack_img = haystack_img.astype(np.uint8)
        self.needle_img = self.needle_img.astype(np.uint8)

        # run the OpenCV algorithm
        result = cv.matchTemplate(haystack_img, self.needle_img, self.method)

        # Get the all the positions from the match result that exceed our threshold
        locations = np.where(result >= threshold)
        locations = list(zip(*locations[::-1]))

        # You'll notice a lot of overlapping rectangles get drawn. We can eliminate those redundant
        # locations by using groupRectangles().
        # First we need to create the list of [x, y, w, h] rectangles
        rectangles = []


        for loc in locations:
            rect = [int(loc[0]), int(loc[1]), self.needle_w, self.needle_h]
            # Add every box to the list twice in order to retain single (non-overlapping) boxes
            rectangles.append(rect)
            rectangles.append(rect)
            
        # Apply group rectangles.
        # The groupThreshold parameter should usually be 1. If you put it at 0 then no grouping is
        # done. If you put it at 2 then an object needs at least 3 overlapping rectangles to appear
        # in the result. I've set eps to 0.5, which is:
        # "Relative difference between sides of the rectangles to merge them into a group."
        rectangles, weights = cv.groupRectangles(rectangles, groupThreshold=1, eps=0.5)

        points = []
        if len(rectangles):
            line_color = (0, 255, 0)
            line_type = cv.LINE_4
            marker_color = (255, 0, 255)
            marker_type = cv.MARKER_CROSS

            # Loop over all the rectangles
            for (x, y, w, h) in rectangles:
                # Determine the center position
                center_x = x + int(w/2)
                center_y = y + int(h/2)
                # Save the points
                points.append((center_x, center_y))

                # Se deseja realizar ações coordenadas com o mouse após a detecção
                # Irá clicar por 12 segundos, caso um retangulo tenha sido identificado 
                self.realizar_cliques(12)
                pyautogui.sleep(6)
                keyboard.press_and_release('1')
                pyautogui.sleep(0.5)
                keyboard.press_and_release('1')
                pyautogui.click()

                
                
                if debug_mode == 'rectangles':
                    # Determine the box position
                    top_left = (x, y)
                    bottom_right = (x + w, y + h)
                    # Draw the box
                    cv.rectangle(haystack_img, top_left, bottom_right, color=line_color, 
                                lineType=line_type, thickness=2)

                elif debug_mode == 'points':
                    # Draw the center point
                    cv.drawMarker(haystack_img, (center_x, center_y), 
                                color=marker_color, markerType=marker_type, 
                                markerSize=40, thickness=2)

        if debug_mode:
            cv.imshow('Matches', haystack_img)

        return points

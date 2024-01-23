import cv2 as cv
import numpy as np
import os
from time import time, sleep
from windowcapture import WindowCapture
from vision import Vision
import pyautogui
import keyboard

# Change the working directory to the folder this script is in.
# Doing this because I'll be putting the files from each video in their own folder on GitHub
os.chdir(os.path.dirname(os.path.abspath(__file__)))



# initialize the WindowCapture class
wincap = WindowCapture('Roblox')
# initialize the Vision class
vision_limestone = Vision('images/pescamini.png')


last_rectangle_time = time()
last_keypress_time = time()

'''
# https://www.crazygames.com/game/guns-and-bottle
wincap = WindowCapture()
vision_gunsnbottle = Vision('gunsnbottle.jpg')
'''

loop_time = time()
while True:
    # get an updated image of the game
    screenshot = wincap.get_screenshot()

    # display the processed image
    points = vision_limestone.find(screenshot, 0.8, 'rectangles')

    if points:
    # Update the last_rectangle_time with the current time
        last_rectangle_time = time()

    # debug the loop rate
    print('FPS {}'.format(1 / (time() - loop_time)))
    loop_time = time()

    # Check if more than 2 minutes have passed since the last rectangle was found
    elapsed_time = time() - last_rectangle_time
    if elapsed_time > 40:
        pyautogui.click()
        last_rectangle_time = time()

        # Update the last_rectangle_time after clicking
        last_rectangle_time = time()

    

    #Checks if 1000 seconds has passed, and when it does it presses on the 2 slot and eat whatever is in it.
    elapsed_time_keypress = time() - last_keypress_time
    if elapsed_time_keypress > 1000:
        keyboard.press_and_release('2')
        pyautogui.sleep(0.5)
        pyautogui.click(clicks=10, interval=0.4)
        pyautogui.sleep(0.5)
        keyboard.press_and_release('1')
        pyautogui.sleep(0.5)        
        pyautogui.click()

        # Reset both timers
        last_rectangle_time = time()
        last_keypress_time = time()

    # press 'q' with the output window focused to exit.
    # waits 1 ms every loop to process key presses
    if cv.waitKey(1) == ord('q'):
        cv.destroyAllWindows()
        break

print('Done.')
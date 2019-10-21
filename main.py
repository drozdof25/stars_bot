import cv2
from PIL import ImageGrab
import win32gui
import tkinter as tk
from tkinter.ttk import Combobox
import numpy as np

def get_window_info():
    def callback(hwnd, window_info):
        if win32gui.IsWindowVisible(hwnd):
            window_info[win32gui.GetWindowText(hwnd)] = hwnd
    window_info = {}
    win32gui.EnumWindows(callback, window_info)
    return  window_info
def data_screen():
    wind = window_info[combo.get()]
    win32gui.MoveWindow(wind,0,0,631,466,True)
    win32gui.SetForegroundWindow(wind)
    rect = win32gui.GetWindowRect(wind)
    print(rect)
    count = 0
    while(True):
        rect = win32gui.GetWindowRect(wind)
        screen = ImageGrab.grab((rect[0],rect[1],rect[2],rect[3]))
        screen_num = np.array(screen)
        first_hand = screen_num[304:326,284:302]
        second_hand = screen_num[304:326,325:343]
        for row in first_hand:
            for pixel in row:
                if np.all(pixel == np.array([255,255,255])):
                    pixel[pixel == 255] = 0
                else:
                    pixel[pixel < 255] = 255
        for row in second_hand:
            for pixel in row:
                if np.all(pixel == np.array([255,255,255])):
                    pixel[pixel == 255] = 0
                else:
                    pixel[pixel < 255] = 255
        cards = {
            '2': [cv2.imread('cards\\2.png')],
            '3': [cv2.imread('cards\\3.png')],
            '4': [cv2.imread('cards\\4.png')],
            '5': [cv2.imread('cards\\5.png')],
            '6': [cv2.imread('cards\\6.png')],
            '7': [cv2.imread('cards\\7.png')],
            '8': [cv2.imread('cards\\8.png')],
            '9': [cv2.imread('cards\\9.png')],
            'T': [cv2.imread('cards\\T.png')],
            'J': [cv2.imread('cards\\J.png'),cv2.imread('cards\\Jh.png')],
            'Q': [cv2.imread('cards\\Q.png')],
            'K': [cv2.imread('cards\\K.png')],
            'A': [cv2.imread('cards\\A.png')]
                 }
        for key,value in cards.items():
            for png in value:
                if np.all(png == first_hand):
                    print('Первая рука '+key)
        for key,value in cards.items():
            for png in value:
                if np.all(png == second_hand):
                    print('Вторая рука ' + key)

        cv2.imshow('screen1', first_hand)
        cv2.imshow('screen2',second_hand)
        if cv2.waitKey(1)== ord('w'):
            count += 1
            h1 = str(count) + 'screen.png'
            #h2 = str(count) + 'f2.png'
            cv2.imwrite(h1, screen_num)
            #cv2.imwrite(h2, second_hand)
#     screen = ImageGrab.grab((rect[0],rect[1],rect[2],rect[3]))
#     screen_num = np.array(screen)
#     first_hand = screen_num[302:322,282:296]
#     for row in first_hand:
#         for pixel in row:
#                 pixel[pixel<255] = 0
#     cv2.imshow('screen2', first_hand)
            # if pixel == np.array([255,255,255]):
    #             first_hand[row][pixel] = np.array([0, 0, 0])
    #         else:
    #             first_hand[row][pixel] = np.array([255, 255, 255])
    # cv2.imshow('screen2', first_hand)
window_info = get_window_info()
root = tk.Tk()
combo = Combobox(root,width = 120)
btn = tk.Button(root,text = 'Ok',command = lambda :data_screen())
keys = []
for key in get_window_info():
    keys.append(key)
combo['values'] = keys
combo.pack(side = 'left')
btn.pack(side = 'left')
root.mainloop()
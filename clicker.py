#!/usr/bin/python3 env
import win32gui
import pyautogui

a, b, c = win32gui.GetCursorInfo()
x, y = c

while True:
    pyautogui.click(x, y)

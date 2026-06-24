import subprocess
import time
import pyautogui

pyautogui.FAILSAFE = False

FOLDER = r"C:\vpds_testcases"
VSCODE = r"C:\Users\B Yaswanth kumar\Downloads\Microsoft VS Code\Code.exe"

subprocess.Popen(["explorer", FOLDER])
time.sleep(3)

subprocess.Popen([VSCODE, FOLDER])
time.sleep(20)

pyautogui.hotkey('alt', 'tab')
time.sleep(1)
pyautogui.hotkey('super', 'up')
time.sleep(1)

pyautogui.hotkey('ctrl', 'shift', '`')
time.sleep(3)

pyautogui.write(r'type C:\vpds_testcases\result.txt', interval=0.05)
pyautogui.press('enter')
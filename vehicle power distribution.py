import subprocess
import time
import pyautogui
import os
import sys

FOLDER    = r"C:\vpds_testcases.py"
VSCODE    = r"C:\Users\B Yaswanth kumar\Downloads\Microsoft VS Code\Code.exe"
TEST_FILE = r"C:\vpds_testcases.py\testcases.py"
PYTHON    = sys.executable

if not os.path.isfile(VSCODE):
    print(f"VS Code not found:\n  {VSCODE}")
    sys.exit()

if not os.path.isdir(FOLDER):
    print(f"Folder not found:\n  {FOLDER}")
    sys.exit()

if not os.path.isfile(TEST_FILE):
    print(f"Test file not found:\n  {TEST_FILE}")
    sys.exit()

print("[Step 1] Opening folder...")
subprocess.Popen(["explorer", FOLDER])
time.sleep(2)

print("[Step 2] Opening VS Code...")
subprocess.Popen([VSCODE, FOLDER, TEST_FILE])
time.sleep(10)

print("[Step 3] Focusing VS Code window...")
pyautogui.click(700, 400)
time.sleep(2)

print("[Step 4] Opening VS Code terminal...")
pyautogui.hotkey('ctrl', '')
time.sleep(3)

print("[Step 5] Running g++ compile...")
g_cmd = r'cmd /c "cd /d C:\vpds_testcases.py && g++ vpds.cpp -o vpds_output.exe && vpds_output.exe"'
pyautogui.write(g_cmd, interval=0.03)
pyautogui.press('enter')
time.sleep(5)

print("[Step 6] Running Python tests...")
py_cmd = f'python "{TEST_FILE}"'
pyautogui.write(py_cmd, interval=0.03)
pyautogui.press('enter')

print("Done! Watch the VS Code terminal for test results.")

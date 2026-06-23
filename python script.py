import subprocess
import time
import pyautogui
import os
import sys

FOLDER  = r"C:\vpds_testcases"
VSCODE  = r"C:\Users\B Yaswanth kumar\Downloads\Microsoft VS Code\Code.exe"
CPP     = r"C:\vpds_testcases\vpds.cpp"

# --- Path checks ---
if not os.path.isfile(VSCODE):
    print("VS Code not found:", VSCODE)
    sys.exit()

if not os.path.isdir(FOLDER):
    print("Folder not found:", FOLDER)
    sys.exit()

if not os.path.isfile(CPP):
    print("CPP file not found:", CPP)
    sys.exit()

# Open folder in Explorer
subprocess.Popen(["explorer", FOLDER])
time.sleep(2)

# Compile and run in a CMD window
subprocess.Popen(
    [
        "cmd",
        "/k",
        r"cd /d C:\vpds_testcases && g++ vpds.cpp -o vpds_output.exe && vpds_output.exe"
    ]
)

# Open VS Code with folder and CPP file (only once)
subprocess.Popen([VSCODE, FOLDER, CPP])
time.sleep(5)

print("VS Code opening...")
time.sleep(15)

# Focus VS Code window
pyautogui.click(700, 400)
time.sleep(2)

# Open integrated terminal
pyautogui.hotkey('ctrl', '`')
time.sleep(3)

# Type compile + run command in VS Code terminal
cmd = r'cd C:\vpds_testcases; g++ vpds.cpp -o vpds_output.exe; .\vpds_output.exe'
pyautogui.write(cmd, interval=0.03)
pyautogui.press('enter')

time.sleep(10)
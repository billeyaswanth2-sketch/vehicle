"""
Vehicle Power Distribution - Test Runner
Author  : Yaswanth
Purpose :
    I.   Open Folder in Explorer
    II.  Open Test Cases in VS Code
    III. Run Test Cases in VS Code (new terminal)
"""

import subprocess
import time
import pyautogui
import os
import sys

# ---------------------------------------------------------------------------
# Paths
# ---------------------------------------------------------------------------

FOLDER = r"C:\vpds_testcases"
VSCODE = r"C:\Users\B Yaswanth kumar\Downloads\Microsoft VS Code\Code.exe"
CPP    = r"C:\vpds_testcases\vpds.cpp"

# ---------------------------------------------------------------------------
# Path Checks
# ---------------------------------------------------------------------------

print("=" * 55)
print("Vehicle Power Distribution - Test Runner")
print("=" * 55)

if not os.path.isfile(VSCODE):
    print(f"[ERROR] VS Code not found: {VSCODE}")
    sys.exit(1)

if not os.path.isdir(FOLDER):
    print(f"[ERROR] Folder not found: {FOLDER}")
    sys.exit(1)

if not os.path.isfile(CPP):
    print(f"[ERROR] CPP file not found: {CPP}")
    sys.exit(1)

print("[OK] VS Code found")
print("[OK] Folder found")
print("[OK] CPP file found")

# ---------------------------------------------------------------------------
# I. Open Folder in Explorer
# ---------------------------------------------------------------------------

print("\n[STEP 1] Opening folder in Explorer...")
subprocess.Popen(["explorer", FOLDER])
time.sleep(2)

# ---------------------------------------------------------------------------
# II. Open Test Cases in VS Code (only once)
# ---------------------------------------------------------------------------

print("[STEP 2] Opening VS Code with folder and CPP file...")
subprocess.Popen([VSCODE, FOLDER, CPP])
time.sleep(20)  # Wait for VS Code to fully load
print("[OK] VS Code opened!")

# ---------------------------------------------------------------------------
# III. Run Test Cases in VS Code (new terminal)
# ---------------------------------------------------------------------------

print("[STEP 3] Opening new terminal in VS Code...")

# Focus VS Code window safely
pyautogui.hotkey('alt', 'tab')
time.sleep(2)

# Open a NEW terminal in VS Code
pyautogui.hotkey('ctrl', 'shift', '`')
time.sleep(3)

# Type compile + run command
print("[INFO] Typing compile and run command...")
cmd = r'cd C:\vpds_testcases; g++ vpds.cpp -o vpds_output.exe; .\vpds_output.exe'
pyautogui.write(cmd, interval=0.05)
time.sleep(1)
pyautogui.press('enter')

print("\n[INFO] Test cases running in VS Code terminal...")
time.sleep(10)

print("\n" + "=" * 55)
print("Done! Check VS Code terminal for test results!")
print("=" * 55)
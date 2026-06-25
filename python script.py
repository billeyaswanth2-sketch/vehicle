"""
Vehicle Power Distribution - Test Runner
Author  : Yaswanth
Purpose :
    I.   Compile C++ Test Cases
    II.  Run Test Cases -> Save to result.txt
    III. Open Folder in Explorer
    IV.  Open VS Code
    V.   Show Results in VS Code New Terminal
"""
import subprocess
import time
import os
import sys
import pyautogui

# ---------------------------------------------------------------------------
# Disable pyautogui failsafe
# ---------------------------------------------------------------------------

pyautogui.FAILSAFE = False

# ---------------------------------------------------------------------------
# Paths
# ---------------------------------------------------------------------------

FOLDER = r"C:\vpds_testcases"
VSCODE = r"C:\Users\B Yaswanth kumar\Downloads\Microsoft VS Code\Code.exe"
CPP    = r"C:\vpds_testcases\testcases.cpp"
EXE    = r"C:\vpds_testcases\testcases.exe"
RESULT = r"C:\vpds_testcases\result.txt"

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
# I. Compile C++ Test Cases
# ---------------------------------------------------------------------------

print("\n[STEP 1] Compiling testcases.cpp...")
compile = subprocess.run(
    ["g++", CPP, "-o", EXE],
    capture_output=True,
    text=True
)

if compile.returncode != 0:
    print("[ERROR] Compilation FAILED!")
    print(compile.stderr)
    sys.exit(1)

print("[OK] Compilation SUCCESS!")

# ---------------------------------------------------------------------------
# II. Run Test Cases -> Save to result.txt
# ---------------------------------------------------------------------------

print("\n[STEP 2] Running test cases...")
with open(RESULT, "w") as f:
    run = subprocess.run(
        [EXE],
        stdout=f,
        stderr=f,
        text=True
    )

print("[OK] Test cases finished!")
print("[OK] Results saved to result.txt!")

# Print results to Jenkins Console
print("\n" + "=" * 55)
with open(RESULT, "r") as f:
    content = f.read()
    print(content)
print("=" * 55)

# ---------------------------------------------------------------------------
# III. Open Folder in Explorer
# ---------------------------------------------------------------------------

print("\n[STEP 3] Opening folder in Explorer...")
subprocess.Popen(["explorer", FOLDER])
time.sleep(3)
print("[OK] Folder opened!")

# ---------------------------------------------------------------------------
# IV. Open VS Code with Folder
# ---------------------------------------------------------------------------

print("\n[STEP 4] Opening VS Code...")
subprocess.Popen([VSCODE, FOLDER])
time.sleep(20)
print("[OK] VS Code opened!")

# ---------------------------------------------------------------------------
# V. Open New Terminal in VS Code and Show Results
# ---------------------------------------------------------------------------

print("\n[STEP 5] Opening new terminal in VS Code...")

# Focus VS Code window
pyautogui.hotkey('alt', 'tab')
time.sleep(2)

# Maximize VS Code window
pyautogui.hotkey('super', 'up')
time.sleep(1)

# Open NEW terminal
pyautogui.hotkey('ctrl', 'shift', '`')
time.sleep(3)

# Type command to show results in terminal
print("[INFO] Showing results in VS Code terminal...")
cmd = r'type C:\vpds_testcases\result.txt'
pyautogui.write(cmd, interval=0.05)
time.sleep(1)
pyautogui.press('enter')
time.sleep(3)

print("\n" + "=" * 55)
print("Done! Check VS Code terminal for results!")
print("=" * 55)

"""
Step 3: Python script to:
  I.   Open your folder path
  II.  Open test cases in VS Code
  III. Run testcases in VS Code (new terminal)

Target path: C:\\vpds_testcases.cpp
Adjust FOLDER_PATH / TEST_FILE / BUILD_DIR below to match your actual project layout.
"""

import os
import subprocess
import sys
import time

# ----------------------------
# CONFIG - edit these as needed
# ----------------------------
TEST_FILE = r"C:\vpds_testcases.cpp"
FOLDER_PATH = os.path.dirname(TEST_FILE)  # C:\
VSCODE_EXE = "code"  # assumes 'code' is on PATH; else give full path to Code.exe

# If your test cases are part of a CMake/GTest build (like vpd-project),
# set BUILD_DIR to the folder containing your CMake build output.
BUILD_DIR = r"C:\vpds_build"
TEST_EXECUTABLE = "run_tests.exe"


def step1_open_folder(folder_path: str):
    """I. Open your folder path (File Explorer)."""
    print(f"[Step 1] Opening folder: {folder_path}")
    if not os.path.isdir(folder_path):
        print(f"  WARNING: Folder does not exist: {folder_path}")
        return
    os.startfile(folder_path)  # Windows only


def step2_open_in_vscode(path: str):
    """II. Open test cases (file or folder) in VS Code."""
    print(f"[Step 2] Opening in VS Code: {path}")
    if not os.path.exists(path):
        print(f"  WARNING: Path does not exist: {path}")
        return
    try:
        subprocess.run([VSCODE_EXE, path], check=True, shell=True)
    except subprocess.CalledProcessError as e:
        print(f"  ERROR: Failed to open VS Code: {e}")
    except FileNotFoundError:
        print("  ERROR: 'code' command not found. Add VS Code to PATH "
              "or set VSCODE_EXE to the full path of Code.exe")


def step3_run_tests_new_terminal(build_dir: str, test_exe: str):
    """III. Run testcases in VS Code's new integrated terminal."""
    print(f"[Step 3] Running testcases from: {build_dir}\\{test_exe}")

    exe_path = os.path.join(build_dir, test_exe)
    if not os.path.isfile(exe_path):
        print(f"  WARNING: Test executable not found: {exe_path}")
        print("  Skipping run step. Build it first, e.g.:")
        print(f"    cmake -S . -B \"{build_dir}\" -G \"MinGW Makefiles\"")
        print(f"    cmake --build \"{build_dir}\"")
        return

    # Use VS Code's command-line interface to open a new terminal and run the command.
    # `code -r` reuses the current window; the terminal command is sent via the
    # integrated terminal using the 'workbench.action.terminal.new' trick below,
    # OR simplest: just open a cmd window running the test (separate from VS Code panel).
    cmd = f'cd /d "{build_dir}" && "{test_exe}" --gtest_output=xml:test_results.xml'
    print(f"  Launching new terminal with command:\n    {cmd}")

    # Opens a new terminal window (cmd.exe) and runs the tests.
    subprocess.Popen(f'start "Run VPD Tests" cmd /k "{cmd}"', shell=True)


def main():
    step1_open_folder(FOLDER_PATH)
    time.sleep(1)

    step2_open_in_vscode(TEST_FILE)
    time.sleep(1)

    step3_run_tests_new_terminal(BUILD_DIR, TEST_EXECUTABLE)


if __name__ == "__main__":
    if sys.platform != "win32":
        print("This script uses Windows-specific calls (os.startfile, 'start' command) "
              "and is intended to run on Windows.")
    main()
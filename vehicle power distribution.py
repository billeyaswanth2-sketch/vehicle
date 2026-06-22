import subprocess
import sys

FOLDER    = r"C:\vpds_testcases.py"
TEST_FILE = r"C:\vpds_testcases.py\testcases.py"

print("[Step 1] Compiling C++...")
subprocess.run(["g++", "vpds.cpp", "-o", "vpds_output.exe"], cwd=FOLDER, check=True)

print("[Step 2] Running C++ program...")
subprocess.run([r"C:\vpds_testcases.py\vpds_output.exe"], cwd=FOLDER, check=True)

print("[Step 3] Running Python tests...")
subprocess.run([sys.executable, TEST_FILE], cwd=FOLDER, check=True)

print("Done!")

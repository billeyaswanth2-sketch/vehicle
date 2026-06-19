"""
Vehicle Power Distribution - Test Module
Converted from CAPL to Python
 
Original: CANoe CAPL test script
Author  : Yaswanth
Target  : Can be run with pytest, or adapted for CANoe COM API / python-can
 
SysVar namespace mapping (CAPL → Python dict keys):
  sysvar::ignition::ignition  →  sys_vars["ignition"]
  sysvar::brake::brake        →  sys_vars["brake"]
  sysvar::gear::gear          →  sys_vars["gear"]
  sysvar::engine::engine      →  sys_vars["engine"]
 
To integrate with real CANoe COM API, replace SysVarSimulator with
a wrapper around win32com.client.Dispatch("CANoe.Application").
"""
 
import time
import pytest
 
# ---------------------------------------------------------------------------
# Minimal SysVar simulator (replaces CANoe environment variables)
# ---------------------------------------------------------------------------
 
class SysVarSimulator:
    """
    Simulates CANoe system variables.
    In a real CANoe setup, swap this out for COM API calls:
        app  = win32com.client.Dispatch("CANoe.Application")
        env  = app.Environment
        var  = env.GetVariable("ignition::ignition")
        var.Value = 1
    """
 
    def __init__(self):
        self._vars: dict = {
            "ignition": 0,
            "brake"   : 1,   # pre-set to 1 (brake pressed by default)
            "gear"    : 0,
            "engine"  : 0,
        }
 
    def set(self, name: str, value: int) -> None:
        self._vars[name] = value
 
    def get(self, name: str) -> int:
        return self._vars[name]
 
    def wait_for_sysvar(self, name: str, timeout_ms: int) -> int:
        """
        Returns 1 if the variable is accessible (always in simulation).
        In a real environment this would block until the variable changes
        or the timeout expires, returning 0 on timeout.
        """
        time.sleep(timeout_ms / 1000.0 * 0.01)   # tiny sim delay
        return 1   # 1 = received, 0 = timeout
 
 
# ---------------------------------------------------------------------------
# Test report helper (mirrors CAPL testStepPass / testStepFail)
# ---------------------------------------------------------------------------
 
class TestReport:
    def __init__(self, module_title: str, description: str, engineer: str):
        self.module_title = module_title
        self.description  = description
        self.engineer     = engineer
        self.results: list[dict] = []
 
    def step_pass(self, step: str, message: str) -> None:
        self.results.append({"step": step, "status": "PASS", "msg": message})
        print(f"  [PASS] {step}: {message}")
 
    def step_fail(self, step: str, message: str) -> None:
        self.results.append({"step": step, "status": "FAIL", "msg": message})
        print(f"  [FAIL] {step}: {message}")
 
    def summary(self) -> None:
        passed = sum(1 for r in self.results if r["status"] == "PASS")
        failed = sum(1 for r in self.results if r["status"] == "FAIL")
        print(f"\n{'='*55}")
        print(f"Module : {self.module_title}")
        print(f"Eng    : {self.engineer}")
        print(f"Total  : {len(self.results)}  |  Pass: {passed}  |  Fail: {failed}")
        print(f"{'='*55}")
 
 
# ---------------------------------------------------------------------------
# Constants (mirroring CAPL variables block)
# ---------------------------------------------------------------------------
 
WAIT_TIMEOUT_MS = 500
 
 
# ---------------------------------------------------------------------------
# Test cases
# ---------------------------------------------------------------------------
 
def tc_brake(sv: SysVarSimulator, report: TestReport) -> None:
    """
    Testcase: tc_brake
    Verifies that setting the brake sysvar to 1 is acknowledged correctly.
    """
    print("\n[TC] brake_test")
 
    # Step 1 – set brake = 1
    sv.set("brake", 1)
    wait_result = sv.wait_for_sysvar("brake", WAIT_TIMEOUT_MS)
 
    if wait_result == 0:
        report.step_fail("test step1", "sys var is not received")
    else:
        if sv.get("brake") == 1:
            report.step_pass("test step1", "brake is working fine")
        else:
            report.step_fail("test step1", "brake is not working")
 
    time.sleep(WAIT_TIMEOUT_MS / 1000.0)
 
 
def tc_gear(sv: SysVarSimulator, report: TestReport) -> None:
    """
    Testcase: tc_gear
    Validates gear positions 0-5 (Park, Reverse, Neutral, Drive, 3rd, 2nd).
    """
    print("\n[TC] gear_test")
 
    gear_steps = [
        (0, "gear is in Park / Neutral"),
        (1, "gear 1 is activated"),
        (2, "gear 2 is activated"),
        (3, "gear 3 is activated"),
        (4, "gear 4 is activated"),
        (5, "gear 5 is activated"),
    ]
 
    for step_num, (gear_val, pass_msg) in enumerate(gear_steps, start=1):
        step_label = f"test step{step_num}"
        sv.set("gear", gear_val)
        wait_result = sv.wait_for_sysvar("gear", WAIT_TIMEOUT_MS)
 
        if wait_result == 0:
            report.step_fail(step_label, "sys var is not received")
        else:
            if sv.get("gear") == gear_val:
                report.step_pass(step_label, pass_msg)
            else:
                report.step_fail(step_label, "gear is not working")
 
        time.sleep(WAIT_TIMEOUT_MS / 1000.0)
 
 
def tc_ignition_key(sv: SysVarSimulator, report: TestReport) -> None:
    """
    Testcase: tc_ignition_key
    Tests all four ignition key positions:
      0 = Lock, 1 = Accessory, 2 = ON, 3 = Start
    For position 3 (Start) the engine sysvar is set to 1 on pass,
    and gear must be 0 + brake must be 1 (safety interlock).
    """
    print("\n[TC] ignition_test")
 
    ignition_steps = [
        (0, "key is in lock mode",      "key is not working"),
        (1, "key is in accessory mode", "key is not working"),
        (2, "key is in ON mode",        "key is not working"),
    ]
 
    for step_num, (ign_val, pass_msg, fail_msg) in enumerate(ignition_steps, start=1):
        step_label = f"test step{step_num}"
        sv.set("ignition", ign_val)
        wait_result = sv.wait_for_sysvar("ignition", WAIT_TIMEOUT_MS)
 
        if wait_result == 0:
            report.step_fail(step_label, "sys var is not received")
        else:
            if sv.get("ignition") == ign_val:
                report.step_pass(step_label, pass_msg)
            else:
                report.step_fail(step_label, fail_msg)
 
        time.sleep(WAIT_TIMEOUT_MS / 1000.0)
 
    # Step 4 – Start (ignition = 3), requires brake=1 and gear=0
    sv.set("gear", 0)
    sv.set("ignition", 3)
    wait_result = sv.wait_for_sysvar("ignition", WAIT_TIMEOUT_MS)
 
    if wait_result == 0:
        report.step_fail("test step4", "sys var is not received")
    else:
        ign_ok   = sv.get("ignition") == 3
        brake_ok = sv.get("brake")    == 1
        gear_ok  = sv.get("gear")     == 0
 
        if ign_ok and brake_ok and gear_ok:
            report.step_pass("test step4", "key is in start mode")
            sv.set("engine", 1)        # engine cranks
        else:
            report.step_fail("test step4", "key is not working")
 
    time.sleep(WAIT_TIMEOUT_MS / 1000.0)
 
 
# ---------------------------------------------------------------------------
# Main test module (mirrors CAPL maintest())
# ---------------------------------------------------------------------------
 
def main_test() -> TestReport:
    print("=" * 55)
    print("Module : vehicle power distribution")
    print("Desc   : test cases are written in Python (converted from CAPL)")
    print("Eng    : Yaswanth")
    print("=" * 55)
 
    sv     = SysVarSimulator()
    report = TestReport(
        module_title="vehicle power distribution",
        description ="test cases are written in Python (converted from CAPL)",
        engineer    ="Yaswanth",
    )
 
    time.sleep(0.4)   # testWaitForTimeout(400)
 
    print("\n--- Group: simulation of signals / test mode communication ---")
 
    tc_brake(sv, report)
    tc_gear(sv, report)
    tc_ignition_key(sv, report)
 
    time.sleep(WAIT_TIMEOUT_MS / 1000.0)
 
    report.summary()
    return report
 
 
# ---------------------------------------------------------------------------
# pytest entry points (one test function per CAPL testcase)
# ---------------------------------------------------------------------------
 
@pytest.fixture(scope="module")
def shared_env():
    """Shared SysVarSimulator and report across all test functions."""
    sv     = SysVarSimulator()
    report = TestReport("vehicle power distribution", "", "Yaswanth")
    yield sv, report
    report.summary()
 
 
def test_brake(shared_env):
    sv, report = shared_env
    before = len(report.results)
    tc_brake(sv, report)
    failures = [r for r in report.results[before:] if r["status"] == "FAIL"]
    assert not failures, f"Brake test failures: {failures}"
 
 
def test_gear(shared_env):
    sv, report = shared_env
    before = len(report.results)
    tc_gear(sv, report)
    failures = [r for r in report.results[before:] if r["status"] == "FAIL"]
    assert not failures, f"Gear test failures: {failures}"
 
 
def test_ignition_key(shared_env):
    sv, report = shared_env
    before = len(report.results)
    tc_ignition_key(sv, report)
    failures = [r for r in report.results[before:] if r["status"] == "FAIL"]
    assert not failures, f"Ignition test failures: {failures}"
 
 
# ---------------------------------------------------------------------------
# Direct execution
# ---------------------------------------------------------------------------
 
if __name__ == "__main__":
    main_test()
 
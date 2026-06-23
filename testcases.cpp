/**
 * Vehicle Power Distribution - Test Module
 * Converted from Python/CAPL to C++  (plain g++, no external libraries)
 *
 * Author  : Yaswanth
 * Compiler: g++ -std=c++17 vpds.cpp -o vpds_output.exe
 *
 * SysVar namespace mapping (CAPL -> C++ map keys):
 *   sysvar::ignition::ignition  ->  vars_["ignition"]
 *   sysvar::brake::brake        ->  vars_["brake"]
 *   sysvar::gear::gear          ->  vars_["gear"]
 *   sysvar::engine::engine      ->  vars_["engine"]
 */

#include <chrono>
#include <iostream>
#include <map>
#include <string>
#include <thread>
#include <vector>

// ---------------------------------------------------------------------------
// Constants
// ---------------------------------------------------------------------------

constexpr int WAIT_TIMEOUT_MS = 500;

// ---------------------------------------------------------------------------
// SysVar Simulator (replaces CANoe environment variables)
// ---------------------------------------------------------------------------

class SysVarSimulator {
public:
    SysVarSimulator() {
        vars_["ignition"] = 0;
        vars_["brake"]    = 1;   // brake pressed by default
        vars_["gear"]     = 0;
        vars_["engine"]   = 0;
    }

    void set(const std::string& name, int value) {
        vars_[name] = value;
    }

    int get(const std::string& name) const {
        auto it = vars_.find(name);
        if (it != vars_.end()) return it->second;
        return -1;
    }

    // Returns 1 = received, 0 = timeout (always 1 in simulation)
    int waitForSysVar(const std::string& /*name*/, int timeout_ms) {
        std::this_thread::sleep_for(
            std::chrono::milliseconds(timeout_ms / 100));
        return 1;
    }

private:
    std::map<std::string, int> vars_;
};

// ---------------------------------------------------------------------------
// Test Report (mirrors CAPL testStepPass / testStepFail)
// ---------------------------------------------------------------------------

struct StepResult {
    std::string step;
    std::string status;   // "PASS" or "FAIL"
    std::string msg;
};

class TestReport {
public:
    TestReport(const std::string& module_title,
               const std::string& engineer)
        : module_title_(module_title), engineer_(engineer) {}

    void stepPass(const std::string& step, const std::string& msg) {
        results_.push_back({step, "PASS", msg});
        std::cout << "  [PASS] " << step << ": " << msg << "\n";
    }

    void stepFail(const std::string& step, const std::string& msg) {
        results_.push_back({step, "FAIL", msg});
        std::cout << "  [FAIL] " << step << ": " << msg << "\n";
    }

    void summary() const {
        int passed = 0, failed = 0;
        for (const auto& r : results_) {
            if (r.status == "PASS") ++passed;
            else                    ++failed;
        }
        std::cout << "\n" << std::string(55, '=') << "\n";
        std::cout << "Module : " << module_title_ << "\n";
        std::cout << "Eng    : " << engineer_     << "\n";
        std::cout << "Total  : " << results_.size()
                  << "  |  Pass: " << passed
                  << "  |  Fail: " << failed << "\n";
        std::cout << std::string(55, '=') << "\n";
    }

    const std::vector<StepResult>& results() const { return results_; }

private:
    std::string             module_title_;
    std::string             engineer_;
    std::vector<StepResult> results_;
};

// ---------------------------------------------------------------------------
// Simple Test Runner
// ---------------------------------------------------------------------------

struct TestCase {
    std::string name;
    bool        passed;
    std::string failure_msg;
};

static std::vector<TestCase> g_test_results;

static void register_test(const std::string& name,
                          const std::vector<StepResult>& all_results,
                          size_t before) {
    std::vector<std::string> fails;
    for (size_t i = before; i < all_results.size(); ++i) {
        if (all_results[i].status == "FAIL")
            fails.push_back(all_results[i].msg);
    }

    if (fails.empty()) {
        g_test_results.push_back({name, true, ""});
        std::cout << "\n[  OK  ] " << name << "\n";
    } else {
        g_test_results.push_back({name, false, fails[0]});
        std::cout << "\n[ FAIL ] " << name << " => " << fails[0] << "\n";
    }
}

// ---------------------------------------------------------------------------
// TC1: Brake Test
// Verifies brake sysvar = 1 is acknowledged correctly.
// ---------------------------------------------------------------------------

static void tc_brake(SysVarSimulator& sv, TestReport& report) {
    std::cout << "\n[TC] brake_test\n";

    sv.set("brake", 1);
    int result = sv.waitForSysVar("brake", WAIT_TIMEOUT_MS);

    if (result == 0) {
        report.stepFail("test step1", "sys var is not received");
    } else {
        if (sv.get("brake") == 1)
            report.stepPass("test step1", "brake is working fine");
        else
            report.stepFail("test step1", "brake is not working");
    }

    std::this_thread::sleep_for(std::chrono::milliseconds(WAIT_TIMEOUT_MS));
}

// ---------------------------------------------------------------------------
// TC2: Gear Test
// Validates gear positions 0-5.
//   0 = Park/Neutral, 1-5 = gear positions
// ---------------------------------------------------------------------------

static void tc_gear(SysVarSimulator& sv, TestReport& report) {
    std::cout << "\n[TC] gear_test\n";

    struct GearStep { int value; std::string pass_msg; };

    const std::vector<GearStep> gear_steps = {
        {0, "gear is in Park / Neutral"},
        {1, "gear 1 is activated"},
        {2, "gear 2 is activated"},
        {3, "gear 3 is activated"},
        {4, "gear 4 is activated"},
        {5, "gear 5 is activated"},
    };

    int step_num = 1;
    for (const auto& gs : gear_steps) {
        std::string label = "test step" + std::to_string(step_num++);
        sv.set("gear", gs.value);
        int result = sv.waitForSysVar("gear", WAIT_TIMEOUT_MS);

        if (result == 0) {
            report.stepFail(label, "sys var is not received");
        } else {
            if (sv.get("gear") == gs.value)
                report.stepPass(label, gs.pass_msg);
            else
                report.stepFail(label, "gear is not working");
        }

        std::this_thread::sleep_for(std::chrono::milliseconds(WAIT_TIMEOUT_MS));
    }
}

// ---------------------------------------------------------------------------
// TC3: Ignition Key Test
// Tests all 4 ignition positions:
//   0 = Lock, 1 = Accessory, 2 = ON, 3 = Start
// Start requires: brake=1 AND gear=0 (safety interlock)
// ---------------------------------------------------------------------------

static void tc_ignition_key(SysVarSimulator& sv, TestReport& report) {
    std::cout << "\n[TC] ignition_test\n";

    struct IgnStep { int value; std::string pass_msg; std::string fail_msg; };

    const std::vector<IgnStep> ignition_steps = {
        {0, "key is in lock mode",      "key is not working"},
        {1, "key is in accessory mode", "key is not working"},
        {2, "key is in ON mode",        "key is not working"},
    };

    int step_num = 1;
    for (const auto& ig : ignition_steps) {
        std::string label = "test step" + std::to_string(step_num++);
        sv.set("ignition", ig.value);
        int result = sv.waitForSysVar("ignition", WAIT_TIMEOUT_MS);

        if (result == 0) {
            report.stepFail(label, "sys var is not received");
        } else {
            if (sv.get("ignition") == ig.value)
                report.stepPass(label, ig.pass_msg);
            else
                report.stepFail(label, ig.fail_msg);
        }

        std::this_thread::sleep_for(std::chrono::milliseconds(WAIT_TIMEOUT_MS));
    }

    // Step 4 - Start: ignition=3, requires brake=1 and gear=0
    sv.set("gear",     0);
    sv.set("ignition", 3);
    int result = sv.waitForSysVar("ignition", WAIT_TIMEOUT_MS);

    if (result == 0) {
        report.stepFail("test step4", "sys var is not received");
    } else {
        bool ign_ok   = sv.get("ignition") == 3;
        bool brake_ok = sv.get("brake")    == 1;
        bool gear_ok  = sv.get("gear")     == 0;

        if (ign_ok && brake_ok && gear_ok) {
            report.stepPass("test step4", "key is in start mode");
            sv.set("engine", 1);   // engine cranks
        } else {
            report.stepFail("test step4", "key is not working");
        }
    }

    std::this_thread::sleep_for(std::chrono::milliseconds(WAIT_TIMEOUT_MS));
}

// ---------------------------------------------------------------------------
// Test runners (one per test case)
// ---------------------------------------------------------------------------

static void run_brake_test(SysVarSimulator& sv, TestReport& report) {
    size_t before = report.results().size();
    tc_brake(sv, report);
    register_test("VpdTest.BrakeTest", report.results(), before);
}

static void run_gear_test(SysVarSimulator& sv, TestReport& report) {
    size_t before = report.results().size();
    tc_gear(sv, report);
    register_test("VpdTest.GearTest", report.results(), before);
}

static void run_ignition_test(SysVarSimulator& sv, TestReport& report) {
    size_t before = report.results().size();
    tc_ignition_key(sv, report);
    register_test("VpdTest.IgnitionKeyTest", report.results(), before);
}

// ---------------------------------------------------------------------------
// main
// ---------------------------------------------------------------------------

int main() {
    std::cout << std::string(55, '=') << "\n";
    std::cout << "Module : Vehicle Power Distribution\n";
    std::cout << "Desc   : Test cases written in C++ (converted from CAPL)\n";
    std::cout << "Eng    : Yaswanth\n";
    std::cout << std::string(55, '=') << "\n";

    std::this_thread::sleep_for(std::chrono::milliseconds(400));
    std::cout << "\n--- Group: simulation of signals / test mode communication ---\n";

    SysVarSimulator sv;
    TestReport report("Vehicle Power Distribution", "Yaswanth");

    // Run all 3 test cases
    run_brake_test    (sv, report);
    run_gear_test     (sv, report);
    run_ignition_test (sv, report);

    // Per-step summary
    report.summary();

    // Overall test runner summary
    int passed = 0, failed = 0;
    std::cout << "\n--- Test Runner Summary ---\n";
    for (const auto& tc : g_test_results) {
        std::cout << (tc.passed ? "[  OK  ] " : "[ FAIL ] ") << tc.name;
        if (!tc.passed) std::cout << "  =>  " << tc.failure_msg;
        std::cout << "\n";
        if (tc.passed) ++passed; else ++failed;
    }
    std::cout << "\nTests run: " << g_test_results.size()
              << "  |  Passed: " << passed
              << "  |  Failed: " << failed << "\n";

    return (failed == 0) ? 0 : 1;
}
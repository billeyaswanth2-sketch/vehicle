#include <iostream>
using namespace std;

int main() {

    cout << "=======================================================" << endl;
    cout << "Module : vehicle power distribution (C++)"              << endl;
    cout << "Eng    : Yaswanth"                                       << endl;
    cout << "=======================================================" << endl;

    int brake = 1;
    cout << "[TC] brake_test" << endl;
    if (brake == 1)
        cout << "  [PASS] brake is working fine" << endl;
    else
        cout << "  [FAIL] brake is not working" << endl;

    int gear = 0;
    cout << "[TC] gear_test" << endl;
    if (gear == 0)
        cout << "  [PASS] gear is in Park / Neutral" << endl;
    else
        cout << "  [FAIL] gear test failed" << endl;

    int key = 0;
    cout << "[TC] ignition_test" << endl;
    if (key == 0)
        cout << "  [PASS] key is in lock mode" << endl;
    else
        cout << "  [FAIL] ignition test failed" << endl;

    cout << "=======================================================" << endl;
    cout << "Done!" << endl;
    cout << "=======================================================" << endl;

    return 0;
}

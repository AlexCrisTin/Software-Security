// ============================================================================
// lock2_buggy.cpp
// He thong khoa cua thong minh - PHIEN BAN CO LOI (dung enum, khop style
// voi lock2.cpp / lock.py / lock_buggy.py de bo 3 ngon ngu dong bo nhau)
//
// LOI THIET KE CO Y (giong het lock_buggy.py):
//   Trong step(), khi action == ACTION_SUBMIT_PIN, he thong VAN so sanh
//   entered_pin voi correct_pin va tang failed_attempts neu sai, nhung
//   KHONG dung ket qua so sanh do de quyet dinh trang thai tiep theo.
//   Ca 2 nhanh (dung/sai) deu ket thuc o STATE_UNLOCKED.
//
//   => Vi pham thuoc tinh safety: "Khong bao gio o UNLOCKED neu PIN
//      nhap vao khong khop correct_pin".
// ============================================================================

#include <iostream>
#include <string>

enum LockState {
    STATE_LOCKED,
    STATE_UNLOCKING,
    STATE_UNLOCKED,
    STATE_ALARM
};

enum Action {
    ACTION_PRESS_DIGIT,
    ACTION_SUBMIT_PIN,
    ACTION_CANCEL,
    ACTION_LOCK_DOOR,
    ACTION_ADMIN_RESET
};

struct AtomicPropositions {
    bool is_locked;
    bool is_unlocking;
    bool is_unlocked;
    bool is_alarm;
    bool has_failed_max;
};

class SmartLock {
private:
    LockState state;
    std::string correct_pin;
    std::string entered_pin;
    int failed_attempts;
    int max_attempts;

public:
    SmartLock(const std::string& pin = "1234", int max_tries = 3)
        : correct_pin(pin), max_attempts(max_tries) {
        reset();
    }

    void reset() {
        state = STATE_LOCKED;
        failed_attempts = 0;
        entered_pin = "";
    }

    LockState getState() const {
        return state;
    }

    int getFailedAttempts() const {
        return failed_attempts;
    }

    AtomicPropositions getAtomicPropositions() const {
        return {
            state == STATE_LOCKED,
            state == STATE_UNLOCKING,
            state == STATE_UNLOCKED,
            state == STATE_ALARM,
            failed_attempts >= max_attempts
        };
    }

    void step(Action action, char digit = '\0') {
        switch (state) {
            case STATE_LOCKED:
                if (action == ACTION_PRESS_DIGIT && digit != '\0') {
                    state = STATE_UNLOCKING;
                    entered_pin = digit;
                }
                break;

            case STATE_UNLOCKING:
                if (action == ACTION_PRESS_DIGIT && digit != '\0') {
                    entered_pin += digit;
                } else if (action == ACTION_SUBMIT_PIN) {
                    bool pin_correct = (entered_pin == correct_pin);

                    if (!pin_correct) {
                        failed_attempts++;
                    }

                    // --- LOI: thieu dieu kien "if (pin_correct)" tai day ---
                    // Dang le phai la:
                    //   if (pin_correct) {
                    //       state = STATE_UNLOCKED;
                    //       failed_attempts = 0;
                    //   } else if (failed_attempts >= max_attempts) {
                    //       state = STATE_ALARM;
                    //   } else {
                    //       state = STATE_LOCKED;
                    //   }
                    // Nhung code hien tai luon luon mo khoa, bat ke pin_correct:
                    entered_pin = "";
                    state = STATE_UNLOCKED;
                } else if (action == ACTION_CANCEL) {
                    entered_pin = "";
                    state = STATE_LOCKED;
                }
                break;

            case STATE_UNLOCKED:
                if (action == ACTION_LOCK_DOOR) {
                    state = STATE_LOCKED;
                }
                break;

            case STATE_ALARM:
                if (action == ACTION_ADMIN_RESET) {
                    reset();
                }
                break;
        }
    }
};

std::string stateToString(LockState s) {
    switch (s) {
        case STATE_LOCKED: return "LOCKED";
        case STATE_UNLOCKING: return "UNLOCKING";
        case STATE_UNLOCKED: return "UNLOCKED";
        case STATE_ALARM: return "ALARM";
    }
    return "UNKNOWN";
}

int main() {
    std::cout << "=== DEMO: Smart Lock lock2_buggy.cpp ===" << std::endl << std::endl;

    SmartLock lock("1234", 3);
    std::cout << "Trang thai ban dau: " << stateToString(lock.getState()) << std::endl;

    // Ke tan cong nhap PIN sai hoan toan: "9999"
    std::cout << std::endl << "--- Nhap PIN SAI hoan toan: \"9999\" ---" << std::endl;
    lock.step(ACTION_PRESS_DIGIT, '9');
    lock.step(ACTION_PRESS_DIGIT, '9');
    lock.step(ACTION_PRESS_DIGIT, '9');
    lock.step(ACTION_PRESS_DIGIT, '9');
    lock.step(ACTION_SUBMIT_PIN);
    std::cout << "Sau khi nhap SAI PIN '9999': " << stateToString(lock.getState())
              << " | Failed count = " << lock.getFailedAttempts() << std::endl;

    if (lock.getState() == STATE_UNLOCKED) {
        std::cout << std::endl;
        std::cout << "*** LO HONG XAC NHAN: cua da MO du nhap sai PIN! ***" << std::endl;
        std::cout << "    Day la counterexample doi chieu voi lock2.cpp (ban dung)" << std::endl;
        std::cout << "    va lock_buggy.py (ban Python tuong ung)." << std::endl;
    }

    return 0;
}

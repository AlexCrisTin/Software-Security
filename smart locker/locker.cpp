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
                    if (entered_pin == correct_pin) {
                        state = STATE_UNLOCKED;
                        failed_attempts = 0;
                        entered_pin = "";
                    } else {
                        failed_attempts++;
                        entered_pin = "";
                        if (failed_attempts >= max_attempts) {
                            state = STATE_ALARM;
                        } else {
                            state = STATE_LOCKED;
                        }
                    }
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
    SmartLock lock("1234", 3);
    std::cout << "Trang thai ban dau: " << stateToString(lock.getState()) << std::endl;

    lock.step(ACTION_PRESS_DIGIT, '1');
    lock.step(ACTION_PRESS_DIGIT, '2');
    lock.step(ACTION_PRESS_DIGIT, '3');
    lock.step(ACTION_PRESS_DIGIT, '4');
    lock.step(ACTION_SUBMIT_PIN);
    std::cout << "Sau khi nhap dung PIN 1234: " << stateToString(lock.getState()) << std::endl;

    lock.step(ACTION_LOCK_DOOR);
    std::cout << "Sau khi khoa: " << stateToString(lock.getState()) << std::endl;

    for (int i = 1; i <= 3; ++i) {
        lock.step(ACTION_PRESS_DIGIT, '9');
        lock.step(ACTION_SUBMIT_PIN);
        std::cout << "Lan sai thu " << i << ": State = " << stateToString(lock.getState())
                  << ", Failed count = " << lock.getFailedAttempts() << std::endl;
    }

    lock.step(ACTION_ADMIN_RESET);
    std::cout << "Sau admin reset: " << stateToString(lock.getState()) << std::endl;

    return 0;
}
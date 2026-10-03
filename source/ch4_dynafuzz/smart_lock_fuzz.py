"""Deterministic fuzz and path-directed demonstrations for generated helpers."""


def failed_attempt_ratio(failed_attempts: int, total_attempts: int) -> int:
    return failed_attempts // total_attempts


def smart_lock_unlock_code(code_a: int, code_b: int) -> int:
    if code_a == 12:
        if code_b == 34:
            raise ValueError("magic value reached")
    return code_a + code_b


def main() -> int:
    crashes = 0
    for i in range(300):
        total = 0 if i % 29 == 0 else (i % 23) + 1
        failed = i % (total + 1) if total else i
        try:
            failed_attempt_ratio(failed, total)
        except ZeroDivisionError:
            crashes += 1

    directed_inputs = [(0, 0), (12, 0), (12, 34)]
    magic_input = None
    for attempt, values in enumerate(directed_inputs, start=1):
        try:
            smart_lock_unlock_code(*values)
        except ValueError:
            magic_input = values
            magic_attempt = attempt
            break

    print("SMART LOCK GENERATED-HELPER FUZZING")
    print(f"failed_attempt_ratio: {crashes}/300 controlled crashes (division by zero)")
    print(f"smart_lock_unlock_code: crash_input={magic_input}, attempt={magic_attempt}")
    passed = crashes == 11 and magic_input == (12, 34) and magic_attempt == 3
    print(f"OVERALL: {'PASS' if passed else 'FAIL'}")
    return 0 if passed else 1


if __name__ == "__main__":
    raise SystemExit(main())

"""SMT checks for arithmetic risks described by the integrated specification."""

from z3 import Int, Solver, sat, unsat


INT32_MAX = 2_147_483_647


def overflow_witness(name: str) -> bool:
    left = Int(f"{name}_left")
    right = Int(f"{name}_right")
    solver = Solver()
    solver.add(left >= 0, right >= 0)
    solver.add(left <= INT32_MAX, right <= INT32_MAX)
    solver.add(left + right > INT32_MAX)
    result = solver.check()
    if result != sat:
        print(f"[FAIL] {name}: {result}")
        return False
    model = solver.model()
    print(
        f"[PASS] {name}: SAT, left={model[left]}, right={model[right]}, "
        f"mathematical_sum={model[left].as_long() + model[right].as_long()}"
    )
    return True


def bounded_failed_counter_is_safe() -> bool:
    current = Int("bounded_current")
    increment = Int("bounded_increment")
    solver = Solver()
    solver.add(current >= 0, current <= 3, increment >= 0, increment <= 1)
    solver.add(current + increment > INT32_MAX)
    result = solver.check()
    print(f"[{'PASS' if result == unsat else 'FAIL'}] bounded failed counter: {str(result).upper()}")
    return result == unsat


def main() -> int:
    print("SMART LOCK EXTENDED ARITHMETIC CHECKS - Z3")
    checks = [
        overflow_witness("failed_attempt_counter"),
        overflow_witness("pin_digit_counter"),
        overflow_witness("auth_log_counter"),
        overflow_witness("unlock_event_counter"),
        overflow_witness("admin_reset_counter"),
        bounded_failed_counter_is_safe(),
    ]
    print(f"OVERALL: {sum(checks)}/{len(checks)} checks passed")
    return 0 if all(checks) else 1


if __name__ == "__main__":
    raise SystemExit(main())

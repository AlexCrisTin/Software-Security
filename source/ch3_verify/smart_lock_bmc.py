"""Bounded Model Checking for the smart-lock report.

The model is the product of controller state, failed-attempt counter and an
authentication flag.  Z3 is used for the SAT/UNSAT results printed below.
"""

from __future__ import annotations

from collections import deque
from dataclasses import dataclass
from typing import Dict, Iterable, List, Tuple

from z3 import And, Bool, BoolVal, Int, Not, Or, Solver, sat, unsat, get_version_string


LOCKED, UNLOCKING, UNLOCKED, ALARM = range(4)
PRESS_DIGIT, SUBMIT_CORRECT, SUBMIT_WRONG, CANCEL, LOCK_DOOR, ADMIN_RESET = range(6)

STATE_NAME = {
    LOCKED: "LOCKED",
    UNLOCKING: "UNLOCKING",
    UNLOCKED: "UNLOCKED",
    ALARM: "ALARM",
}
ACTION_NAME = {
    PRESS_DIGIT: "PRESS_DIGIT",
    SUBMIT_CORRECT: "SUBMIT_CORRECT",
    SUBMIT_WRONG: "SUBMIT_WRONG",
    CANCEL: "CANCEL",
    LOCK_DOOR: "LOCK_DOOR",
    ADMIN_RESET: "ADMIN_RESET",
}


@dataclass
class PathVars:
    state: List
    failed: List
    authenticated: List
    action: List


def _domain_constraints(v: PathVars, k: int):
    constraints = []
    for i in range(k + 1):
        constraints.extend(
            [v.state[i] >= LOCKED, v.state[i] <= ALARM,
             v.failed[i] >= 0, v.failed[i] <= 3]
        )
    for i in range(k):
        constraints.extend([v.action[i] >= PRESS_DIGIT, v.action[i] <= ADMIN_RESET])
    return constraints


def _transition(q, f, auth, action, qn, fn, authn, *, buggy: bool):
    locked_cases = [
        And(q == LOCKED, action == PRESS_DIGIT,
            qn == UNLOCKING, fn == f, authn == False),
        And(q == LOCKED, action != PRESS_DIGIT,
            qn == LOCKED, fn == f, authn == False),
    ]

    if buggy:
        submit_wrong = And(
            q == UNLOCKING, action == SUBMIT_WRONG,
            qn == UNLOCKED, fn == f + 1, authn == False,
        )
        submit_correct = And(
            q == UNLOCKING, action == SUBMIT_CORRECT,
            qn == UNLOCKED, fn == f, authn == True,
        )
    else:
        submit_wrong = Or(
            And(q == UNLOCKING, action == SUBMIT_WRONG, f < 2,
                qn == LOCKED, fn == f + 1, authn == False),
            And(q == UNLOCKING, action == SUBMIT_WRONG, f >= 2,
                qn == ALARM, fn == 3, authn == False),
        )
        submit_correct = And(
            q == UNLOCKING, action == SUBMIT_CORRECT,
            qn == UNLOCKED, fn == 0, authn == True,
        )

    unlocking_cases = [
        submit_correct,
        submit_wrong,
        And(q == UNLOCKING, action == CANCEL,
            qn == LOCKED, fn == f, authn == False),
        And(q == UNLOCKING,
            Or(action == PRESS_DIGIT, action == LOCK_DOOR, action == ADMIN_RESET),
            qn == UNLOCKING, fn == f, authn == False),
    ]
    unlocked_cases = [
        And(q == UNLOCKED, action == LOCK_DOOR,
            qn == LOCKED, fn == f, authn == False),
        And(q == UNLOCKED, action != LOCK_DOOR,
            qn == UNLOCKED, fn == f, authn == auth),
    ]
    alarm_cases = [
        And(q == ALARM, action == ADMIN_RESET,
            qn == LOCKED, fn == 0, authn == False),
        And(q == ALARM, action != ADMIN_RESET,
            qn == ALARM, fn == 3, authn == False),
    ]
    return Or(*(locked_cases + unlocking_cases + unlocked_cases + alarm_cases))


def build_bmc(k: int, *, buggy: bool = False) -> Tuple[Solver, PathVars]:
    v = PathVars(
        state=[Int(f"q_{i}") for i in range(k + 1)],
        failed=[Int(f"failed_{i}") for i in range(k + 1)],
        authenticated=[Bool(f"authenticated_{i}") for i in range(k + 1)],
        action=[Int(f"action_{i}") for i in range(k)],
    )
    solver = Solver()
    solver.add(*_domain_constraints(v, k))
    solver.add(v.state[0] == LOCKED, v.failed[0] == 0, v.authenticated[0] == False)
    for i in range(k):
        solver.add(
            _transition(
                v.state[i], v.failed[i], v.authenticated[i], v.action[i],
                v.state[i + 1], v.failed[i + 1], v.authenticated[i + 1],
                buggy=buggy,
            )
        )
    return solver, v


def _trace(model, v: PathVars, k: int) -> List[str]:
    lines = []
    for i in range(k + 1):
        q = model.eval(v.state[i]).as_long()
        f = model.eval(v.failed[i]).as_long()
        auth = bool(model.eval(v.authenticated[i]))
        if i < k:
            action = model.eval(v.action[i]).as_long()
            lines.append(
                f"  s{i}: {STATE_NAME[q]:9s} failed={f} auth={str(auth):5s} "
                f"--{ACTION_NAME[action]}-->"
            )
        else:
            lines.append(f"  s{i}: {STATE_NAME[q]:9s} failed={f} auth={str(auth):5s}")
    return lines


def _run_query(title: str, solver: Solver, v: PathVars, k: int, expected, *, show_trace=False):
    result = solver.check()
    status = "PASS" if result == expected else "FAIL"
    print(f"[{status}] {title}: {str(result).upper()}")
    if result == sat and show_trace:
        for line in _trace(solver.model(), v, k):
            print(line)
    return status == "PASS"


def _python_step(state: Tuple[int, int, bool], action: int) -> Tuple[int, int, bool]:
    q, f, auth = state
    if q == LOCKED:
        return (UNLOCKING, f, False) if action == PRESS_DIGIT else (LOCKED, f, False)
    if q == UNLOCKING:
        if action == SUBMIT_CORRECT:
            return UNLOCKED, 0, True
        if action == SUBMIT_WRONG:
            return (ALARM, 3, False) if f >= 2 else (LOCKED, f + 1, False)
        if action == CANCEL:
            return LOCKED, f, False
        return UNLOCKING, f, False
    if q == UNLOCKED:
        return (LOCKED, f, False) if action == LOCK_DOOR else (UNLOCKED, f, auth)
    if action == ADMIN_RESET:
        return LOCKED, 0, False
    return ALARM, 3, False


def reachability_diameter() -> Tuple[int, Dict[Tuple[int, int, bool], int]]:
    initial = (LOCKED, 0, False)
    distance = {initial: 0}
    queue = deque([initial])
    while queue:
        state = queue.popleft()
        for action in ACTION_NAME:
            nxt = _python_step(state, action)
            if nxt not in distance:
                distance[nxt] = distance[state] + 1
                queue.append(nxt)
    return max(distance.values()), distance


def main() -> int:
    print("SMART LOCK FORMAL VERIFICATION - Z3 BMC")
    print(f"Z3 version: {get_version_string()}")
    diameter, reachable = reachability_diameter()
    print(f"Reachable product states: {len(reachable)}")
    print(f"Reachability diameter (CT_state): {diameter}")
    print()

    checks = []

    # P4 violation query: leave ALARM on a non-admin action.
    k = 7
    solver, v = build_bmc(k, buggy=False)
    solver.add(Or(*[
        And(v.state[i] == ALARM, v.action[i] != ADMIN_RESET,
            v.state[i + 1] != ALARM)
        for i in range(k)
    ]))
    checks.append(_run_query("SAFE P4 alarm escape, k=7", solver, v, k, unsat))

    # Concrete persistent-attack witness: three wrong PINs, then two more
    # non-admin actions.  Both are ignored by the ALARM state.
    actions = [PRESS_DIGIT, SUBMIT_WRONG] * 3 + [PRESS_DIGIT, SUBMIT_WRONG]
    solver, v = build_bmc(len(actions), buggy=False)
    solver.add(*[v.action[i] == action for i, action in enumerate(actions)])
    solver.add(v.state[-1] == ALARM)
    checks.append(_run_query(
        "SAFE persistent attack remains in ALARM", solver, v, len(actions), sat,
        show_trace=True,
    ))

    # Admin reset is the only permitted transition out of ALARM.
    actions = [PRESS_DIGIT, SUBMIT_WRONG] * 3 + [ADMIN_RESET]
    solver, v = build_bmc(len(actions), buggy=False)
    solver.add(*[v.action[i] == action for i, action in enumerate(actions)])
    solver.add(v.state[-1] == LOCKED, v.failed[-1] == 0)
    checks.append(_run_query(
        "SAFE admin reset returns ALARM to LOCKED", solver, v, len(actions), sat,
        show_trace=True,
    ))

    # P1 on the buggy implementation: wrong PIN reaches unauthenticated UNLOCKED.
    k = 2
    solver, v = build_bmc(k, buggy=True)
    solver.add(v.action[0] == PRESS_DIGIT, v.action[1] == SUBMIT_WRONG)
    solver.add(v.state[2] == UNLOCKED, Not(v.authenticated[2]))
    checks.append(_run_query(
        "BUGGY P1 unauthenticated unlock", solver, v, k, sat, show_trace=True,
    ))

    # The same P1 violation query must be impossible on the fixed model.
    k = 7
    solver, v = build_bmc(k, buggy=False)
    solver.add(Or(*[
        And(v.state[i] == UNLOCKED, Not(v.authenticated[i]))
        for i in range(k + 1)
    ]))
    checks.append(_run_query("SAFE P1 unauthenticated unlock, k=7", solver, v, k, unsat))

    # P3 reachability: a correct PIN can still unlock the door.
    k = 2
    solver, v = build_bmc(k, buggy=False)
    solver.add(v.action[0] == PRESS_DIGIT, v.action[1] == SUBMIT_CORRECT)
    solver.add(v.state[2] == UNLOCKED, v.authenticated[2])
    checks.append(_run_query(
        "SAFE P3 authenticated UNLOCKED is reachable", solver, v, k, sat,
        show_trace=True,
    ))

    passed = sum(checks)
    print()
    print(f"OVERALL: {passed}/{len(checks)} checks passed")
    return 0 if passed == len(checks) else 1


if __name__ == "__main__":
    raise SystemExit(main())

"""Small control-flow views for SecLabFramework Ch3.

These functions intentionally avoid Z3 expressions so the educational CFG
renderer can produce readable before/after graphs.
"""

LOCKED = 0
UNLOCKED = 2
ALARM = 3
ADMIN_RESET = 5


def submit_v0(pin_correct, failed):
    """Buggy version: every submitted PIN reaches UNLOCKED."""
    if not pin_correct:
        failed = failed + 1
    return UNLOCKED


def submit_v1(pin_correct, failed):
    """Fixed version: correct PIN unlocks; three failures raise ALARM."""
    if pin_correct:
        return UNLOCKED

    failed = failed + 1
    if failed >= 3:
        return ALARM
    return LOCKED


def alarm_step(state, action):
    """Only ADMIN_RESET may leave ALARM; other actions self-loop."""
    if state != ALARM:
        return state
    if action == ADMIN_RESET:
        return LOCKED
    return ALARM


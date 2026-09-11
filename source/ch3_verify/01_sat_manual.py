"""
Chuong 3 - Phan 1, muc 3.3/3.4: SAT Solving
================================================

Bai tap: "Giai SAT bang tay" (slide 1133/100)
  phi = (a v ~b) ^ (b v c) ^ (~a v ~c)
  Hoi: cong thuc nay co SAT khong? Neu co, tim mot phep gan thoa man.

File nay VUA giai bang suy luan thu cong (comment) VUA viet code brute-force
(vet can 2^3 to hop) va doi chieu bang Z3 SAT solver de xac nhan ket qua.

Chay: python3 ch3_verify/01_sat_manual.py
"""
from itertools import product

try:
    from z3 import Bool, Or, Not, And, Solver, sat
    HAS_Z3 = True
except ImportError:
    HAS_Z3 = False


def phi(a: bool, b: bool, c: bool) -> bool:
    """phi = (a v ~b) ^ (b v c) ^ (~a v ~c)"""
    return (a or not b) and (b or c) and (not a or not c)


def brute_force_sat():
    """Vet can toan bo 2^3 = 8 to hop (a,b,c) -> tim phep gan thoa man."""
    satisfying = []
    for a, b, c in product([True, False], repeat=3):
        if phi(a, b, c):
            satisfying.append((a, b, c))
    return satisfying


def z3_sat():
    a, b, c = Bool("a"), Bool("b"), Bool("c")
    s = Solver()
    s.add(Or(a, Not(b)))
    s.add(Or(b, c))
    s.add(Or(Not(a), Not(c)))
    result = s.check()
    return result, (s.model() if result == sat else None)


if __name__ == "__main__":
    print("== Giai thu cong (suy luan tung buoc, xem comment file) ==")
    print("  Thu a=False: menh de 1 (F v ~b) can b=False")
    print("  Voi b=False: menh de 2 (F v c) can c=True")
    print("  Kiem tra menh de 3 (~a v ~c) = (T v F) = T -> tat ca dung")
    print("  => SAT voi a=False, b=False, c=True (dap an slide)")

    print("\n== Xac nhan bang brute-force (vet can 2^3 = 8 to hop) ==")
    results = brute_force_sat()
    print(f"  So phep gan thoa man: {len(results)} / 8")
    for a, b, c in results:
        print(f"    a={a}, b={b}, c={c}")

    if HAS_Z3:
        print("\n== Xac nhan bang Z3 SMT/SAT solver ==")
        result, model = z3_sat()
        print(f"  Ket qua: {result}")
        if model:
            print(f"  Mot phep gan thoa man: {model}")

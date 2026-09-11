"""
Chuong 3 - Phan 2, muc 3.5: Bounded Model Checking (BMC)
============================================================

Bai tap: "Ma hoa BMC bang tay" (slide 360/100)
  He thong 2 trang thai s0=0, s1=1; transition R(0,1) va R(1,1) (self-loop)
  Thuoc tinh xau: "dat trang thai 1". Viet cong thuc BMC cho k=1, xac dinh
  SAT/UNSAT.

  BMC_1 = (s0 = 0) ^ R(s0, s1) ^ (bad(s0) v bad(s1))

File nay ma hoa CHINH cong thuc do bang Z3 (thay vi chi suy luan tay) de
kiem chung tu dong ket qua SAT va trich xuat counterexample.
"""
from z3 import Int, Solver, sat, Or, And


def R(x: int, y: int) -> bool:
    """Quan he chuyen tiep: R(0,1) va R(1,1) (self-loop tai 1)."""
    return (x, y) in {(0, 1), (1, 1)}


def bad(s: int) -> bool:
    """Thuoc tinh xau: dat trang thai 1."""
    return s == 1


def bmc_k1_with_z3():
    s0, s1 = Int("s0"), Int("s1")
    solver = Solver()
    solver.add(s0 == 0)  # trang thai khoi tao
    # R(s0, s1): chi co 2 cap hop le (0,1) va (1,1) -> ma hoa disjunction
    solver.add(Or(And(s0 == 0, s1 == 1), And(s0 == 1, s1 == 1)))
    # bad(s0) v bad(s1): it nhat 1 trong 2 buoc dat trang thai xau (=1)
    solver.add(Or(s0 == 1, s1 == 1))
    result = solver.check()
    model = solver.model() if result == sat else None
    return result, model


if __name__ == "__main__":
    print("== Bai tap: Ma hoa BMC bang tay (k=1) ==")
    print("  BMC_1 = (s0=0) ^ R(s0,s1) ^ (bad(s0) v bad(s1))")
    result, model = bmc_k1_with_z3()
    print(f"  Ket qua Z3: {result}")
    print(f"  Counterexample (mo hinh thoa man): {model}")
    print("  -> SAT voi s1=1: he thong dat trang thai xau CHI SAU 1 BUOC "
          "(dung nhu dap an slide: R(0,1) cho s1=1 la bad).")

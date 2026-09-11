"""
Chuong 3 - Phan 1, muc 3.4: SMT (Satisfiability Modulo Theories)
====================================================================

3 bai tap trong file nay:
  (1) "Viet rang buoc SMT" (slide 1159): age>=18 && age<=65 && has_license
  (2) "Phan tich cong thuc CNF" (slide 1350): (a ^ b) v c -> CNF
  (3) "Mo hinh hoa bang Bit-vector" (slide 1375): unsigned char 250 + 10 tran so
  (4) "Bai tap tong hop: Tu ma nguon toi SMT" (slide 1471):
        a + b == c && a > 0 && b > 0 -> sinh bo gia tri dat nhanh return 1

Chay: python3 ch3_verify/02_smt_examples.py
"""
from z3 import (
    Int, Bool, Solver, sat, And, Or, Not, BitVecVal, BitVec, simplify
)


def exercise_1_age_license():
    """Bai tap: Viet rang buoc SMT (slide 1159)."""
    age = Int("age")
    has_license = Bool("has_license")
    s = Solver()
    s.add(And(age >= 18, age <= 65, has_license == True))
    result = s.check()
    model = s.model() if result == sat else None
    return result, model


def exercise_2_cnf():
    """Bai tap: Phan tich cong thuc CNF (slide 1350): (a ^ b) v c
    -> ap dung luat phan phoi: (a v c) ^ (b v c). Kiem chung 2 dang
    TUONG DUONG bang cach so sanh tren moi to hop (a,b,c) qua Z3."""
    a, b, c = Bool("a"), Bool("b"), Bool("c")
    original = Or(And(a, b), c)
    cnf = And(Or(a, c), Or(b, c))

    s = Solver()
    # Neu (original XOR cnf) la UNSAT voi moi to hop -> 2 cong thuc tuong duong
    s.add(original != cnf)
    result = s.check()  # ky vong: unsat (khong ton tai to hop nao lam 2 ve khac nhau)
    return result


def exercise_3_bitvector_overflow():
    """Bai tap: Mo hinh hoa bang Bit-vector (slide 1375):
    unsigned char count = 250; count += 10; -> xac nhan tran so."""
    count = BitVecVal(250, 8)
    result = simplify(count + 10)
    return result


def exercise_4_source_to_smt():
    """Bai tap tong hop: Tu ma nguon toi SMT (slide 1471):
        int check(int a,int b,int c){ if(a+b==c && a>0 && b>0) return 1; return 0; }
    Sinh tu dong bo (a,b,c) dat nhanh return 1."""
    a, b, c = Int("a"), Int("b"), Int("c")
    s = Solver()
    s.add(a + b == c, a > 0, b > 0)
    result = s.check()
    model = s.model() if result == sat else None
    return result, model


if __name__ == "__main__":
    print("== (1) Bai tap: Viet rang buoc SMT (age/has_license) ==")
    r1, m1 = exercise_1_age_license()
    print(f"  Ket qua: {r1}")
    print(f"  Mot bo gia tri thoa man: {m1}")

    print("\n== (2) Bai tap: Phan tich cong thuc CNF ((a^b)vc <-> (avc)^(bvc)) ==")
    r2 = exercise_2_cnf()
    print(f"  Kiem tra tuong duong (original != cnf).check() = {r2}")
    print("  ->", "TUONG DUONG (unsat = khong co phan vi du bac bo)" if str(r2) == "unsat"
          else "KHONG tuong duong!")

    print("\n== (3) Bai tap: Mo hinh hoa bang Bit-vector (unsigned char 250+10) ==")
    r3 = exercise_3_bitvector_overflow()
    print(f"  simplify(BitVecVal(250,8) + 10) = {r3}")
    print("  -> xac nhan: 250 + 10 = 260 mod 256 = 4 (dung nhu dap an slide)")
    assert str(r3) == "4"

    print("\n== (4) Bai tap tong hop: Tu ma nguon toi SMT (check(a,b,c)) ==")
    r4, m4 = exercise_4_source_to_smt()
    print(f"  Ket qua: {r4}")
    print(f"  Bo gia tri dat nhanh return 1: {m4}")

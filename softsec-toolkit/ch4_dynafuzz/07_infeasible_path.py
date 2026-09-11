"""
Bai tap: Xac dinh Infeasible Path (Chuong4_Phan2, slide 966)

    void f(unsigned int x) {
        if (x > 100) {
            if (x < 0) {   // unsigned luon >= 0!
                crash();
            }
        }
    }

Nhanh crash() co feasible (dat duoc) hay khong? Xac nhan bang Z3 voi kieu
BitVec KHONG DAU (unsigned) 32-bit, giong dung ngu nghia C.
"""
from z3 import BitVec, Solver, sat, ULT, UGT


def check_feasibility():
    x = BitVec("x", 32)  # unsigned int 32-bit trong C
    s = Solver()
    s.add(UGT(x, 100))    # x > 100 (unsigned so sanh)
    s.add(ULT(x, 0))      # x < 0 (unsigned so sanh) -- ve mat toan hoc UNSAT
    return s.check()


if __name__ == "__main__":
    print("== Bai tap: Xac dinh Infeasible Path (unsigned int x) ==")
    result = check_feasibility()
    print(f"  Dieu kien: (x > 100) AND (x < 0) voi x la BitVec 32-bit KHONG DAU")
    print(f"  Ket qua Z3: {result}")
    print("  -> UNSAT: nhanh crash() la INFEASIBLE PATH (khong bao gio dat duoc),")
    print("     vi voi kieu unsigned, x < 0 KHONG BAO GIO dung (gia tri nho nhat la 0).")
    print("     Day la mot vi du kinh dien ve tai sao white-box fuzzing/symbolic")
    print("     execution can hieu DUNG NGU NGHIA KIEU DU LIEU (typed) cua ngon ngu,")
    print("     tranh lang phi thoi gian tim input cho duong khong the toi.")

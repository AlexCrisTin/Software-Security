"""
Chuong 3 - Phan 2, muc 3.6: Memory Model
=============================================

Bai tap: "Mo hinh hoa Double-Free bang Memory Model" (slide 661)
  Dung y tuong valid_map da hoc, hay mo ta (bang loi) cach phat hien
  double-free mot cach hinh thuc.

File nay HIEN THUC HOA truc tiep bang Z3 Array theory: valid_map la mot
mang anh xa dia chi con tro -> Bool (True = da cap phat, chua free).

Chay: python3 ch3_verify/06_memory_model_doublefree.py
"""
from z3 import Array, IntSort, BoolSort, Store, Select, Solver, sat, Not, Int


def model_double_free_scenario(second_free_checks_validity: bool):
    """Mo phong: malloc(p) -> free(p) -> free(p) lan 2.
    Neu 'second_free_checks_validity' = True, ta THEM rang buoc:
    tai thoi diem free lan 2, valid_map[p] phai la True (tuc la ham free()
    an toan tu kiem tra truoc khi thuc hien) -> ky vong UNSAT (khong the
    xay ra double-free vi da bi chan).
    Neu = False (khong kiem tra), ta chi hoi 'co ton tai kich ban ma
    valid_map[p]=False luc goi free lan 2 hay khong' -> ky vong SAT (co
    the xay ra double-free)."""
    valid_map = Array("valid_map", IntSort(), BoolSort())
    p = Int("p")
    s = Solver()

    # Sau malloc(p): valid_map[p] = True
    after_malloc = Store(valid_map, p, True)
    # Sau free(p) lan 1: valid_map[p] = False
    after_free1 = Store(after_malloc, p, False)

    if second_free_checks_validity:
        # An toan: free() luon kiem tra Select(valid_map, p) == True truoc khi
        # cho phep free -> tai day ta yeu cau dieu do PHAI dung o lan free thu 2,
        # dong thoi valid_map[p] hien dang la False (mau thuan) -> ky vong UNSAT
        s.add(Select(after_free1, p) == True)
    else:
        # Khong an toan: hoi xem co the goi free(p) lan 2 (khong kiem tra) hay
        # khong, tuc chi can Select(after_free1, p) == False (dung dang trang
        # thai da free) -> day chinh la dieu kien double-free
        s.add(Select(after_free1, p) == False)

    return s.check()


if __name__ == "__main__":
    print("== Mo hinh hoa Double-Free bang valid_map (Z3 Array theory) ==")
    print("Y tuong: sau free(p), valid_map[p] = False. Neu free(p) duoc goi")
    print("LAN NUA ma khong kiem tra, valid_map[p] van dang False -> double-free.\n")

    r_unsafe = model_double_free_scenario(second_free_checks_validity=False)
    print(f"Kich ban KHONG kiem tra truoc khi free lan 2: {r_unsafe}")
    print("  -> SAT nghia la: co ton tai trang thai (p bat ky) ma tai do free() lan 2")
    print("     duoc goi trong khi valid_map[p] = False -> DAY CHINH LA double-free.")

    r_safe = model_double_free_scenario(second_free_checks_validity=True)
    print(f"\nKich ban CO kiem tra 'assert Select(valid_map, p) == True' truoc free lan 2: {r_safe}")
    print("  -> UNSAT nghia la: khong the dong thoi thoa man 'valid_map[p]=True' (dieu")
    print("     kien de duoc phep free) VA 'valid_map[p]=False' (trang thai thuc te sau")
    print("     free lan 1) -> ham free() an toan se TU CHOI thuc hien free lan 2,")
    print("     ngan chan duoc double-free.")

    print("\nRang buoc SMT tong quat (theo dap an slide):")
    print("  Not(Select(valid_map, p)) tai thoi diem free thu 2 => neu SAT,")
    print("  ton tai tinh huong double-free.")

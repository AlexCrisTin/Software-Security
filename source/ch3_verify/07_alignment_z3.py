"""
Chuong 3 - Phan 2, muc 3.7 (?): Kiem chung Alignment bang SMT
==================================================================

Bai tap 1: "Kiem chung Alignment bang Z3" (slide 952)
  Custom allocator tra ve dia chi la boi so cua 4 (KHONG phai 8). struct Data
  yeu cau alignment 8 byte. Hoi: co the vi pham alignment hay khong?

Bai tap 2: "Chung minh tinh chat Alignment" (slide 1076)
  struct S { int a,b; } sizeof(S)=8, alignof(S)=4. Neu base chia het cho 4,
  chung minh S arr[10]; arr[2] cung co dia chi chia het cho 4.

Chay: python3 ch3_verify/07_alignment_z3.py
"""
from z3 import BitVec, Solver, URem, sat, ForAll, Implies, Int


def exercise_1_custom_allocator_violation():
    """addr la boi so cua 4 (addr % 4 == 0). Hoi: co the addr % 8 != 0
    (vi pham yeu cau alignment 8 cua struct Data) hay khong?"""
    addr = BitVec("addr", 64)
    s = Solver()
    s.add(URem(addr, 4) == 0)      # allocator dam bao boi so 4
    s.add(URem(addr, 8) != 0)      # hoi: co vi pham alignment 8 khong?
    result = s.check()
    model = s.model() if result == sat else None
    return result, model


def exercise_2_array_alignment_proof():
    """Chung minh: neu base % 4 == 0 va sizeof(S) == 8, thi voi moi i,
    (base + i*8) % 4 == 0. Ta chung minh bang cach tim PHAN VI DU BAC BO:
    neu KHONG the tim thay base thoa base%4==0 nhung (base+16)%4 != 0
    (i=2) => tinh chat DUNG (proof by refutation, dung Z3 nhu mot bo
    kiem chung khong ton tai phan vi du)."""
    base = Int("base")
    s = Solver()
    s.add(base % 4 == 0)          # gia thiet: base da dung alignment
    s.add((base + 2 * 8) % 4 != 0)  # phu dinh dieu can chung minh (arr[2])
    result = s.check()  # ky vong UNSAT -> khong co phan vi du -> tinh chat DUNG
    return result


if __name__ == "__main__":
    print("== Bai tap: Kiem chung Alignment bang Z3 ==")
    print("Allocator tra ve dia chi boi so 4 (khong phai 8). struct Data can align 8.")
    result, model = exercise_1_custom_allocator_violation()
    print(f"  Ket qua: {result}")
    if model:
        print(f"  Vi du vi pham: addr = {model[BitVec('addr', 64)]}")
    print("  -> SAT: XAC NHAN allocator nay CO THE tra ve dia chi vi pham yeu cau")
    print("     alignment 8 byte cua struct Data (vd: dia chi la boi so 4 nhung khong")
    print("     phai boi so 8, nhu 4, 12, 20, ...).")

    print("\n== Bai tap: Chung minh tinh chat Alignment (arr[2]) ==")
    r2 = exercise_2_array_alignment_proof()
    print(f"  Ket qua (tim phan vi du bac bo tinh chat): {r2}")
    print("  -> UNSAT: KHONG ton tai phan vi du => tinh chat DUNG voi MOI base")
    print("     (mien base da chia het cho 4 tu dau) => arr[2] = base + 16 luon")
    print("     chia het cho 4. Khop voi chung minh tay: base%4=0, 16%4=0 => tong%4=0.")

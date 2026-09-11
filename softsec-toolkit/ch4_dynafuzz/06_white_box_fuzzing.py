"""
Bai tap: Thiet ke White-box Fuzzing cho ham cu the (Chuong4_Phan2, slide 1003)

    int check(int code) {
        if (code == 0x1337) {
            return 1; // Muc tieu
        }
        return 0;
    }

Viet ma Python (Z3) de tu dong sinh gia tri code dat toi return 1, minh hoa
nguyen ly cot loi cua white-box fuzzing (khac voi black-box fuzzing thuan
random, gan nhu KHONG THE doan trung 0x1337 = 4919 trong khong gian 2^32).
"""
from z3 import Int, Solver, sat
import random


def check(code: int) -> int:
    return 1 if code == 0x1337 else 0


def white_box_solve():
    """White-box: dung SMT solver de GIAI NGUOC dieu kien code == 0x1337."""
    code = Int("code")
    s = Solver()
    s.add(code == 0x1337)
    result = s.check()
    model = s.model() if result == sat else None
    return result, model


def black_box_attempt(max_tries: int = 2_000_000, seed: int = 1) -> int:
    """Black-box: thu ngau nhien trong pham vi int 32-bit -- xac suat trung
    0x1337 la 1/2^32, minh hoa TAI SAO can white-box cho dieu kien equality
    hiem gap nhu the nay."""
    random.seed(seed)
    for i in range(1, max_tries + 1):
        candidate = random.randint(-2**31, 2**31 - 1)
        if check(candidate) == 1:
            return i
    return -1  # khong tim thay trong so lan thu cho phep


if __name__ == "__main__":
    print("== White-box fuzzing: giai nguoc dieu kien code == 0x1337 bang Z3 ==")
    result, model = white_box_solve()
    print(f"  Ket qua Z3: {result}")
    print(f"  Gia tri sinh ra: {model}")
    code_value = model[Int("code")].as_long()
    print(f"  Xac nhan: check({code_value}) = {check(code_value)}  (mong doi 1)")

    print("\n== Doi chieu voi Black-box fuzzing (thu ngau nhien) ==")
    tries = black_box_attempt(max_tries=2_000_000)
    if tries == -1:
        print("  Sau 2,000,000 lan thu ngau nhien: VAN CHUA tim thay 0x1337")
        print("  -> xac suat trung 1 lan thu la 1/2^32 ~ 2.3e-10, minh hoa ro")
        print("     nguyen ly: white-box fuzzing (SMT solver) giai QUYET TRUC TIEP")
        print("     dieu kien equality, trong khi black-box gan nhu bat luc voi")
        print("     'magic constant' nhu the nay neu khong co dictionary ho tro.")
    else:
        print(f"  Tim thay sau {tries} lan thu (hiem, may man)")

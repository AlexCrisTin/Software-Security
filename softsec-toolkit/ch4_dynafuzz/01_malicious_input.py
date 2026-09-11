"""
Chuong 4 - Phan 1, muc 4.1: Security Testing / Fuzzing
============================================================

Bai tap: "Xac dinh input 'ac y' cho mot ham" (slide 184)

    void process_name(char *name, int max_len) {
        char buffer[64];
        strncpy(buffer, name, max_len);
    }

Voi tu duy security testing, de xuat 3 input "ac y" dang thu cho ham nay,
va MO PHONG lai bang mot ham Python tuong duong de kiem chung hau qua ma
khong can crash chuong trinh that (C ban that duoc kiem chung bang CBMC/ASan
trong file 01b_malicious_input_harness.c).
"""


def process_name_model(name: str, max_len: int, buffer_size: int = 64) -> dict:
    """Mo phong lai strncpy(buffer, name, max_len) vao buffer 64 byte de
    phan tich hau qua ma khong thuc su ghi de bo nho that."""
    truncated = name[:max_len]
    bytes_written = min(len(name), max_len)
    overflow = bytes_written > buffer_size
    # strncpy KHONG tu dong them '\0' neu name dai >= max_len -> co the
    # thieu ky tu ket thuc chuoi (missing null terminator, CWE-170)
    missing_null_terminator = len(name) >= max_len
    return {
        "bytes_written": bytes_written,
        "buffer_overflow": overflow,
        "missing_null_terminator": missing_null_terminator,
    }


MALICIOUS_INPUTS = [
    # (mo ta, name, max_len)
    ("max_len > 64 (buffer cung chi co 64 byte)", "A" * 100, 100),
    ("name dai dung bang max_len -> thieu ky tu '\\0' ket thuc", "B" * 64, 64),
    ("max_len am (so nguyen am truyen vao tham so int)", "C" * 10, -1),
]


if __name__ == "__main__":
    print("== Bai tap: Xac dinh input 'ac y' cho process_name() ==\n")
    for desc, name, max_len in MALICIOUS_INPUTS:
        print(f"Input: {desc}")
        print(f"  name (rut gon)='{name[:20]}...' ({len(name)} ky tu), max_len={max_len}")
        result = process_name_model(name, max_len)
        print(f"  -> {result}")
        if result["buffer_overflow"]:
            print("  !! CANH BAO: se ghi vuot qua buffer[64] -> CWE-787 stack buffer overflow")
        if result["missing_null_terminator"]:
            print("  !! CANH BAO: strncpy khong dam bao '\\0' ket thuc -> doc chuoi sau nay se")
            print("     doc tran qua vung nho ke tiep (CWE-170)")
        print()

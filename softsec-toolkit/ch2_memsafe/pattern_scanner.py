"""
Chuong 2 - Phan 2, muc 2.5: Cong cu phan tich tinh
=====================================================

Bai tap: "Viet Rule tuy chinh (khai niem)" (slide 961/100) yeu cau MO TA
bang loi cach mot static-analysis rule don gian co the phat hien viec dung
ham system() (cam vi rui ro command injection, CWE-78, da hoc o Chuong 1).

Module nay hien thuc hoa CHINH rule do bang Python (dung regex, giong cach
cac cong cu syntax-based nhu grep-rule/cppcheck --rule hoat dong o muc co
ban), thay vi chi mo ta bang loi -- day la phan "code hoa" tu nhien cua bai
tap khai niem nay, dung cho module ch2_memsafe.pattern_scanner duoc nhac
toi cung ten trong slide 955.

Chay: python3 ch2_memsafe/pattern_scanner.py <file.c> [file2.c ...]
"""
import re
import sys
from dataclasses import dataclass
from typing import List


@dataclass
class Finding:
    file: str
    line_no: int
    line: str
    rule: str


# Danh sach ham nguy hiem can canh bao. system() la trong tam cua bai tap,
# cac ham con lai lay tu "Checklist Code Review cho ma C" (Chuong2_Phan1)
# de scanner nay huu ich hon trong thuc te.
BANNED_FUNCTIONS = {
    "system": "Nguy co Command Injection (CWE-78) - cam dung theo chinh sach to chuc",
    "gets": "Khong gioi han do dai input - buffer overflow chac chan (CWE-242)",
    "strcpy": "Khong kiem tra do dai dich - nen dung strncpy/snprintf",
    "strcat": "Khong kiem tra do dai dich - nen dung strncat/snprintf",
    "sprintf": "Khong gioi han do dai - nen dung snprintf",
}

_CALL_RE = {name: re.compile(rf"\b{name}\s*\(") for name in BANNED_FUNCTIONS}


def scan_source(path: str) -> List[Finding]:
    findings: List[Finding] = []
    with open(path, "r", encoding="utf-8", errors="replace") as f:
        for line_no, line in enumerate(f, start=1):
            stripped = line.strip()
            if stripped.startswith("//") or stripped.startswith("*"):
                continue
            for name, pattern in _CALL_RE.items():
                if pattern.search(line):
                    findings.append(Finding(path, line_no, line.rstrip("\n"), name))
    return findings


def report(findings: List[Finding]) -> None:
    if not findings:
        print("Khong phat hien vi pham nao.")
        return
    for f in findings:
        print(f"{f.file}:{f.line_no}: canh bao [{f.rule}] {BANNED_FUNCTIONS[f.rule]}")
        print(f"    {f.line.strip()}")


if __name__ == "__main__":
    files = sys.argv[1:] or [
        "ch2_memsafe/01_linked_list_uaf.c",
        "ch2_memsafe/04_unsafe_fixes.c",
        "ch2_memsafe/07_cppcheck_demo.c",
    ]
    for path in files:
        print(f"== Quet {path} ==")
        report(scan_source(path))
        print()

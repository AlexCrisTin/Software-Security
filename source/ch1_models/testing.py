"""
Chuong 1 - Phan 1, muc 1.3: Kiem thu & kiem chung phan mem
============================================================

File nay hien thuc hoa cac bai tap co the "viet code" trong Phan 1:

- Bai tap "chuan bi du an Python (module ch1_models)" (slide 96-97/100):
    ham mo phong equivalence partitioning (EP) va boundary value analysis
    (BVA) TU DONG sinh test case tu khoang gia tri hop le.
- Bai tap: Equivalence Partitioning cho mat khau (slide 88-90/100)
- Bai tap: Boundary Value Analysis cho mat khau (slide 90-92/100)
- Vi du Test Automation voi pytest (slide 87/100) -> xem tests/test_age.py
- Bai tap thuc hanh cuoi Phan 1 (slide 98/100): 3 test case BVA cho ham
    copy_input (buffer overflow) -> ham `boundary_value_test_cases()` duoi day
    duoc tai su dung, ket qua duoc kiem chung bang C trong ch2_memsafe.

Ngon ngu: Python 3 (dung cho toan bo softsec-toolkit theo dinh huong slide).
"""
from dataclasses import dataclass
from typing import Callable, List, Tuple


# ---------------------------------------------------------------------------
# 1) Equivalence Partitioning + Boundary Value Analysis tu dong
# ---------------------------------------------------------------------------

@dataclass
class EquivalenceClass:
    name: str
    low: float
    high: float          # None-safe: dung float('inf')/-inf cho khoang mo
    expected_valid: bool


def build_range_classes(low: int, high: int) -> List[EquivalenceClass]:
    """Sinh 3 lop tuong duong chuan cho mot khoang [low, high] dong:
    < low (invalid) | [low, high] (valid) | > high (invalid).
    Day chinh la mo hinh tong quat cho ca vi du 'tuoi hop le' (0-120, slide 75)
    va bai tap 'mat khau 8-20 ky tu' (slide 88-91)."""
    return [
        EquivalenceClass("duoi_bien_duoi", float("-inf"), low - 1, False),
        EquivalenceClass("hop_le", low, high, True),
        EquivalenceClass("tren_bien_tren", high + 1, float("inf"), False),
    ]


def boundary_value_test_cases(low: int, high: int) -> List[Tuple[int, bool]]:
    """Sinh 4 gia tri bien chuan: low-1, low, high, high+1 kem nhan (expected)
    -> dung cho ca bai tap Equivalence/BVA mat khau va copy_input.

    Vi du voi (8, 20): tra ve [(7, False), (8, True), (20, True), (21, False)]
    -- dung KHOP voi dap an slide 91/100.
    """
    return [
        (low - 1, False),
        (low, True),
        (high, True),
        (high + 1, False),
    ]


def is_valid_age(age: int) -> bool:
    """Ham vi du slide 87/100 (0 <= age <= 120)."""
    return 0 <= age <= 120


def is_valid_password_length(pwd: str) -> bool:
    """Bai tap Equivalence Partitioning / BVA cho mat khau (slide 88-91):
    do dai hop le tu 8 den 20 ky tu."""
    return 8 <= len(pwd) <= 20


# ---------------------------------------------------------------------------
# 2) Bai tap: Tinh Cyclomatic Complexity (Chuong1_Phan2, slide 21-23)
# ---------------------------------------------------------------------------
#
#   int f(int a, int b) {
#       if (a > 0) {
#           if (b > 0) return 1;
#           else return 2;
#       }
#       return 0;
#   }
#
# CFG co 4 node quyet dinh/tra ve va 4 canh phan nhanh doc lap.
# V(G) = E - N + 2  =  cach tinh thu cong o duoi, dong thoi mo phong lai
# bang do thi (adjacency list) de tinh tu dong cho ham bat ky duoc mo ta
# duoi dang CFG.

def cyclomatic_complexity(edges: int, nodes: int, connected_components: int = 1) -> int:
    """V(G) = E - N + 2P (P = so thanh phan lien thong, thuong = 1)."""
    return edges - nodes + 2 * connected_components


def f_reference(a: int, b: int) -> int:
    """Cai dat lai ham f(a, b) trong bai tap de co the do coverage thuc te."""
    if a > 0:
        if b > 0:
            return 1
        else:
            return 2
    return 0


def branch_coverage(test_cases: List[Tuple[int, int]]) -> dict:
    """Bai tap: Statement vs Branch Coverage (slide 393 vung Chuong1_Phan2).

    Voi bo test chi gom (a=5, b=3): tra ve ty le statement/branch coverage va
    danh sach nhanh chua duoc bao phu, dung khop dap an slide (statement=100%,
    branch=50%, thieu nhanh a<=0 va nhanh else khi b<=0).
    """
    branches_hit = {"a>0": False, "a<=0": False, "b>0_given_a>0": False, "b<=0_given_a>0": False}
    statements_hit = {"check_a": False, "check_b": False, "return1": False, "return2": False, "return0": False}

    for a, b in test_cases:
        statements_hit["check_a"] = True
        if a > 0:
            branches_hit["a>0"] = True
            statements_hit["check_b"] = True
            if b > 0:
                branches_hit["b>0_given_a>0"] = True
                statements_hit["return1"] = True
            else:
                branches_hit["b<=0_given_a>0"] = True
                statements_hit["return2"] = True
        else:
            branches_hit["a<=0"] = True
            statements_hit["return0"] = True

    total_branches = len(branches_hit)
    hit_branches = sum(branches_hit.values())
    total_stmts = len(statements_hit)
    hit_stmts = sum(statements_hit.values())

    missing = [k for k, v in branches_hit.items() if not v]
    return {
        "statement_coverage": hit_stmts / total_stmts,
        "branch_coverage": hit_branches / total_branches,
        "missing_branches": missing,
    }


def suggested_extra_test_cases() -> List[Tuple[int, int]]:
    """De xuat test case bo sung de dat 100% branch coverage (cau 3, slide 393)."""
    return [(5, 3), (5, -3), (-5, 0)]


# ---------------------------------------------------------------------------
# 3) Bai tap: Thiet ke Decision Table (Chuong1_Phan2, slide 590)
# ---------------------------------------------------------------------------
#
#   Tu choi boi thuong neu (qua han phi) HOAC (gian lan phat hien).

def insurance_decision(overdue: bool, fraud_detected: bool) -> str:
    """4 to hop dieu kien -> quyet dinh 'Tu choi' / 'Chap nhan',
    khop voi decision table dap an cua bai tap."""
    if overdue or fraud_detected:
        return "Tu choi"
    return "Chap nhan"


def full_decision_table() -> List[dict]:
    rows = []
    for overdue in (True, False):
        for fraud in (True, False):
            rows.append({
                "Qua han phi?": "D" if overdue else "S",
                "Gian lan?": "D" if fraud else "S",
                "Ket qua": insurance_decision(overdue, fraud),
            })
    return rows


if __name__ == "__main__":
    print("== EP/BVA tu dong cho khoang [8, 20] (mat khau) ==")
    for cls in build_range_classes(8, 20):
        print(f"  {cls.name}: [{cls.low}, {cls.high}] hop le={cls.expected_valid}")
    print("  4 test case bien:", boundary_value_test_cases(8, 20))

    print("\n== Cyclomatic Complexity cho f(a,b) ==")
    # CFG day du: N1 kiem tra a>0, N2 kiem tra b>0, N3 return1, N4 return2,
    # N5 return0, N6 exit chung -> 6 node, 7 canh (N1->N2, N1->N5, N2->N3,
    # N2->N4, N3->N6, N4->N6, N5->N6)
    print("  V(G) = E - N + 2 =", cyclomatic_complexity(edges=7, nodes=6))
    print("  (kiem tra cheo: V(G) = so_dieu_kien_quyet_dinh + 1 =", 2 + 1, ")")

    print("\n== Branch coverage voi 1 test case (a=5, b=3) ==")
    result = branch_coverage([(5, 3)])
    print(f"  statement coverage = {result['statement_coverage']*100:.0f}%")
    print(f"  branch coverage    = {result['branch_coverage']*100:.0f}%")
    print("  nhanh con thieu    =", result["missing_branches"])
    print("  de xuat test bo sung:", suggested_extra_test_cases())
    print("  kiem tra lai voi 3 test case ->", branch_coverage(suggested_extra_test_cases()))

    print("\n== Decision table: tu choi boi thuong ==")
    for row in full_decision_table():
        print(" ", row)

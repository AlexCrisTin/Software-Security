"""
Bai tap: Tinh Edge Coverage (Chuong4_Phan1, slide 579)

    void f(int a, int b) {
        if (a > 0) {
            if (b > 0) { /* A */ }
            else { /* B */ }
        } else {
            if (b > 0) { /* C */ }
            else { /* D */ }
        }
    }

Voi 2 test case: (a=1,b=1) va (a=-1,b=-1), co bao nhieu trong 4 nhanh
(A,B,C,D) da duoc bao phu?
"""
from typing import List, Tuple


def f_instrumented(a: int, b: int) -> str:
    """Cai dat lai f(a,b), tra ve nhan cua nhanh duoc thuc thi (A/B/C/D)
    -- day chinh la 'instrumentation' toi gian mo phong compile-time
    instrumentation da hoc o muc 4.3."""
    if a > 0:
        if b > 0:
            return "A"
        else:
            return "B"
    else:
        if b > 0:
            return "C"
        else:
            return "D"


def edge_coverage(test_cases: List[Tuple[int, int]]) -> dict:
    covered = set()
    trace = []
    for a, b in test_cases:
        branch = f_instrumented(a, b)
        covered.add(branch)
        trace.append((a, b, branch))
    all_branches = {"A", "B", "C", "D"}
    return {
        "trace": trace,
        "covered": covered,
        "missing": all_branches - covered,
        "coverage_percent": len(covered) / len(all_branches) * 100,
    }


if __name__ == "__main__":
    test_cases = [(1, 1), (-1, -1)]
    print(f"== Bai tap: Tinh Edge Coverage voi test case {test_cases} ==\n")
    result = edge_coverage(test_cases)
    for a, b, branch in result["trace"]:
        print(f"  f({a}, {b}) -> nhanh {branch}")
    print(f"\nNhanh da bao phu: {sorted(result['covered'])} "
          f"({len(result['covered'])}/4 = {result['coverage_percent']:.0f}%)")
    print(f"Nhanh CHUA bao phu: {sorted(result['missing'])}")
    print("-> khop dap an slide: 2/4 nhanh (A va D) da duoc bao phu; can them")
    print("   test case (vd a=1,b=-1 -> B va a=-1,b=1 -> C) de dat 100% edge coverage.")

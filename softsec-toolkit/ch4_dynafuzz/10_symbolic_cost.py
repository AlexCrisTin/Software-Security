"""
Bai tap: Uoc luong chi phi Symbolic Execution (Chuong4_Phan2, slide 852)

So sanh chi phi (so lan goi SMT solver) giua:
  (a) Ham co 20 nhanh re DOC LAP (khong long nhau) -> O(n)
  (b) Ham co 10 tang if-else LONG NHAU (nested) -> O(2^n) duong thi hanh

Minh hoa bang tay + tinh toan cu the.
"""
import math


def independent_branches_cost(n_branches: int) -> int:
    """20 nhanh doc lap: moi nhanh chi can 1 lan goi solver de kiem tra
    feasibility rieng -> chi phi tuyen tinh O(n)."""
    return n_branches


def nested_branches_cost(depth: int) -> int:
    """n tang long nhau: so duong thi hanh phan biet la 2^n (moi tang co
    2 nhanh, nhan don voi tang truoc) -> can toi da 2^n lan goi solver de
    kham pha het (moi duong 1 lan check() trong DFS symbolic execution)."""
    return 2 ** depth


if __name__ == "__main__":
    n1, n2 = 20, 10
    cost1 = independent_branches_cost(n1)
    cost2 = nested_branches_cost(n2)

    print("== Bai tap: Uoc luong chi phi Symbolic Execution ==\n")
    print(f"(a) Ham co {n1} nhanh re DOC LAP:")
    print(f"    So lan goi SMT solver toi da can thiet ~ O(n) = {cost1} lan")
    print(f"    (moi nhanh kiem tra feasibility doc lap, khong anh huong lan nhau)\n")

    print(f"(b) Ham co {n2} tang if-else LONG NHAU:")
    print(f"    So duong thi hanh phan biet = 2^{n2} = {cost2:,} duong")
    print(f"    So lan goi SMT solver toi da can thiet ~ O(2^n) = {cost2:,} lan\n")

    ratio = cost2 / cost1
    print(f"So sanh: ham (b) can NHIEU HON ~{ratio:,.0f} lan so voi ham (a),")
    print(f"mac du chi co it hon so dieu kien re nhanh ({n2} so voi {n1}).")
    print("-> day chinh la 'PATH EXPLOSION' -- van de co ban khien symbolic")
    print("   execution kho mo rong (scale) cho code thuc te co nhieu tang long nhau,")
    print("   can cac ky thuat nhu path merging, state pruning de giam chi phi.")

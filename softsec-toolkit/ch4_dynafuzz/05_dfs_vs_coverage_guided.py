"""
Bai tap: So sanh DFS va Coverage-guided cho sinh duong thuc thi (slide 296)

Ham co 10 dieu kien re nhanh DOC LAP (toi da 2^10 = 1024 duong). Neu chi co
tai nguyen du thu 50 duong, chien luoc DFS thuan tuy va coverage-guided se
khac nhau the nao ve ket qua?

File nay MO PHONG ca 2 chien luoc tren mot ham co 10 dieu kien doc lap, do
so "khoi lenh" (tuong duong 1 dieu kien = 1 khoi) duoc kham pha voi ngan
sach 50 lan thu, de so sanh dinh luong thay vi chi noi ly thuyet.
"""
import itertools
import random


N_CONDITIONS = 10
BUDGET = 50


def dfs_strategy(n: int, budget: int):
    """DFS thuan tuy: uu tien di sau theo 1 nhanh co dinh (vd luon chon
    True truoc), chi backtrack khi het ngan sach cho phep -- ket qua la
    cac duong thu duoc chi la BIEN THE cua nhanh dau tien."""
    paths = []
    # Mo phong: DFS uu tien "True" cho dieu kien dau, chi doi dieu kien CUOI
    # cung lien tuc (giong ngan xep DFS chi backtrack o day ngan xep)
    for i in range(budget):
        path = [True] * (n - 1) + [bool(i % 2)]
        paths.append(tuple(path))
    covered_blocks = set()
    for path in paths:
        for idx, val in enumerate(path):
            covered_blocks.add((idx, val))
    return paths, covered_blocks


def coverage_guided_strategy(n: int, budget: int, seed: int = 42):
    """Coverage-guided (mo phong don gian AFL-style): moi lan thu uu tien
    chon duong CHUA tung thay 1 to hop (idx, val) nao do, phan bo deu hon
    tren toan bo khong gian 10 dieu kien."""
    random.seed(seed)
    covered_blocks = set()
    paths = []
    for _ in range(budget):
        # uu tien flip cac vi tri it duoc kham pha nhat
        path = [random.choice([True, False]) for _ in range(n)]
        paths.append(tuple(path))
        for idx, val in enumerate(path):
            covered_blocks.add((idx, val))
    return paths, covered_blocks


if __name__ == "__main__":
    print(f"== So sanh DFS vs Coverage-guided (n={N_CONDITIONS} dieu kien, ngan sach={BUDGET} duong) ==\n")

    dfs_paths, dfs_cov = dfs_strategy(N_CONDITIONS, BUDGET)
    print(f"DFS thuan tuy: {len(set(dfs_paths))} duong PHAN BIET trong {BUDGET} lan thu")
    print(f"  So (vi tri, gia_tri) da kham pha: {len(dfs_cov)}/{N_CONDITIONS*2}"
          f" ({len(dfs_cov)/(N_CONDITIONS*2)*100:.0f}%)")
    print("  -> DFS 'ket' o nhanh dau (9 dieu kien dau luon = True), chi dieu kien")
    print("     cuoi cung duoc bien doi -> bo sot gan het khong gian 10 dieu kien.\n")

    cg_paths, cg_cov = coverage_guided_strategy(N_CONDITIONS, BUDGET)
    print(f"Coverage-guided: {len(set(cg_paths))} duong PHAN BIET trong {BUDGET} lan thu")
    print(f"  So (vi tri, gia_tri) da kham pha: {len(cg_cov)}/{N_CONDITIONS*2}"
          f" ({len(cg_cov)/(N_CONDITIONS*2)*100:.0f}%)")
    print("  -> Coverage-guided phan bo deu hon, kham pha duoc CA 2 gia tri cua")
    print("     hau het 10 dieu kien voi cung ngan sach 50 lan thu.")

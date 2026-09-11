"""
Chuong 4 - Phan 2, muc 4.4: Concolic Execution
====================================================

Bai tap: "Sinh duong thuc thi cho ham don gian" (slide 209)

    int classify(int x, int y) {
        if (x > 0) {
            if (y > 0) return 1;
            return 2;
        }
        return 3;
    }

Voi input ban dau x=5, y=5 (di vao nhanh return 1), hay liet ke cac path
condition can PHU DINH de kham pha 2 nhanh con lai bang concolic execution.

File nay hien thuc hoa CHINH thuat toan concolic (dynamic symbolic
execution): chay cu the (concrete) de lay path condition, roi dung Z3 phu
dinh tung dieu kien de sinh input moi kham pha nhanh chua tham.
"""
from z3 import Int, Solver, sat, Not, And


def classify_concrete(x: int, y: int) -> int:
    """Thuc thi CU THE (concrete) -- dong thoi ghi lai path condition."""
    if x > 0:
        if y > 0:
            return 1
        return 2
    return 3


def classify_path_condition(x_sym, y_sym, x_concrete, y_concrete):
    """Sinh path condition (danh sach dieu kien symbolic) theo DUNG duong
    di ma thuc thi cu the (x_concrete, y_concrete) da chon."""
    conditions = []
    if x_concrete > 0:
        conditions.append(x_sym > 0)
        if y_concrete > 0:
            conditions.append(y_sym > 0)
        else:
            conditions.append(y_sym <= 0)
    else:
        conditions.append(x_sym <= 0)
    return conditions


def explore_new_branch(path_conditions, negate_index):
    """Phu dinh dieu kien tai vi tri `negate_index` trong path condition,
    giu nguyen cac dieu kien truoc do -> giai bang Z3 de sinh input moi."""
    s = Solver()
    for i, cond in enumerate(path_conditions):
        s.add(Not(cond) if i == negate_index else cond)
    result = s.check()
    return result, (s.model() if result == sat else None)


if __name__ == "__main__":
    x, y = Int("x"), Int("y")
    x0, y0 = 5, 5

    print(f"== Concolic execution: input ban dau x={x0}, y={y0} ==")
    branch = classify_concrete(x0, y0)
    print(f"classify({x0}, {y0}) = {branch}  (di vao nhanh return 1)")

    path = classify_path_condition(x, y, x0, y0)
    print("\nPath condition cua duong hien tai (return 1):")
    for c in path:
        print(f"  {c}")

    print("\n== Phu dinh tung dieu kien de kham pha nhanh moi ==")
    print("\n[Phu dinh dieu kien 2: y>0 -> y<=0] -> kham pha nhanh return 2")
    result, model = explore_new_branch(path, negate_index=1)
    print(f"  Ket qua: {result}, input moi: {model}")
    if model:
        new_x, new_y = model[x].as_long(), model[y].as_long()
        print(f"  Xac nhan: classify({new_x}, {new_y}) = {classify_concrete(new_x, new_y)} (mong doi 2)")

    print("\n[Phu dinh dieu kien 1: x>0 -> x<=0] -> kham pha nhanh return 3")
    result, model = explore_new_branch(path, negate_index=0)
    print(f"  Ket qua: {result}, input moi: {model}")
    if model:
        new_x = model[x].as_long()
        new_y = model[y].as_long() if y in model else 0
        print(f"  Xac nhan: classify({new_x}, {new_y}) = {classify_concrete(new_x, new_y)} (mong doi 3)")

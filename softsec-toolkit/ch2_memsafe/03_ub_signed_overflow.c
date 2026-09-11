/* Bai tap: Xac dinh UB trong doan ma (Chuong2_Phan1, slide 1214)
 * a + b voi a=INT_MAX, b=1 -> TRAN SO CO DAU la Undefined Behavior (UB)
 * theo chuan C (khac unsigned, von duoc dinh nghia ro la wrap-around).
 *
 * Bien dich voi UBSan de PHAT HIEN UB ngay khi chay:
 *   gcc -fsanitize=undefined -g -o /tmp/ub03 03_ub_signed_overflow.c
 */
#include <stdio.h>
#include <limits.h>
#include <stdbool.h>

int compute_ub(int a, int b) {
    int result = a + b; /* UB neu tran so co dau */
    return result;
}

/* Ban an toan: kiem tra tran truoc khi cong (theo checklist code review) */
bool safe_add(int a, int b, int *out) {
    if ((b > 0 && a > INT_MAX - b) || (b < 0 && a < INT_MIN - b)) {
        return false; /* se tran, tu choi thuc hien */
    }
    *out = a + b;
    return true;
}

int main(void) {
    printf("INT_MAX = %d\n", INT_MAX);
    int r = compute_ub(INT_MAX, 1);
    printf("compute_ub(INT_MAX, 1) = %d  (UB - ket qua khong dinh nghia!)\n", r);

    int out;
    bool ok = safe_add(INT_MAX, 1, &out);
    printf("safe_add(INT_MAX, 1) -> ok=%s%s\n", ok ? "true" : "false",
           ok ? "" : " (da chan tran so an toan)");
    return 0;
}

/* Bai tap: BMC voi vong lap (Chuong3_Phan2, slide 445)
 *
 *   int sum_array(int *arr, int n) {
 *       int total = 0;
 *       for (int i = 0; i < n; i++) total += arr[i];
 *       return total;
 *   }
 *
 * Neu muon BMC kiem chung ham nay voi moi n tu 0 den 50, gia tri --unwind
 * toi thieu la bao nhieu? Dieu gi xay ra neu chon --unwind 30?
 *
 * Dap an ly thuyet: can --unwind >= 50 (+1 cho unwinding assertion) de bao
 * phu HET moi gia tri n <= 50. Neu chon --unwind 30, CBMC se KHONG unwind
 * du cho n > 30 -> "unwinding assertion" that bai (bao dong khong day du)
 * hoac CBMC bao SUCCESS "gia" (khong con dung).
 */
#include <stdlib.h>

int sum_array(int *arr, int n) {
    int total = 0;
    for (int i = 0; i < n; i++) {
        total += arr[i];
    }
    return total;
}

int main(void) {
    int n;
    __CPROVER_assume(n >= 0 && n <= 50);
    int arr[50];
    for (int i = 0; i < 50; i++) arr[i] = 1; /* du lieu co dinh, don gian */
    int result = sum_array(arr, n);
    __CPROVER_assert(result == n, "tong phai bang n (moi phan tu = 1)");
    return 0;
}

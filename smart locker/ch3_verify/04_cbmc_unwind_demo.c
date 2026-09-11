/* Bai tap: Xac dinh gia tri Unwind phu hop (Chuong3_Phan2, slide 286)
 *
 *   void process(int n) {
 *       int arr[10];
 *       for (int i = 0; i < n; i++) {
 *           arr[i] = i;   // Loi neu n > 10
 *       }
 *   }
 *
 * Neu muon CBMC phat hien loi ngay ca khi n len toi 15, gia tri --unwind
 * toi thieu nen la bao nhieu?
 *
 * Dap an ly thuyet: --unwind phai >= so lan lap toi da can kiem tra (15)
 * CONG THEM 1 buoc de CBMC tao "unwinding assertion" xac nhan vong lap da
 * duoc unwind du (thuong dat --unwind 16, hoac it nhat 15).
 *
 * Kiem chung THUC TE bang CBMC:
 *   cbmc 04_cbmc_unwind_demo.c --bounds-check --unwind 10 --function process
 *   cbmc 04_cbmc_unwind_demo.c --bounds-check --unwind 16 --function process
 */
void process(int n) {
    int arr[10];
    for (int i = 0; i < n; i++) {
        arr[i] = i; /* CWE-787: out-of-bounds write neu n > 10 */
    }
}

int main(void) {
    int n;
    __CPROVER_assume(n >= 0 && n <= 15); /* gioi han khong gian n de CBMC kha thi */
    process(n);
    return 0;
}

/* Bai tap tong hop lon (Chuong3_Phan2, slide 1386):
 *   Ham C phan tich goi tin mang, dung vong lap doc header_len byte vao
 *   buffer 256 byte co dinh. Kiem chung day du KHONG co buffer overflow.
 *
 * Quy trinh (theo dap an slide):
 *   1) Chay CBMC voi --bounds-check --unwind N (N du lon hon header_len toi da)
 *   2) Neu FAILURE, lay counterexample (header_len cu the) de xac nhan & sua
 *   3) Neu SUCCESS va khong co unwinding assertion failure -> dat completeness
 *
 * File nay chua CA phien ban CO LOI va phien ban DA SUA, kiem chung ca hai
 * bang CBMC that.
 */
#include <stdint.h>

#define BUF_SIZE 256

/* PHIEN BAN CO LOI: khong kiem tra header_len truoc khi doc vao buffer co dinh */
void parse_packet_buggy(const uint8_t *network_data, int header_len, uint8_t *out_buf) {
    for (int i = 0; i < header_len; i++) {
        out_buf[i] = network_data[i]; /* CWE-787 neu header_len > BUF_SIZE */
    }
}

/* PHIEN BAN DA SUA: gioi han header_len khong vuot qua BUF_SIZE */
void parse_packet_fixed(const uint8_t *network_data, int header_len, uint8_t *out_buf) {
    int safe_len = (header_len > BUF_SIZE) ? BUF_SIZE : header_len;
    if (safe_len < 0) safe_len = 0;
    for (int i = 0; i < safe_len; i++) {
        out_buf[i] = network_data[i];
    }
}

#ifdef DEMO_BUGGY
int main(void) {
    int header_len;
    __CPROVER_assume(header_len >= 0 && header_len <= 300); /* gioi han khong gian tim kiem */
    uint8_t network_data[300];
    uint8_t out_buf[BUF_SIZE];
    parse_packet_buggy(network_data, header_len, out_buf);
    return 0;
}
#else
int main(void) {
    int header_len;
    __CPROVER_assume(header_len >= 0 && header_len <= 300);
    uint8_t network_data[300];
    uint8_t out_buf[BUF_SIZE];
    parse_packet_fixed(network_data, header_len, out_buf);
    return 0;
}
#endif

/* Xac nhan THUC TE bang ASan cho bai tap "input ac y" o file 01 (Python model) */
#include <string.h>
#include <stdio.h>

void process_name(char *name, int max_len) {
    char buffer[64];
    strncpy(buffer, name, max_len); /* Loi neu max_len > 64 */
    printf("buffer da ghi (co the khong co '\\0' ket thuc)\n");
}

int main(void) {
    char malicious[] = "AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA";
    process_name(malicious, 100); /* max_len=100 > buffer 64 -> tran */
    return 0;
}

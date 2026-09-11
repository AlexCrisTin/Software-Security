/* Bai tap: Phat hien Memory Leak (Chuong2_Phan1, slide 837)
 * Loi: duplicate_string() cap phat bo nho nhung khong bao gio duoc free()
 * -> Memory Leak, CWE-401.
 *
 * Bien dich (dung Valgrind hoac LeakSanitizer de PHAT HIEN):
 *   gcc -fsanitize=address -g -DDEMO_LEAK -o /tmp/leak02 02_memory_leak.c
 *   ASAN_OPTIONS=detect_leaks=1 /tmp/leak02
 */
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

char *duplicate_string(const char *s) {
    char *copy = malloc(strlen(s) + 1);
    strcpy(copy, s);
    return copy;
}

#ifdef DEMO_LEAK
void process_leaky(void) {
    char *name = duplicate_string("hello");
    printf("%s\n", name);
    /* Ham ket thuc o day -- KHONG free(name) -> memory leak */
}
#endif

void process_fixed(void) {
    char *name = duplicate_string("hello");
    printf("%s\n", name);
    free(name); /* DA SUA: giai phong truoc khi ham ket thuc */
}

int main(void) {
#ifdef DEMO_LEAK
    process_leaky();
#else
    process_fixed();
#endif
    return 0;
}

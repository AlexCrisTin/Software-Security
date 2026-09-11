/* Thuc hanh: Chay cppcheck tren doan ma da hoc (Chuong2_Phan2, slide 691)
 * Gop lai vai doan ma "co loi" da hoc o Phan 1 de cppcheck quet tinh (khong
 * can chay chuong trinh) va doi chieu voi ket qua ASan/Valgrind o tren.
 *
 * Chay: cppcheck --enable=all --inconclusive 07_cppcheck_demo.c
 */
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

char *duplicate_string(const char *s) {
    char *copy = malloc(strlen(s) + 1);
    strcpy(copy, s);
    return copy; /* cppcheck: khong phat hien duoc leak nay (can biet caller) */
}

void leaky_caller(void) {
    char *name = duplicate_string("hello");
    printf("%s\n", name);
    /* thieu free(name) */
}

void greet(char *name) {
    char msg[50];
    strcpy(msg, "Hello, ");   /* cppcheck: canh bao dung strcpy khong an toan */
    strcat(msg, name);
    printf("%s\n", msg);
}

int *make_array(int n) {
    int *arr = malloc(n * sizeof(int));
    for (int i = 0; i <= n; i++) { /* cppcheck: co the phat hien vong lap tran mang tinh */
        arr[i] = 0;
    }
    return arr;
}

int main(void) {
    greet("World");
    int *a = make_array(5);
    free(a);
    leaky_caller();
    return 0;
}

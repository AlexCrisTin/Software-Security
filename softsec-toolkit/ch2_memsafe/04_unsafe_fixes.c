/* 3 bai tap "sua doan ma khong an toan" (Chuong2_Phan1):
 *   (1) slide 1261: greet() dung strcpy/strcat -> buffer overflow
 *   (2) slide 1299: make_array() vong lap <= thay vi < -> off-by-one +
 *       khong kiem tra malloc tra ve NULL
 *   (3) slide 1368: read_line() cap phat thieu 1 byte cho '\0' + khong
 *       kiem tra malloc/fgets tra ve
 *
 * Bien dich: gcc -fsanitize=address -g -o /tmp/fixes04 04_unsafe_fixes.c
 */
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

/* ---------- (1) greet: strcpy/strcat -> snprintf ---------- */
void greet_unsafe(char *name) {
    char msg[50];
    strcpy(msg, "Hello, ");
    strcat(msg, name); /* neu name dai -> tran buffer 50 byte */
    printf("%s\n", msg);
}

void greet_safe(const char *name) {
    char msg[50];
    snprintf(msg, sizeof(msg), "Hello, %s", name); /* tu dong cat bot, khong tran */
    printf("%s\n", msg);
}

/* ---------- (2) make_array: <= thay vi <, khong kiem tra malloc ---------- */
int *make_array_unsafe(int n) {
    int *arr = malloc(n * sizeof(int));
    for (int i = 0; i <= n; i++) { /* Loi 1: <= ghi tran 1 phan tu (out-of-bounds write) */
        arr[i] = 0;
    }
    return arr; /* Loi 2: khong kiem tra malloc co the tra ve NULL */
}

int *make_array_safe(int n) {
    if (n <= 0) return NULL;
    int *arr = malloc((size_t)n * sizeof(int));
    if (arr == NULL) return NULL;      /* sua loi 2 */
    for (int i = 0; i < n; i++) {      /* sua loi 1: < thay vi <= */
        arr[i] = 0;
    }
    return arr;
}

/* ---------- (3) read_line: thieu 1 byte cho '\0', khong kiem tra tra ve ---------- */
char *read_line_unsafe(FILE *f) {
    char buf[256];
    fgets(buf, sizeof(buf), f);              /* khong kiem tra NULL (EOF/loi) */
    char *result = malloc(strlen(buf));      /* Loi 1: thieu +1 cho ky tu '\0' */
    strcpy(result, buf);                     /* Loi 2: strcpy ghi tran 1 byte do thieu cho '\0' */
    return result;
}

char *read_line_safe(FILE *f) {
    char buf[256];
    if (fgets(buf, sizeof(buf), f) == NULL) return NULL; /* kiem tra EOF/loi doc */
    size_t len = strlen(buf);
    char *result = malloc(len + 1);          /* sua loi 1: +1 cho '\0' */
    if (result == NULL) return NULL;
    memcpy(result, buf, len + 1);            /* sua loi 2: khong tran nua */
    return result;
}

int main(void) {
    printf("== (1) greet_safe ==\n");
    greet_safe("Vu Quang Dung");

    printf("\n== (2) make_array_safe(5) ==\n");
    int *arr = make_array_safe(5);
    for (int i = 0; i < 5; i++) printf("%d ", arr[i]);
    printf("\n");
    free(arr);

    printf("\n== (3) read_line_safe (doc 1 dong tu stdin gia lap) ==\n");
    FILE *f = fmemopen("Xin chao ATPM\n", 15, "r");
    char *line = read_line_safe(f);
    printf("doc duoc: \"%s\"\n", line);
    free(line);
    fclose(f);

#ifdef DEMO_UNSAFE
    printf("\n== chay ban KHONG AN TOAN de ASan bat loi ==\n");
    int *bad = make_array_unsafe(5);
    (void)bad;
#endif
    return 0;
}

/* Bai tap: Gioi han do sau de quy an toan (Chuong2_Phan1, slide 1463)
 * Bai toan: ham phan tich bieu thuc long nhau bang de quy, input tu nguoi
 * dung -> co the gay Stack Overflow (CWE-674) neu do sau khong gioi han.
 * Bien phap: gioi han MAX_DEPTH tuong tu dap an slide.
 *
 * Bien dich: gcc -g -o /tmp/rec05 05_recursion_depth.c
 */
#include <stdio.h>
#include <string.h>

#define MAX_DEPTH 100

/* parse_expr don gian: dem do sau dau ngoac '(' long nhau, tra ve
 * -1 neu vuot qua MAX_DEPTH (thay vi de stack overflow that su). */
int parse_expr(const char *s, int depth) {
    if (depth > MAX_DEPTH) {
        fprintf(stderr, "Loi: bieu thuc long nhau qua sau (>%d), tu choi xu ly "
                        "de tranh stack overflow\n", MAX_DEPTH);
        return -1;
    }
    if (*s == '\0') return depth;
    if (*s == '(') return parse_expr(s + 1, depth + 1);
    return parse_expr(s + 1, depth);
}

int main(void) {
    char normal[] = "((((1+2))))";
    printf("parse_expr(\"%s\") = %d (do sau ngoac hop le)\n", normal, parse_expr(normal, 0));

    /* Gia lap input "ac y": 1000 dau '(' lien tiep */
    char malicious[1001];
    memset(malicious, '(', 1000);
    malicious[1000] = '\0';
    int r = parse_expr(malicious, 0);
    printf("parse_expr(1000 dau '(') = %d (%s)\n", r,
           r == -1 ? "DA CHAN, khong bi stack overflow" : "khong mong doi");
    return 0;
}

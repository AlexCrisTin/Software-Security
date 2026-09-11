/* Bai tap thuc hanh mo rong (Chuong2_Phan2, slide 1471)
 * Chuong trinh C nho (~50 dong) quan ly danh sach san pham bang linked list:
 * them / xoa / tim kiem. Sau do:
 *   (1) chay cppcheck va sua moi canh bao muc error
 *   (2) bien dich -fsanitize=address, thu voi du lieu bien (danh sach rong,
 *       xoa phan tu khong ton tai)
 *   (3) tinh toan va toi uu kich thuoc struct san pham theo alignment
 *
 * Bien dich: gcc -fsanitize=address -g -o /tmp/product09 09_product_list_extended.c
 */
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

/* (3) Struct san pham da toi uu alignment: double(8) -> int(4) -> char[24] */
typedef struct Product {
    double price;         /* 8 byte */
    int id;                /* 4 byte */
    char name[24];          /* 24 byte -> tong 8+4+24 = 36, boi so 8 la 40 */
    struct Product *next;
} Product;

Product *add_product(Product *head, int id, const char *name, double price) {
    Product *p = malloc(sizeof(Product));
    if (p == NULL) return head;
    p->id = id;
    strncpy(p->name, name, sizeof(p->name) - 1);
    p->name[sizeof(p->name) - 1] = '\0';
    p->price = price;
    p->next = head;
    return p;
}

Product *remove_product(Product *head, int id) {
    Product *cur = head, *prev = NULL;
    while (cur != NULL) {
        if (cur->id == id) {
            if (prev == NULL) head = cur->next;
            else prev->next = cur->next;
            free(cur);
            return head;
        }
        prev = cur;
        cur = cur->next;
    }
    return head; /* du lieu bien: xoa id khong ton tai -> khong lam gi, an toan */
}

Product *find_product(Product *head, int id) {
    for (Product *cur = head; cur != NULL; cur = cur->next)
        if (cur->id == id) return cur;
    return NULL;
}

void free_all(Product *head) {
    while (head != NULL) {
        Product *next = head->next;
        free(head);
        head = next;
    }
}

int main(void) {
    printf("sizeof(struct Product) = %zu byte\n", sizeof(Product));

    /* (2a) du lieu bien: danh sach rong */
    Product *head = NULL;
    printf("Tim kiem tren danh sach rong: %s\n",
           find_product(head, 1) ? "tim thay" : "khong tim thay (dung nhu ky vong)");
    head = remove_product(head, 1); /* xoa tren danh sach rong -> khong crash */

    head = add_product(head, 1, "Ban phim", 19.99);
    head = add_product(head, 2, "Chuot", 9.99);

    /* (2b) du lieu bien: xoa phan tu KHONG ton tai */
    head = remove_product(head, 999);

    Product *found = find_product(head, 2);
    printf("Tim id=2: %s\n", found ? found->name : "khong tim thay");

    free_all(head);
    printf("Da giai phong toan bo danh sach - kiem tra bang ASan/Valgrind.\n");
    return 0;
}

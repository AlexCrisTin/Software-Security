/* 4 bai tap ve Struct Alignment (Chuong2_Phan2):
 *  (1) slide 138: Tinh sizeof(struct Data) tren x86-64
 *  (2) slide 272: Sap xep lai struct Mixed de giam padding
 *  (3) slide 445: Mang Point points[1000] - anh huong alignment
 *  (4) slide 489: Khong nen dua vao bo cuc struct mac dinh cho protocol
 *      -> dung __attribute__((packed))
 *
 * Bien dich: gcc -g -o /tmp/align06 06_struct_alignment.c && /tmp/align06
 */
#include <stdio.h>
#include <stddef.h>

/* (1) Cho x86-64: char=1, short=2, int=4, double=8 */
struct Data {
    char flag;      /* offset 0, 1 byte, +7 padding (can canh cho double) */
    double value;   /* offset 8, 8 byte */
    short id;       /* offset 16, 2 byte, +6 padding cuoi (can boi so 8) */
};

/* (2) Mixed CHUA toi uu: char, long long, char, int, char */
struct Mixed_unoptimized {
    char a;
    long long b;
    char c;
    int d;
    char e;
};

/* (2) Mixed DA sap xep lai: field lon -> nho de giam padding */
struct Mixed_optimized {
    long long b;   /* 8 byte, offset 0 */
    int d;         /* 4 byte, offset 8 */
    char a;        /* 1 byte, offset 12 */
    char c;        /* 1 byte, offset 13 */
    char e;        /* 1 byte, offset 14, +1 padding cuoi -> tong 16 */
};

/* (3) Point: alignment lon nhat la 4 (int) -> sizeof phai la boi so cua 4 */
struct Point {
    char tag;
    int x, y;
};

/* (4) Protocol design: KHONG nen dua vao bo cuc mac dinh (co padding) khi
 * giao tiep qua mang -- dung packed de kiem soat tuong minh tung byte. */
struct ProtocolHeader_default {
    char type;      /* padding tu dong sau day */
    int length;
};

#pragma pack(push, 1)
struct ProtocolHeader_packed {
    char type;
    int length;
} __attribute__((packed));
#pragma pack(pop)

int main(void) {
    printf("== (1) Bai tap: Tinh kich thuoc Struct ==\n");
    printf("sizeof(struct Data)  = %zu byte\n", sizeof(struct Data));
    printf("  offsetof(flag)=%zu offsetof(value)=%zu offsetof(id)=%zu\n",
           offsetof(struct Data, flag), offsetof(struct Data, value), offsetof(struct Data, id));

    printf("\n== (2) Bai tap: Sap xep lai Struct toi uu ==\n");
    printf("sizeof(struct Mixed_unoptimized) = %zu byte (co nhieu padding xen ke)\n",
           sizeof(struct Mixed_unoptimized));
    printf("sizeof(struct Mixed_optimized)   = %zu byte (sap xep lon->nho, it padding hon)\n",
           sizeof(struct Mixed_optimized));

    printf("\n== (3) Bai tap: Mang Struct va Alignment ==\n");
    printf("sizeof(struct Point) = %zu byte (boi so cua alignment lon nhat = 4, do int)\n",
           sizeof(struct Point));
    printf("-> moi phan tu trong Point points[1000] deu duoc can chinh dung, "
           "khong chi phan tu dau tien\n");

    printf("\n== (4) Bai tap: Alignment trong Protocol Design ==\n");
    printf("sizeof(struct ProtocolHeader_default) = %zu byte (co padding an, phu thuoc compiler/kien truc)\n",
           sizeof(struct ProtocolHeader_default));
    printf("sizeof(struct ProtocolHeader_packed)  = %zu byte (dung 1+4=5 byte, khong padding, "
           "an toan khi truyen qua mang giua cac he thong khac nhau)\n",
           sizeof(struct ProtocolHeader_packed));
    return 0;
}

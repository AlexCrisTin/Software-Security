/* Bai tap tong hop: Ra soat mot module C hoan chinh (Chuong2_Phan2, slide 1129)
 *
 * Module quan ly danh sach sinh vien (linked list of struct Student):
 *   (1) struct Student toi uu alignment
 *   (2) 3 chuc nang: them sinh vien, xoa theo ID, ghi toan bo ra file nhi phan
 *   (3) 3 rui ro bo nho tiem an duoc chu thich truc tiep trong code, cung
 *       cach phong tranh da ap dung
 *
 * Bien dich & chay voi ASan + Valgrind de xac nhan khong loi bo nho:
 *   gcc -fsanitize=address -g -o /tmp/student08 08_student_module.c
 *   /tmp/student08
 */
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <stdint.h>

/* (1) Sap xep truong theo kich thuoc giam dan de giam padding:
 *     double(8) -> int(4) -> char[32] -> uint8_t(1)   */
typedef struct Student {
    double gpa;          /* 8 byte */
    int id;               /* 4 byte */
    char name[32];        /* 32 byte, boi so cua alignment lon nhat */
    uint8_t active;       /* 1 byte, +7 padding cuoi (boi so 8) */
    struct Student *next;
} Student;

/* Rui ro 1 (them sinh vien): malloc co the tra ve NULL -> luon kiem tra */
Student *add_student(Student *head, int id, const char *name, double gpa) {
    Student *s = malloc(sizeof(Student));
    if (s == NULL) {                 /* PHONG TRANH rui ro 1: NULL check */
        fprintf(stderr, "Loi cap phat bo nho cho sinh vien id=%d\n", id);
        return head;
    }
    s->id = id;
    strncpy(s->name, name, sizeof(s->name) - 1);  /* PHONG TRANH tran buffer ten */
    s->name[sizeof(s->name) - 1] = '\0';
    s->gpa = gpa;
    s->active = 1;
    s->next = head;
    return s;
}

/* Rui ro 2 (xoa theo ID): dangling pointer / double-free neu goi xoa 2 lan
 * tren cung 1 con tro ma khong dat lai NULL o phia caller. */
Student *remove_student(Student *head, int id) {
    Student *cur = head, *prev = NULL;
    while (cur != NULL) {
        if (cur->id == id) {
            if (prev == NULL) head = cur->next;
            else prev->next = cur->next;
            free(cur);
            /* PHONG TRANH rui ro 2: khong con truy cap 'cur' sau free() */
            return head;
        }
        prev = cur;
        cur = cur->next;
    }
    return head; /* khong tim thay id -> khong lam gi (tranh free con tro la) */
}

/* Rui ro 3 (ghi file nhi phan): ghi thang struct chua con tro 'next' ra file
 * la loi nghiem trong (dia chi bo nho khong con y nghia khi doc lai / tren
 * may khac) -> chi ghi cac truong du lieu thuc su, KHONG ghi con tro. */
typedef struct { int id; char name[32]; double gpa; uint8_t active; } StudentRecord;

void write_students_binary(Student *head, const char *path) {
    FILE *f = fopen(path, "wb");
    if (f == NULL) { perror("fopen"); return; }
    for (Student *cur = head; cur != NULL; cur = cur->next) {
        StudentRecord rec = { cur->id, {0}, cur->gpa, cur->active };
        memcpy(rec.name, cur->name, sizeof(rec.name));
        /* PHONG TRANH rui ro 3: ghi struct "phang" khong chua con tro */
        fwrite(&rec, sizeof(rec), 1, f);
    }
    fclose(f);
}

void free_all(Student *head) {
    while (head != NULL) {
        Student *next = head->next;
        free(head);
        head = next;
    }
}

int main(void) {
    printf("sizeof(struct Student) = %zu byte (da toi uu alignment)\n", sizeof(Student));

    Student *head = NULL;
    head = add_student(head, 1, "Nguyen Van A", 3.6);
    head = add_student(head, 2, "Tran Thi B", 3.8);
    head = add_student(head, 3, "Le Van C", 3.2);

    head = remove_student(head, 2);

    printf("Danh sach con lai:\n");
    for (Student *cur = head; cur != NULL; cur = cur->next) {
        printf("  id=%d ten=%s gpa=%.1f\n", cur->id, cur->name, cur->gpa);
    }

    write_students_binary(head, "/tmp/students.bin");
    printf("Da ghi danh sach ra /tmp/students.bin (%zu byte/ban ghi)\n", sizeof(StudentRecord));

    free_all(head);
    return 0;
}

/* Bai tap: Tim loi trong doan ma Linked List (Chuong2_Phan1, slide 684)
 *
 * Loi: remove_first() goi free(old_head) RỒI moi doc old_head->data
 * -> Use-After-Free (UAF), CWE-416.
 *
 * Bien dich & chay (co ASan de PHAT HIEN loi ngay khi chay):
 *   gcc -fsanitize=address -g -o /tmp/bug01 01_linked_list_uaf.c && /tmp/bug01
 */
#include <stdio.h>
#include <stdlib.h>

typedef struct Node { int data; struct Node *next; } Node;

Node *make_node(int v, Node *next) {
    Node *n = malloc(sizeof(Node));
    n->data = v;
    n->next = next;
    return n;
}

/* PHIEN BAN CO LOI (dung de minh hoa loi trong slide) */
void remove_first_buggy(Node **head) {
    Node *old_head = *head;
    *head = (*head)->next;
    free(old_head);
    printf("Removed: %d\n", old_head->data); /* Loi o day! UAF */
}

/* PHIEN BAN DA SUA: doc data TRUOC khi free */
void remove_first_fixed(Node **head) {
    Node *old_head = *head;
    int removed_value = old_head->data;      /* doc truoc */
    *head = old_head->next;
    free(old_head);
    printf("Removed: %d\n", removed_value);
}

int main(void) {
#ifdef DEMO_BUG
    Node *head = make_node(1, make_node(2, make_node(3, NULL)));
    remove_first_buggy(&head);
    printf("head->data sau khi xoa: %d\n", head->data);
#else
    Node *head = make_node(1, make_node(2, make_node(3, NULL)));
    remove_first_fixed(&head);
    printf("head->data sau khi xoa: %d\n", head->data);
    free(head->next);
    free(head);
#endif
    return 0;
}

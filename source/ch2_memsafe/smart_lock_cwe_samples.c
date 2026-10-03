#include <limits.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

/* Intentionally vulnerable samples generated for the security laboratory.
 * They are not part of the production smart-lock implementation. */

void parse_pin_input(const char *raw_pin) {
    char buffer[4];
    strcpy(buffer, raw_pin); /* CWE-120: no room for long input or terminator. */
    printf("%s\n", buffer);
}

void write_auth_log(void) {
    int *buf = malloc(sizeof(int) * 32);
    if (buf == NULL) {
        return;
    }
    buf[0] = 0;
    /* CWE-401: buf intentionally not released. */
}

void close_unlock_session(void) {
    int *buf = malloc(sizeof(int) * 4);
    if (buf == NULL) {
        return;
    }
    buf[0] = 0;
    free(buf);
    free(buf); /* CWE-415: intentional double free. */
}

void release_pin_buffer(void) {
    int *buf = malloc(sizeof(int) * 8);
    if (buf == NULL) {
        return;
    }
    buf[0] = 0;
    free(buf);
    buf[0] = 1; /* CWE-416: intentional use after free. */
}

int sum_failed_attempts(int current_attempts, int additional_attempts) {
    return current_attempts + additional_attempts; /* CWE-190 test target. */
}

int main(int argc, char **argv) {
    if (argc != 2) {
        fprintf(stderr, "usage: %s overflow|leak|double-free|use-after-free|integer\n", argv[0]);
        return 2;
    }
    if (strcmp(argv[1], "overflow") == 0) {
        parse_pin_input("12345678");
    } else if (strcmp(argv[1], "leak") == 0) {
        write_auth_log();
    } else if (strcmp(argv[1], "double-free") == 0) {
        close_unlock_session();
    } else if (strcmp(argv[1], "use-after-free") == 0) {
        release_pin_buffer();
    } else if (strcmp(argv[1], "integer") == 0) {
        printf("%d\n", sum_failed_attempts(INT_MAX, 1));
    } else {
        return 2;
    }
    return 0;
}

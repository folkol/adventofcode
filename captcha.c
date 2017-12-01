#include <stdio.h>

#define BUF_SIZE 10000

// Naive filter that extracts line segments between \t and : from stdin
int main(void) {
//    int n, sum;
//    char buf[BUF_SIZE], *c;
//
//    char primus = getc(stdin);
//    printf("%c\n", primus);
//    while ((n = fread(buf, 1, sizeof buf, stdin))) {
//        c = buf;
//        for (int i = 0; i < n - 1; ++i, ++c) {
//            if (buf[n] == buf[n + 1]) {
//                ++sum;
//            }
//        }
//    }
//    printf("%\n", n);
//
//    if (*c == primus) {
//        ++sum;
//    }
//    printf("%d\n", sum);

//    char mybuf[4096];
//    setvbuf(stdin, mybuf, _IOFBF, 4096);

//    int primus, prev, c = 0;
//    long sum = 1;
//    primus = prev = getchar();
//    printf("c: %c\n", primus);
//    while (c = getchar()) {
////        putc(c, stdout);
//        if (prev == c) {
//            sum += prev;
//        }
//        prev = c;
//    }


//    printf("c: %i\n", c);
//    if (c == primus) {
//        sum += c;
//    }
//    printf("%ld\n", sum);
//    return 0;

    int c, prev, primus, sum = 0;
    primus = prev = getchar();
    while (c = getchar(), c != EOF) {
        if (prev == c) {
            sum += c - '0';
        }
        prev = c;
    }
    if (prev == primus) {
        sum += prev;
    }
    printf("%d\n", sum);
}

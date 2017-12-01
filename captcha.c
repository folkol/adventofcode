#include <stdio.h>

#define BUF_SIZE 10000

int main(void) {
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

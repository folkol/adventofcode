#include <stdio.h>
#include <string.h>

#define LPAREN(c) c == '(' || c == '[' || c == '{' || c == '<'
typedef char c_pair[2];
typedef struct { char bracket;int value; } bv;

char complement(char c) {
    static const c_pair table[] = {"()", "[]", "{}", "<>", ")(", "][", "}{", "><"};
    for (int i = 0; i < sizeof(table) / sizeof(table[0]); i++) {
        if (table[i][0] == c) {
            return table[i][1];
        }
    }
    return 0;
}

int value(char c) {
    static const bv table[] = {{')', 3}, {']', 57}, {'}', 1197}, {'>', 25137}};
    for (int i = 0; i < sizeof(table) / sizeof(table[0]); i++) {
        if (table[i].bracket == c) {
            return table[i].value;
        }
    }
    return 0;
}

int main(void) {
    int score = 0;
    char *line = NULL;
    char stack[640 << 10];  // ought to be enough!
    size_t linecap = 0;
    while (getline(&line, &linecap, stdin) > 0) {
        int sp = 0;
        for (char *c = line; *c != '\0' && *c != '\n'; c++) {
            if (LPAREN(*c)) {
                stack[sp++] = *c;
            } else if (stack[sp - 1] == complement(*c)) {
                sp--;
            } else {
                score += value(*c);
                break;
            }
        }
    }

    printf("%d\n", score);
}

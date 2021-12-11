#include <stdio.h>
#include <stdlib.h>

int total_points = 0;

void count_points(char c) {
    switch(c) {
        case ')':
            total_points += 3;
            break;
        case ']':
            total_points += 57;
            break;
        case '}':
            total_points += 1197;
            break;
        case '>':
            total_points += 25137;
            break;
    }
}

int consume_chunk(char* line, int *pos, int limit) {
    char end;
    switch(line[*pos]) {
        case '(':
            end = ')';
            break;
        case '[':
            end = ']';
            break;
        case '{':
            end = '}';
            break;
        case '<':
            end = '>';
            break;
        default:
            return 0;
    }

    (*pos)++;

    while(consume_chunk(line, pos, limit))
        ;

    if(line[*pos] != end) {
        count_points(line[*pos]);
        *pos = limit;
        return 0;
    }

    (*pos)++;

    return 1;
}


int main(void) {
    char *line = NULL;
    size_t linecap = 0;
    ssize_t linelen;
    while ((linelen = getline(&line, &linecap, stdin)) > 0) {
        int pos = 0;
        while(pos < linelen) {
            consume_chunk(line, &pos, linelen);
        }
    }

    printf("%d\n", total_points);

    return 0;
}

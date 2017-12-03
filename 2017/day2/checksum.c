#import <stdio.h>
#import <errno.h>
#import <string.h>
#import <stdlib.h>
#import <limits.h>

int main(void) {
    int sum = 0;
    char buf[1024];
    while (fgets(buf, sizeof buf, stdin)) {
        int i, max = INT_MIN, min = INT_MAX;
        char *s = strtok(buf, "\t");
        while (s) {
            int i = atoi(s);
//            printf("-- s: %s\td: %d\n", s, i);
            if (i > max) {
                max = i;
            }
            if (i < min) {
                min = i;
            }
            s = strtok(NULL, "\t");
        }
        sum += max - min;
//        printf("max: %d\tmin: %d\tdiff: %d\tsum: %d\n", max, min, max - min, sum);
    }
    printf("%d\n", sum);
}


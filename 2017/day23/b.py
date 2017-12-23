"""Hand-optimized version:

    b = 109300
    c = 126300

    for(int i = b; b < c; b += 17) {
        f = 1
        for(int d = 2; d < b; d++) {
            for(int e = 2; e < b; e++) {
                if(d * e == b) { // Found factorization of b
                    f = 0
                }
            }
        }
        if(f == 0) {
            h++
        }
    }

    print(h)

    Essentially: Counting non-prime numbers in the range 126300–109300
"""


def is_prime(a):
    return all(a % i for i in range(2, a))


b = 109300
c = 126300
h = 0

for b in range(109300, 126300 + 1, 17):
    if not is_prime(b):
        h += 1

print(h)

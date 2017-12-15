#include <iostream>
#include <random>

const int MASK = (1 << 16) - 1;
const int N = 40000000;

using namespace std;

int main() {
    minstd_rand0 A(634);
    minstd_rand B(301);

    int score = 0;
    for (int i = 0; i < N; i++) {
        int a = A() & MASK;
        int b = B() & MASK;
        if (a == b) {
            score++;
        }
    }
    cout << score << endl;
    return 0;
}


#include <iostream>
#include <string>
#include <utility>
#include <vector>

struct Point {
    long x, y, z;
};

struct Cube {
    bool state;
    Point p1, p2;

    bool contains(Point p) const {
        return p.x >= p1.x && p.x < p2.x && p.y >= p1.y && p.y < p2.y && p.z >= p1.z && p.z < p2.z;
    }
};

bool state_for(std::vector<Cube> steps, Point point) {
    for (auto &&step = steps.rbegin(); step != steps.rend(); ++step) {
        if (step->contains(point)) {
            return step->state;
        }
    }
    return false;
}

int main() {
    std::vector<Cube> steps;
    std::string line, status;
    int numbers[6];
    while (std::cin) {
        // on numbers=-57795..-6158,y=29564..72030,z=20435..90618
        std::cin >> status;
        std::cin.ignore(3); std::cin >> numbers[0];
        std::cin.ignore(2); std::cin >> numbers[1];
        std::cin.ignore(3); std::cin >> numbers[2];
        std::cin.ignore(2); std::cin >> numbers[3];
        std::cin.ignore(3); std::cin >> numbers[4];
        std::cin.ignore(2); std::cin >> numbers[5];
        std::cin >> std::ws;
        steps.emplace_back(Cube{
            status == "on",
            numbers[0],
            numbers[2],
            numbers[4],
            numbers[1] + 1,
            numbers[3] + 1,
            numbers[5] + 1
        });
    }

    long n = 0;
    for (int x = -50; x <= 50; x++) {
        for (int y = -50; y <= 50; y++) {
            for (int z = -50; z <= 50; z++) {
                n += state_for(steps, Point{x, y, z});
            }
        }
    }
    std::cout << n << "\n";
}

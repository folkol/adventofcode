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

    long volume() const {
        return (p2.x - p1.x) * (p2.y - p1.y) * (p2.z - p1.z);
    }
};

struct CompressedCoords {
    std::vector<long> x, y, z;

    CompressedCoords(const std::vector<Cube> &steps) {
        for (auto step: steps) {
            x.insert(x.end(), {step.p1.x, step.p2.x});
            y.insert(y.end(), {step.p1.y, step.p2.y});
            z.insert(z.end(), {step.p1.z, step.p2.z});
        }
        compress();
    }

    static void sort_uniq(std::vector<long> &v) {
        sort(v.begin(), v.end());
        v.erase(unique(v.begin(), v.end()), v.end());
    }

    void compress() {
        sort_uniq(x);
        sort_uniq(y);
        sort_uniq(z);
    }

    void subdivisions(const std::function<void(Cube &&cube)> &visitor) {
        for (int i = 0; i < x.size() - 1; i++) {
            for (int j = 0; j < y.size() - 1; j++) {
                for (int k = 0; k < z.size() - 1; k++) {
                    visitor(Cube{
                        true,
                        x[i],
                        y[j],
                        z[k],
                        x[i + 1],
                        y[j + 1],
                        z[k + 1]
                    });
                }
            }
        }
    }
};

// TODO: Replace this search with a prepopulated map of compressed coords -> state...
bool state_for(std::vector<Cube> steps, Point &point) {
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
        // on x=-57795..-6158,y=29564..72030,z=20435..90618
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
    CompressedCoords cc(steps);
    cc.subdivisions([&n, steps](Cube subdivision) {
        n += state_for(steps, subdivision.p1) * subdivision.volume();
    });
    std::cout << n << "\n";
}

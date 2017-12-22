import re
from collections import namedtuple, defaultdict

Vector = namedtuple('Vector', ['x', 'y', 'z'])


class Particle(object):
    def __init__(self, id, p, v, a):
        self.id = id
        self.p = p
        self.v = v
        self.a = a

    def tick(self):
        self.v = Vector(self.v.x + self.a.x, self.v.y + self.a.y, self.v.z + self.a.z)
        self.p = Vector(self.p.x + self.v.x, self.p.y + self.v.y, self.p.z + self.v.z)


def parse_particle(i, s):
    px, py, pz, vx, vy, vz, ax, ay, az = map(int, re.findall('-?\d+', s))
    return Particle(i, Vector(px, py, pz), Vector(vx, vy, vz), Vector(ax, ay, az))


particles = [parse_particle(i, line) for i, line in enumerate(open('particles.dat'))]

for _ in range(10_000):  # Ought to be enough for anybody... >.>
    coordinates = defaultdict(list)
    for particle in particles:
        coordinates[particle.p].append(particle)
    particles = [particle for particle in particles if len(coordinates[particle.p]) == 1]
    for particle in particles:
        particle.tick()

print(len(particles))

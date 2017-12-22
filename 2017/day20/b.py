import re
from collections import namedtuple, defaultdict

Vector = namedtuple('Vector', ['x', 'y', 'z'])


class Particle(object):
    def __init__(self, id, p, v, a):
        self.id = id
        self.p = p
        self.v = v
        self.a = a


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
        particle.v = Vector(particle.v.x + particle.a.x, particle.v.y + particle.a.y, particle.v.z + particle.a.z)
        particle.p = Vector(particle.p.x + particle.v.x, particle.p.y + particle.v.y, particle.p.z + particle.v.z)

print(len(particles))

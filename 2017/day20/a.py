import re
from collections import namedtuple

Vector = namedtuple('Vector', ['x', 'y', 'z'])
Particle = namedtuple('Particle', ['id', 'p', 'v', 'a'])


def parse_particle(i, s):
    px, py, pz, vx, vy, vz, ax, ay, az = map(int, re.findall('-?\d+', s))
    return Particle(i, (px, py, pz), (vx, vy, vz), (ax, ay, az))


def manhattan_acc(particle):
    return sum(map(abs, particle.a))


particles = (parse_particle(i, line) for i, line in enumerate(open('particles.dat')))

print(min(particles, key=manhattan_acc))

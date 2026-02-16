#!/usr/bin/env python3

from collections import namedtuple
import math
import sys

#
# Const
#

G = 6.67408*10**-11

EARTH_MASS = 5.97237*10**24
EARTH_RADIUS = 6.378*10**6
MOON_MASS = 7.342*10**22
# MOON_RADIUS = 1.737*10**6
EARTH_MOON_D = 3.84402 * 10**8

ANGULAR_SPEED = 2*math.pi / (27.3*86400)  # rad/sec

SIM_DURATION = 10.0*86400
INJECTION_ALTITUDE = 185*1000  # 100 nm (Apollo 16-17: 90 nm)

EXPORT_DT = 50
EXPORT_DT_MS = EXPORT_DT*1000.0

#
# Helpers
#

def deg2rad(angle):
    return angle*math.pi/180.0

#
# Vector
#

class Vector(object):
    def __init__(self, x, y):
        self.x = x
        self.y = y

    @staticmethod
    def from_polar_rad(magnitude, angle):
        return Vector(
            magnitude*math.cos(angle),
            magnitude*math.sin(angle),
        )

    def magnitude(self):
        return math.sqrt(self.x**2 + self.y**2)

    def rotate(self, r):
        return Vector(
            r[0][0]*self.x + r[0][1]*self.y,
            r[1][0]*self.x + r[1][1]*self.y,
        )

    def __repr__(self):
        return 'Vector(%s, %s)' % (self.x, self.y)

    def __add__(self, other):
        if isinstance(other, Vector):
            return Vector(self.x+other.x, self.y+other.y)
        elif isinstance(other, int):
            return Vector(self.x+other, self.y+other)
        else:
            raise Exception('Error, I do not know how to add Vector and "%s"' % other.__class__.__name__)

    def __radd__(self, other):
        return self.__add__(other)

    def __sub__(self, other):
        assert isinstance(other, Vector)
        return Vector(self.x-other.x, self.y-other.y)

    def __mul__(self, other):
        assert isinstance(other, (int, float))
        return Vector(self.x*other, self.y*other)

    def __div__(self, other):
        assert isinstance(other, (int, float))
        return Vector(self.x/other, self.y/other)

    def __truediv__(self, other):
        assert isinstance(other, (int, float))
        return Vector(self.x/other, self.y/other)


class Body(object):
    def __init__(self, mass, pos, vel):
        self.mass = mass
        self.mu = G*mass
        self.pos = pos
        self.vel = vel
        self.acc = Vector(0, 0)

    def update_acc(self, others):
        a = Vector(0, 0)

        for other in others:
            dpos = other.pos - self.pos

            # grav_force = G*self.mass*other.mass / dpos.magnitude()**2
            # grav_acc = grav_force / self.mass
            grav_acc = G * self.mass * other.mass / dpos.magnitude()**2 / self.mass
            angle = math.atan2(dpos.y, dpos.x)
            a += Vector.from_polar_rad(grav_acc, angle)

        self.acc = a

    def update_state(self, _others, sim_dt):
        self.vel += self.acc*sim_dt
        self.pos += self.vel*sim_dt


#
# Funcs
#

def barycenter_distance(d, m1, m2):
    return d * m2 / (m1 + m2)


def orbital_speed(mass, distance):
    return math.sqrt(G*mass/abs(distance))

#
# Main
#

def main():
    #
    # Args
    #

    if len(sys.argv) != 1+3:
        print("Usage: %s <injection_angle_deg:float> <injection_dv:float> <sim_step_per_sec:float>" % sys.argv[0])
        print("Example: %s -123.7 3150 10" % sys.argv[0])
        exit(1)

    injection_angle_deg = float(sys.argv[1])
    injection_dv = float(sys.argv[2])
    sim_step_per_sec = float(sys.argv[3])

    print("Args")
    print("\tinjection_angle_deg: %.3f" % injection_angle_deg)
    print("\tinjection_dv: %.3f" % injection_dv)
    print("\tsim_step_per_sec: %.3f" % sim_step_per_sec)
    print("")

    #
    # Vars
    #

    injection_angle = deg2rad(injection_angle_deg)

    earth_pos = Vector(-barycenter_distance(EARTH_MOON_D, EARTH_MASS, MOON_MASS), 0)
    moon_pos = Vector(+barycenter_distance(EARTH_MOON_D, MOON_MASS, EARTH_MASS), 0)
    spacecraft_pos = earth_pos + Vector.from_polar_rad(EARTH_RADIUS+INJECTION_ALTITUDE, injection_angle)

    earth_vel = Vector.from_polar_rad(earth_pos.magnitude()*ANGULAR_SPEED, -math.pi/2)
    moon_vel = Vector.from_polar_rad(moon_pos.magnitude()*ANGULAR_SPEED, math.pi/2)
    sc_s = orbital_speed(EARTH_MASS, (spacecraft_pos-earth_pos).magnitude()) + injection_dv
    spacecraft_vel = Vector.from_polar_rad(sc_s, injection_angle+math.pi/2)

    earth = Body(EARTH_MASS, earth_pos, earth_vel)
    moon = Body(MOON_MASS, moon_pos, moon_vel)
    spacecraft = Body(
        1,
        spacecraft_pos,
        spacecraft_vel,
    )

    sim_dt = 1.0 / sim_step_per_sec
    sim_dt_ms = 1000.0 / sim_step_per_sec
    t_max_ms = SIM_DURATION * 1000.0

    assert EXPORT_DT_MS >= sim_dt_ms, "sim_dt_ms must be lower than EXPORT_DT_MS"

    #
    # prints
    #

    print('Pos')
    print('\tEarth:     ', earth.pos)
    print('\tMoon:      ', moon.pos)
    print('\tSpacecraft:', spacecraft.pos)
    print('Vel')
    print('\tEarth:     ', earth.vel)
    print('\tMoon:      ', moon.vel)
    print('\tSpacecraft:', spacecraft.vel)
    # print('Grav')
    # print('\tmoon <- earth:      ', earth.grav_acc_from(moon))
    # print('\tearth <- moon:      ', moon.grav_acc_from(earth))
    # print('\tearth <- spacecraft:', spacecraft.grav_acc_from(earth))
    # print('\tmoon <- spacecraft: ', spacecraft.grav_acc_from(moon))
    print("")

    #
    # Sim
    #

    last_sim_ms = 0
    last_export_ms = 0

    poss = []

    while last_sim_ms < t_max_ms:
        earth.update_acc([moon])
        moon.update_acc([earth])
        spacecraft.update_acc([earth, moon])

        earth.update_state([moon], sim_dt)
        moon.update_state([earth], sim_dt)
        spacecraft.update_state([earth, moon], sim_dt)

        if last_sim_ms >= last_export_ms:
            alpha = -ANGULAR_SPEED * last_sim_ms/1000.0
            r = [
                [math.cos(alpha), -math.sin(alpha)],
                [math.sin(alpha), math.cos(alpha)]
            ]

            poss.append((
                earth.pos.rotate(r),
                moon.pos.rotate(r),
                spacecraft.pos.rotate(r),
            ))

            last_export_ms += EXPORT_DT_MS

        last_sim_ms += sim_dt_ms

    print("poss size: %d" % len(poss))
    scp = poss[-1][2]
    print("spacecraft pos %.0f %.0f" % (scp.x, scp.y))

    #
    # Export
    #

    with open('out.txt', 'w') as f:
        f.write('t earth_x earth_y moon_x moon_y spacecraft_x spacecraft_y\n')

        for (i, (ep, mp, scp)) in enumerate(poss):
            f.write("{:.0f} {:.0f} {:.0f} {:.0f} {:.0f} {:.0f} {:.0f}\n".format(
                i * EXPORT_DT,
                ep.x, ep.y,
                mp.x, mp.y,
                scp.x, scp.y,
            ))


main()

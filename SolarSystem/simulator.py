#!/usr/bin/env python3

#
# Adapt from https://fiftyexamples.readthedocs.io/en/latest/gravity.html
#

import math
import os

import numpy as np
import json
from astropy.time import Time
from astroquery.jplhorizons import Horizons

names = ['Mercury', 'Venus', 'Earth', 'Mars', 'Jupiter', 'Saturn', 'Uranus', 'Neptune']
nasaids = [1, 2, 3, 4, 5, 6, 7, 8]   

DAY_STEP = 10
URANUS_REVOLUTION_TIME = 30660
NUM_STEP = URANUS_REVOLUTION_TIME / DAY_STEP

G = 6.67428e-11

# Assumed scale: 100 pixels = 1AU.
AU = (149.6e6 * 1000)     # 149.6 million km, in meters.
AU_PER_DAY = 1731456.836805556
#SCALE = 250 / AU

class Horizon:
    vx = vy = vz = 0.0
    px = py = pz = 0.0
    size = 0

    def setInitialCondition(self, sim_start_date):
        data = dict(info="Solar planets database, including positions and velocities at the given date", date=sim_start_date)
        for i in range(len(names)):
            nasaid = nasaids[i]
            obj = Horizons(id=nasaid, location="@sun", epochs=Time(sim_start_date).jd, id_type='id').vectors()
            data[str(nasaid)] = {
                "name": names[i],
                "r": [np.double(obj[xi]) for xi in ['x', 'y', 'z']],
                "v": [np.double(obj[vxi]) for vxi in ['vx', 'vy', 'vz']]
            }
        with open("planets.json", 'w') as f:
            json.dump(data, f, indent=4)

    def getPlanetInitialCondition(self, positionInSolarSystem):
        if (str(positionInSolarSystem) == '0'):
            return
        with open('planets.json') as json_file:
            data = json.load(json_file)
        self.px, self.py, self.pz  = data[str(positionInSolarSystem)]['r']
        self.vx, self.vy, self.vz  = data[str(positionInSolarSystem)]['v']
        
    def getPosition (self):
        return self.px * AU, self.py * AU, self.pz * AU 

    def getSpeed (self):
        return self.vx * AU_PER_DAY, self.vy * AU_PER_DAY, self.vz * AU_PER_DAY

class Planet:
    #mass : mass in kg
    #vx, vy: x, y velocities in m/s
    #px, py: x, y positions in m
    
    name = 'Planet'
    mass = None
    vx = vy = vz = 0.0
    px = py = pz = 0.0
    vmodulo = 0.0
    dmodulo = 0.0

    dmin = float('inf')
    dmax = 0.0
    
    vmin = float('inf')
    vmax = 0.0

    def attraction(self, other):
        #Returns the force exerted upon this body by the other body.
        # Report an error if the other object is the same as this one.

        if self is other:
            raise ValueError("Attraction of object %r to itself requested" % self.name)

        # Compute the distance of the other body.
        sx, sy = self.px, self.py
        ox, oy = other.px, other.py
        dx = (ox-sx)
        dy = (oy-sy)
        d = math.sqrt(dx**2 + dy**2)

        # Report an error if the distance is zero; otherwise we'll
        # get a ZeroDivisionError exception further down.
        if d == 0:
            raise ValueError("Collision between objects %r and %r" % (self.name, other.name))

        # Compute the force of attraction
        f = G * self.mass * other.mass / (d**2)

        # Compute the direction of the force.
        theta = math.atan2(dy, dx)
        fx = math.cos(theta) * f
        fy = math.sin(theta) * f
        return fx, fy

def clean_info_on_file(bodies):
    for body in bodies:
       try:
          os.remove(body.name + ".txt")
          print('Removing ' + body + '.txt file\n')
       except:
          pass

    for body in bodies:
        planetFile = open(body.name + ".txt", "a")
        #planetFile.write("#posX, posY, velX, velY\n")
        planetFile.write("#||pos (a.u.)||, ||vel (m/s)||\n")
        planetFile.close()
   
def loop(bodies):
    timestep = 24 * 3600 * DAY_STEP
    
    # loop on (DAY_STEP * NUM_STEP) days
    step = 1
    while (True and (step <= NUM_STEP)):
        print()
        print('Step #{}'.format(step))
        for body in bodies:
            body.dmodulo = math.sqrt(body.px*body.px + body.py * body.py)
            body.vmodulo = math.sqrt(body.vx*body.vx + body.vy * body.vy)
            
            if (body.dmodulo <= body.dmin):
                body.dmin = body.dmodulo
            if (body.dmodulo >= body.dmax):
                body.dmax = body.dmodulo

            if (body.vmodulo <= body.vmin) and (body.vmin != 0):
                body.vmin = body.vmodulo
            if (body.vmodulo >= body.vmax):
                body.vmax = body.vmodulo

            print (body.name + ' ' + str(body.px/AU) + ',' + str(body.py/AU) + ',' + str(body.vx) + ',' + str(body.vy) +
                   ' ==> ' + str(body.dmodulo/AU) + ',' + str(body.vmodulo))

            # update info on file
            planetFile = open(body.name + ".txt", "a")
            #planetFile.write(str(body.px/AU) + ',' + str(body.py/AU) + ',' + str(body.vx) + ',' + str(body.vy) + 
            #                 str(body.dmodulo/AU) + ',' + str(body.vmodulo) + '\n')
            planetFile.write(str(body.dmodulo/AU) + ',' + str(body.vmodulo) + '\n')
            planetFile.close()

        step += 1

        force = {}
        for body in bodies:
            # Add up all of the forces exerted on 'body'.
            total_fx = total_fy = 0.0
            for other in bodies:
                if body is other:
                    continue
                fx, fy = body.attraction(other)
                total_fx += fx
                total_fy += fy

            # Record the total force exerted.
            force[body] = (total_fx, total_fy)

        # Update velocities based upon on the force.
        for body in bodies:
            fx, fy = force[body]
            body.vx += fx / body.mass * timestep
            body.vy += fy / body.mass * timestep

            # Update positions
            body.px += body.vx * timestep
            body.py += body.vy * timestep

    print()
    print ('Simulation ran on ' + (str(DAY_STEP * NUM_STEP))+ ' days')
    print ()
    for body in bodies:
        print (body.name + ' D(min): ' + str(body.dmin/AU) + ' D(max): ' + str(body.dmax/AU) + ' V(min): ' + str(body.vmin) + ' V(max): ' + str(body.vmax))

def main():
    sim_start_date = "1822-09-23 00:00:00"
    #sim_start_date = "1990-09-23 00:00:00"     

    print ('Get initial condition for date: ' + sim_start_date)
    h = Horizon()
    h.setInitialCondition(sim_start_date)

    # http://nssdc.gsfc.nasa.gov/planetary/factsheet/venusfact.html
    #
    # v in m/s
    # p in AU
    #
    sun = Planet()
    sun.name = 'Sun'
    sun.mass = 1.98892 * 10**30

    h.getPlanetInitialCondition(1)
    mercury = Planet()
    mercury.name = names[0]
    mercury.mass = 0.33011 * 10**24
    mercury.px, mercury.py, mercury.pz = h.getPosition ()
    mercury.vx, mercury.vy, mercury.vz = h.getSpeed ()
    #mercury.vx = 0.0
    #mercury.vy = 47.36 * 1000     

    h.getPlanetInitialCondition(2)
    venus = Planet()
    venus.name = names[1]
    venus.mass = 4.8685 * 10**24
    venus.px, venus.py, venus.pz = h.getPosition ()
    venus.vx, venus.vy, venus.vz = h.getSpeed ()
    #venus.vx = 0.0 * 1000
    #venus.vy = -35.02 * 1000

    h.getPlanetInitialCondition(3)
    earth = Planet()
    earth.name = names[2]
    earth.mass = 5.9742 * 10**24
    earth.px, earth.py, earth.pz = h.getPosition ()
    earth.vx, earth.vy, earth.vz = h.getSpeed ()
    #earth.vx = 0.0
    #earth.vy = 29.783 * 1000     

    h.getPlanetInitialCondition(4)
    mars = Planet()
    mars.name = names[3]
    mars.mass = 0.64171 * 10**24
    mars.px, mars.py, mars.pz = h.getPosition ()
    mars.vx, mars.vy, mars.vz = h.getSpeed ()
    #mars.vx = 0.0 * 1000
    #mars.vy = 24.07 * 1000

    h.getPlanetInitialCondition(5)
    jupiter = Planet()
    jupiter.name = names[4]
    jupiter.mass = 1898.19 * 10**24
    jupiter.px, jupiter.py, jupiter.pz = h.getPosition ()
    jupiter.vx, jupiter.vy, jupiter.vz = h.getSpeed ()
    #jupiter.vx = 0.0 * 1000
    #jupiter.vy = 13.06  * 1000

    h.getPlanetInitialCondition(6)
    saturn = Planet()
    saturn.name = names[5]
    saturn.mass = 568.34 * 10**24
    saturn.px, saturn.py, saturn.pz = h.getPosition ()
    saturn.vx, saturn.vy, saturn.vz = h.getSpeed ()
    #saturn.vx = 0.0 * 1000
    #saturn.vy = 9.68 * 1000

    h.getPlanetInitialCondition(7)
    uranus = Planet()
    uranus.name = names[6]
    uranus.mass = 86.813 * 10**24
    uranus.px, uranus.py, uranus.pz = h.getPosition ()
    uranus.vx, uranus.vy, uranus.vz = h.getSpeed ()
    #uranus.vx = 0.0 * 1000
    #uranus.vy = 6.80 * 1000

    h.getPlanetInitialCondition(8)
    neptune = Planet()
    neptune.name = names[7]
    neptune.mass = 102.413 * 10**24
    neptune.px, neptune.py, neptune.pz = h.getPosition ()
    neptune.vx, neptune.vy, neptune.vz = h.getSpeed ()
    #neptune.vx = 0 * 1000
    #neptune.vy = 5.43 * 1000

    bodies = [sun, mercury, venus, earth, mars, jupiter, saturn, uranus]
    clean_info_on_file(bodies)

    loop(bodies)
    
if __name__ == '__main__':
    main()

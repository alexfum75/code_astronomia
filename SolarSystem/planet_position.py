#!/usr/bin/env python

#Fetch planet information from nasa.org and store it in a json file.

import numpy as np
import json
from astropy.time import Time
from astroquery.jplhorizons import Horizons

#      X-component of position vector (au)
#      Y      Y-component of position vector (au)
#      Z      Z-component of position vector (au)
#      VX     X-component of velocity vector (au/day)                           
#      VY     Y-component of velocity vector (au/day)                           
#      VZ     Z-component of velocity vector (au/day)                           
#      LT     One-way down-leg Newtonian light-time (day)
#      RG     Range; distance from coordinate center (au)
#      RR     Range-rate; radial velocity wrt coord. center (au/day)

sim_start_date = "2013-07-12 00:00:00"     # simulating a solar system starting from this date
names = ['Mercury', 'Venus', 'Earth', 'Mars', 'Jupiter', 'Saturn', 'Uranus', 'Neptune']
sizes = [0.38, 0.95, 1. , 0.53, 317.8, 95.16, 14.54, 17.15]
nasaids = [1, 2, 3, 4, 5, 6, 7, 8]   

data = dict(info="Solar planets database, including positions and velocities at the given date", date=sim_start_date)

for i in range(8):
    nasaid = nasaids[i]
    obj = Horizons(id=nasaid, location="@sun", epochs=Time(sim_start_date).jd, id_type='id').vectors()
    data[str(nasaid)] = {
        "name": names[i],
        "size": sizes[i],
        "r": [np.double(obj[xi]) for xi in ['x', 'y', 'z']],
        "v": [np.double(obj[vxi]) for vxi in ['vx', 'vy', 'vz']]
    }

with open("planets.json", 'w') as f:
    json.dump(data, f, indent=4)

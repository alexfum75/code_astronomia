#!/usr/bin/env python3
'''
TLI is Translunar Injection, the burn of the S-IVB that takes Apollo 11 out of Earth
 orbit and onto the Moon. The burn will raise Apollo's inertial velocity from 7,800 to 11,000 
 metres per second which will send it on a very long elliptical orbit with an apogee well beyond 
 the Moon. The Moon's gravitational field will interfere with this trajectory, changing it to 
 one that will bring the spacecraft around its far side and on a path back to Earth, a so-called 
 free-return trajectory.
https://history.nasa.gov/afj/ap11fj/02earth-orbit-tli.html

Midway through the second revolution in Earth parking orbit,
the S-IVB third-stage engine will restart at 2:44:15 GET over the
mid-Pacific just south of the equator to inject Apollo 11 toward
the Moon. The velocity will increase from 25,567 fps to 35,533 fps
at TLI cutoff--a velocity increase of 991 fps. The TLI burn is
targeted for about 6 fps overspeed to compensate for the later SPS
evasive maneuver after LM extraction. TLI will place Apollo 11 on
a free-return circumlunar trajectory from which midcourse corrections
if necessary could be made with the SM RCS thrusters. Entry from a
free-return trajectory would be at 10:37 a.m. EDT July 22 at 14.9
degrees south latitude by 174.9 east longitude after a flight time
of 145 hrs 04 min. 

'''

from matplotlib import pyplot as plt
from plot_common import (
    EARTH_RADIUS,
    MOON_RADIUS,
    COLOR_EARTH,
    COLOR_MOON,
    COLOR_MOON_ORBIT,
    COLOR_SC_ORBIT,
    Plot,
)


class PlotFreeReturn(Plot):
    def data_prepare(self):
        self.data_prepared = (
            self.data_raw['earth_pos'][0][:int(self.config['point_plotted'])],
            self.data_raw['earth_pos'][1][:int(self.config['point_plotted'])],
            self.data_raw['moon_pos'][0][:int(self.config['point_plotted'])],
            self.data_raw['moon_pos'][1][:int(self.config['point_plotted'])],
            self.data_raw['sc_pos'][0][:int(self.config['point_plotted'])],
            self.data_raw['sc_pos'][1][:int(self.config['point_plotted'])],
        )

        print('plot %d/%d points' % (self.config['point_plotted'], len(self.data_raw['earth_pos'][0])))

    def plot(self):
        ax = self.ax
        earth_xs, earth_ys, moon_xs, moon_ys, sc_xs, sc_ys = self.data_prepared

        # orbit: sc initial
        # ax.add_artist(plt.Circle((earth_xs[0], earth_ys[0]), EARTH_RADIUS+185*1000, edgecolor=COLOR_ORBIT_LEO, facecolor='none'))

        # earth and moon bodies
        ax.add_artist(plt.Circle((earth_xs[0], earth_ys[0]), EARTH_RADIUS, color=COLOR_EARTH))
        ax.add_artist(plt.Circle((moon_xs[0], moon_ys[0]), MOON_RADIUS, color=COLOR_MOON))

        # trajectories
        # plt.plot(earth_xs, earth_ys, '-', color=COLOR_EARTH_ORBIT)
        if self.config['show_moon_orbit']:
            plt.plot(moon_xs, moon_ys, '-', color=COLOR_MOON_ORBIT)
        plt.plot(sc_xs, sc_ys,  color = self.config['color'], label = self.config['param'])
        plt.grid(True)

# THRUST
colorLine = 1
colorName = ['red','blue','yellow','green','purple','black','orange','green','aqua','brown','peru','pink','navy','seagreen','tan','darkgreen']
simDay = 10
angle = -123.7
colorLine = 1
for deltaV in range(3145, 3155, 2):
	baseFile = 'deltav\\out_' + str(angle) + '_' + str(deltaV) + '.0'
	inFile = baseFile + '.txt'
	outFile = baseFile + '.svg'
	parValue = 'ΔV = ' + str(deltaV) + ' α = ' + str(angle)
	conf = {
		'xlim': (-40*10**6, 450*10**6),
		'ylim': (-390*10**6, 400*10**6),
		'infile': inFile,
		'outfile': outFile,
		'point_plotted': simDay * 86400/50,
		'show_moon_orbit': True,
		'param': parValue,
		'color': colorName[colorLine]
	}
	p = PlotFreeReturn (conf)
	p.go()
	colorLine = colorLine + 1
p.display('Free Return Trajectory for different ΔV from LEO 100 nm after T = 10 days')

# ANGLE
colorLine = 1
for angle in range(111, 133, 2):
    deltaV = 3150
    baseFile = 'angle\\out_-' + str(angle) + '.7_' + str(deltaV) + '.0'
    inFile = baseFile + '.txt'
    outFile = baseFile + '.svg'
    parValue = 'ΔV = ' + str(deltaV) + ' α = ' + str(angle) + '.7'	
    conf = {
        'xlim': (-40*10**6, 450*10**6),
        'ylim': (-390*10**6, 400*10**6),
        'infile': inFile,
        'outfile': outFile,
        'point_plotted': simDay * 86400/50,
        'show_moon_orbit': True,
        'param': parValue,
        'color': colorName[colorLine]
    }
    p = PlotFreeReturn (conf)
    p.go()
    colorLine = colorLine + 1
p.display('Free Return Trajectory for different α from LEO 100 nm after T = 10 days')

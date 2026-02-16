#!/usr/bin/env python3

import os
import matplotlib
from matplotlib import pyplot as plt
import numpy as np
import matplotlib.lines as mlines


def barycenter_distance(d, m1, m2):
    return d * m2 / (m1 + m2)


SUN_MASS = 1.9885*10**30

EARTH_MASS = 5.97237*10**24
EARTH_RADIUS = 6.378*10**6
EARTH_SEMIMAJOR_AXIS = 1.49598023*10**11

MOON_MASS = 7.342*10**22
MOON_RADIUS = 1.737*10**6
MOON_SEMIMAJOR_AXIS = 3.84399*10**8

EARTH_MOON_DISTANCE = 3.84402 * 10**8
EARTH_POS = (-barycenter_distance(EARTH_MOON_DISTANCE, EARTH_MASS, MOON_MASS), 0)
MOON_POS = (+barycenter_distance(EARTH_MOON_DISTANCE, MOON_MASS, EARTH_MASS), 0)


COLOR_EARTH = 'darkblue'
COLOR_MOON = 'grey'
COLOR_MOON_ORBIT = 'silver'
COLOR_SC_ORBIT = 'black'
COLOR_ORBIT_LEO = 'grey'
COLOR_SOI = 'red'


def get_script_folder():
    return os.path.dirname(os.path.abspath(__file__))


class Plot(object):
    def __init__(self, config):
        """
        config
            TODO
            xlim
            ylim
            infile
            outfile
        """
        self.config = config
        self.data_raw = {}
        self.data_prepared = {}

        self.ax = plt.gca()
        self.fig = plt.gcf()
        self.figsizex, self.figsizey = self.fig.get_size_inches()

        if 'infile' in self.config:
            self.load_data_raw(config['infile'])

    def load_data_raw(self, infile):
        with open('%s\\%s' % (get_script_folder(), infile), 'r') as f:
            _header, *data_raw = f.readlines()

        data_parsed = [[int(tup) for tup in line.strip().split()] for line in data_raw]
        _time, earth_xs, earth_ys, moon_xs, moon_ys, sc_xs, sc_ys = np.array(data_parsed).transpose()

        self.data_raw = {
            'earth_pos': (earth_xs, earth_ys),
            'moon_pos': (moon_xs, moon_ys),
            'sc_pos': (sc_xs, sc_ys),
        }

    def go(self):
        print('=== %s ===' % self.config['outfile'])
        self.data_prepare()
        self.configure_axis()
        self.plot()
        self.savefig()
		
    def display(self, title):
        plt.legend(loc = 0)
        plt.title(title)
        plt.show()

    def data_prepare(self):
        pass

    def plot(self):
        pass

    def configure_axis(self):
        ax = self.ax
        figsizex = self.figsizex
        figsizey = self.figsizey
        xlim = self.config['xlim']
        ylim = self.config['ylim']
        param = self.config['param']

        # configure size

        ax.set_aspect(1.0)

        ax.set_xlim(xlim)

        if ylim == 'auto':
            val = (xlim[1]-xlim[0]) * (figsizey/figsizex) / 2
            ylim = (-val, +val)
            print('ylim: auto')
        else:
            ideal_y = (xlim[1]-xlim[0]) * (figsizey/figsizex)
            current_y = ylim[1] - ylim[0]
            diff = ideal_y - current_y
            ylim = (ylim[0]-diff/2, ylim[1]+diff/2)
            print('ylim: current=%d, ideal=%d, diff=%d' % (current_y/10**6, ideal_y/10**6, diff/10**6))
        ax.set_ylim(ylim)

        print('Size: %d x %d' % ((xlim[1]-xlim[0])/10**6, (ylim[1]-ylim[0])/10**6))

        # configure axis

        def formatter(x, p):
            return format(x/10**6, ',').replace(',', ' ')

        ax.get_xaxis().set_major_formatter(matplotlib.ticker.FuncFormatter(formatter))
        ax.get_yaxis().set_major_formatter(matplotlib.ticker.FuncFormatter(formatter))

        ax.set_xlabel('Unit: 1000 km')
        ax.set_ylabel('Unit: 1000 km')


    def savefig(self):
        scale = 1.5

        plt.rcParams['svg.hashsalt'] = 'constantseed'  # https://github.com/matplotlib/matplotlib/pull/7748

        self.fig.set_size_inches((scale*self.figsizex, scale*self.figsizey))
        self.fig.savefig('%s/%s' % (get_script_folder(), self.config['outfile']), bbox_inches='tight')

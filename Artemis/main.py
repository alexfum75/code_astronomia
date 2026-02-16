__author__ = "Alessandro Fumagalli"
__copyright__ = "Copyright 2023, articolidiastronomia.com"
__credits__ = ["Alessandro Fumagalli"]
__license__ = "GPL"
__maintainer__ = "Alessandro Fumagalli"

import numpy as np

import artemis_nav
import matplotlib.pyplot as plt
import pandas as pd
from math_utility import pythagoras, norma
from matplotlib.dates import DayLocator, DateFormatter

database = r"data\artemis.db"
artemis_barycenter_state_vector = r"data\artemis.barycenter.state_vector"
moon_barycenter_state_vector = r"data\moon.barycenter.state_vector"
earth_barycenter_state_vector = r"data\earth.barycenter.state_vector"


def read_data(csv_file):
    print(f'Reading navigation data: {csv_file} ')
    df = pd.read_csv(csv_file, sep=',', header=0)
    df.rename(columns={"Calendar Date (TDB)": "Calendar Date"}, inplace=True)

    # rework
    df['Calendar Date'] = df['Calendar Date'].replace(' A.D. ', '', regex=True)
    df.drop(columns=df.columns[-1], axis=1, inplace=True)
    df['Calendar Date'] = pd.to_datetime(df['Calendar Date'])

    return df


def createDateLabel(timestamp):
    token_data = str(timestamp).split(' ')
    return token_data[0]


def df_get_nav_point(df):
    nav_point_dict = {}

    for index, row in df.iterrows():
        x = float(row['X'])
        y = float(row['Y'])
        z = float(row['Z'])
        vx = float(row['VX'])
        vy = float(row['VY'])
        vz = float(row['VZ'])
        artemis_nav_obj = artemis_nav.ArtemisObject()
        dat = row['Calendar Date']

        artemis_nav_obj.setTimeStamp(dat)
        tuple_pos = (x, y, z)
        artemis_nav_obj.setPos(tuple_pos)
        tuple_speed = (vx, vy, vz)
        artemis_nav_obj.setSpeed(tuple_speed)
        nav_point_dict[artemis_nav_obj.getArtemisDate()] = artemis_nav_obj

    nav_point_sort = dict(sorted(nav_point_dict.items()))
    return nav_point_sort


def print_nav_point(nav_point):
    for key, value in nav_point.items():
        value.printStateVector()


def plot_nav_point_3D(nav_point, view):
    print(f'Plotting navigation points with view: {view} ')
    plt.figure(figsize=(15, 15))
    ax = plt.axes(projection='3d')
    ax.view_init(view[0], view[1])

    artemis_timestamp = []
    artemis_pos = []
    moon_pos = []

    for trace_color, state_vector in nav_point.items():
        x_pos = []
        y_pos = []
        z_pos = []
        now = '2023-11-11'
        for time, value in state_vector.items():
            vector_pos = state_vector[time].getPos()
            vector_timestamp = state_vector[time].getArtemisDate()
            (x, y, z) = vector_pos
            label_date = createDateLabel(vector_timestamp)

            if now != label_date:
                now = label_date
                new_date = now.replace('-', '')
                ax.scatter(x, y, z, marker='x', color='black', s=100, label='_nolegend_')
                if trace_color != 'blue':  # not the Earth
                    ax.text(x, y, z, str(new_date), size=7)

            x_pos.append(x)
            y_pos.append(y)
            z_pos.append(z)
            if trace_color == 'red':
                artemis_timestamp.append(vector_timestamp)
                artemis_pos.append(vector_pos)
            if trace_color == 'gray':
                moon_pos.append(vector_pos)
        ax.scatter3D(x_pos, y_pos, z_pos, marker='.', color=trace_color, s=250)

    artemis_distance = []
    for i in range(len(moon_pos)):
        artemis_distance.append(pythagoras(moon_pos[i], artemis_pos[i]))

    ax.grid(color='green', linestyle='--', linewidth=1)
    ax.set_title(f"ARTEMIS 1 Trajectory", fontsize=25)
    ax.set_xlabel("x (Km)")
    ax.set_ylabel("y (Km)")
    ax.set_zlabel("z (Km)")

    ax.set_xlim(-400000, 400000)
    ax.set_ylim(-400000, 400000)
    ax.set_zlim(-150000, 150000)

    leg_list = ['Artemis I', 'Moon ', 'Earth']
    ax.legend(leg_list, loc='upper left', title="Legenda", markerfirst=False, fontsize=10)
    suffix = str(view[0]) + '_' + str(view[1])
    plt.savefig(f"figure/Artemis_trajectory_{suffix}.png", dpi=600)


def plot_nav_distance(nav_point):
    print(f'Plotting Artemis distance Artemis vs Moon')
    plt.figure(figsize=(15, 15))

    artemis_timestamp = []
    artemis_pos = []
    moon_pos = []

    for trace_color, state_vector in nav_point.items():
        for time, value in state_vector.items():
            vector_pos = state_vector[time].getPos()
            vector_timestamp = state_vector[time].getArtemisDate()
            if trace_color == 'red':
                artemis_timestamp.append(vector_timestamp)
                artemis_pos.append(vector_pos)
            if trace_color == 'gray':
                moon_pos.append(vector_pos)

    artemis_distance = []
    for i in range(len(moon_pos)):
        artemis_distance.append(pythagoras(moon_pos[i], artemis_pos[i]))

    axs = plt.axes()
    axs.grid(color='green', linestyle='--', linewidth=1)
    axs.set_title(f"ARTEMIS 1 distance", fontsize=25)
    axs.set_xlabel("Baricentric Dynamical Time")
    axs.set_ylabel("Distance Moon-Artemis (Km)")
    plt.plot(artemis_timestamp, artemis_distance)
    axs.xaxis.set_major_locator(DayLocator(interval=1))
    axs.xaxis.set_major_formatter(DateFormatter('%Y%m%d'))
    tick = np.arange(0, 400000, 10000)
    axs.set_yticks(tick)
    plt.gcf().autofmt_xdate(rotation=650)
    plt.savefig("figure/Artemis_distance.png", dpi=600)


def plot_nav_speed(nav_point):
    print(f'Plotting Artemis speed')
    plt.figure(figsize=(15, 15))

    artemis_speed = []
    artemis_timestamp = []

    for trace_color, state_vector in nav_point.items():
        for time, value in state_vector.items():
            vector_speed = state_vector[time].getSpeed()
            vector_timestamp = state_vector[time].getArtemisDate()
            if trace_color == 'red':
                artemis_timestamp.append(vector_timestamp)
                artemis_speed.append(norma(vector_speed))

    axs = plt.axes()
    axs.grid(color='green', linestyle='--', linewidth=1)
    axs.set_title(f"ARTEMIS 1 Speed, fontsize=25")
    axs.set_xlabel("Baricentric Dynamical Time")
    axs.set_ylabel("Speed (Km/s)")
    plt.plot(artemis_timestamp, artemis_speed)
    axs.xaxis.set_major_locator(DayLocator(interval=1))
    axs.xaxis.set_major_formatter(DateFormatter('%Y%m%d'))
    tick = np.arange(0, 15, 0.5)
    axs.set_yticks(tick)
    plt.gcf().autofmt_xdate(rotation=650)
    plt.savefig("figure/Artemis_speed.png", dpi=600)


if __name__ == '__main__':
    print(f'*** START ***')

    nav_point_list = {}

    artemis_df = read_data(artemis_barycenter_state_vector)
    artemis_nav_point_sort_dict = df_get_nav_point(artemis_df)
    nav_point_list['red'] = artemis_nav_point_sort_dict

    moon_df = read_data(moon_barycenter_state_vector)
    moon_nav_point_sort_dict = df_get_nav_point(moon_df)
    nav_point_list['gray'] = moon_nav_point_sort_dict

    earth_df = read_data(earth_barycenter_state_vector)
    earth_nav_point_sort_dict = df_get_nav_point(earth_df)
    nav_point_list['blue'] = earth_nav_point_sort_dict

    plot_nav_point_3D(nav_point_list, (-170, 60))
    plot_nav_point_3D(nav_point_list, (90, 90))
    plot_nav_speed(nav_point_list)
    plot_nav_distance(nav_point_list)

    print(f'*** DONE ***')

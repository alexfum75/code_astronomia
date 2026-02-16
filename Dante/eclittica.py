import matplotlib.pyplot as plt
import numpy as np
import astropy.units as u
from astropy.coordinates import SkyCoord, get_constellation

# 1. Generate points along the ecliptic (lat=0, long=0-360)
lon = np.linspace(0, 360, 500) * u.deg
lat = np.zeros(500) * u.deg
ecliptic_coords = SkyCoord(lon=lon, lat=lat, frame='barycentrictrueecliptic')
ecliptic_icrs = ecliptic_coords.transform_to('icrs')
ra_rad = ecliptic_icrs.ra.wrap_at(180 * u.deg).radian
dec_rad = ecliptic_icrs.dec.radian

zodiac_top = SkyCoord(lon=lon, lat=8*u.deg, frame='barycentrictrueecliptic')
zodiac_top_icrs = zodiac_top.transform_to('icrs')
ra_zodiac_top_rad = zodiac_top_icrs.ra.wrap_at(180 * u.deg).radian
dec_zodiac_top_rad = zodiac_top_icrs.dec.radian

zodiac_bottom = SkyCoord(lon=lon, lat=-8*u.deg, frame='barycentrictrueecliptic')
zodiac_bottom_icrs = zodiac_bottom.transform_to('icrs')
ra_zodiac_bottom_rad = zodiac_bottom_icrs.ra.wrap_at(180 * u.deg).radian
dec_zodiac_bottom_rad = zodiac_bottom_icrs.dec.radian

# 4. Plot using Matplotlib
plt.figure(figsize=(16, 10))
ax = plt.subplot(111, projection='aitoff', aspect='equal')
ax.scatter(ra_rad, dec_rad, s=2, marker='.', color='red', label='Eclittica')
ax.scatter(ra_zodiac_top_rad, dec_zodiac_top_rad, marker='.', s=2, color='green', label='Fascia superiore dello Zodiaco')
ax.scatter(ra_zodiac_bottom_rad, dec_zodiac_bottom_rad, marker='.', s=2, color='green', label='Fascia inferiore dello Zodiaco', linestyle='-')

constellation_icrs = ecliptic_coords.transform_to('icrs')
short_name = get_constellation(ecliptic_coords, short_name=True)
for i, name in enumerate(short_name):
    if (i % 40 != 0):
        continue
    ax.text(ra_rad[i], dec_rad[i], short_name[i], color='yellow', size=16)

rng = np.random.default_rng()
ra_random = rng.uniform(0, 360, 110) * u.degree
dec_random = np.linspace(-90, 90, 110) * u.deg
c = SkyCoord(ra=ra_random, dec=dec_random, frame='icrs')
ra_rad = c.ra.wrap_at(180 * u.deg).radian
dec_rad = c.dec.radian
#ax.text(ra_rad[i], dec_rad[i], name, color='white')
ax.scatter(ra_rad, dec_rad, color='white', s=5)

ax.grid(True)
ax.set_title("Eclittica e zodiaco", size=16)
ax.set_facecolor('black')

plt.legend(prop = { "size": 16 })
#plt.show()
plt.savefig('eclittica.png',)


import numpy as np
import matplotlib.pyplot as plt
from skyfield.api import load


def plot_dark_ecliptic_map():
    ts = load.timescale()

    # 1. Calcolo del percorso di precessione (26.000 anni)
    #years = np.linspace(-13000, 13000, 1000)
    years = np.linspace(13000, -13000, 1000)
    print(years)
    times = ts.utc(years, 1, 1)

    # Costante obliquità dell'eclittica (circa 23.44 gradi)
    EPS = np.radians(23.44)

    ra_path, r_path = [], []
    for t in times:
        m = t.M.T
        ncp_icrs = np.dot(m, [0, 0, 1])

        # Conversione a coordinate eclittiche
        x, y, z = ncp_icrs
        ye = y * np.cos(EPS) + z * np.sin(EPS)
        ze = -y * np.sin(EPS) + z * np.cos(EPS)
        xe = x

        lon = np.arctan2(ye, xe)
        lat = np.degrees(np.arcsin(ze))

        ra_path.append(lon)
        r_path.append(90 - lat)  # Distanza dal centro (Polo Eclittica)

    # 2. Database Stelle Principali (RA ore, Dec gradi)
    stars_main = {
        "Polaris": (2.5, 89.3), "Vega": (18.6, 38.8), "Thuban": (14.1, 64.4),
        "Deneb": (20.7, 45.3), "Capella": (5.3, 46.0),
        "Kochab": (14.8, 74.2), "Alderamin": (21.3, 62.6),
        "Betelgeuse": (5.9, 7.4), "Sirius": (6.7, -16.7),
        "Rigel": (5.2, -8.2),
    }

    # 3. Setup Grafico
    fig = plt.figure(figsize=(8, 8), facecolor='black')
    ax = fig.add_subplot(111, projection='polar')
    ax.set_facecolor('black')

    # Disegna il cerchio di precessione
    ax.plot(ra_path, r_path, color='#FF3333', lw=2.5, alpha=0.9, label="Precessione")

    # 4. Funzione di conversione per le stelle
    def to_ecliptic(ra_h, dec_d):
        ra_r = np.radians(ra_h * 15)
        dec_r = np.radians(dec_d)
        x = np.cos(ra_r) * np.cos(dec_r)
        y = np.sin(ra_r) * np.cos(dec_r)
        z = np.sin(dec_r)
        ye = y * np.cos(EPS) + z * np.sin(EPS)
        ze = -y * np.sin(EPS) + z * np.cos(EPS)
        xe = x
        return np.arctan2(ye, xe), 90 - np.degrees(np.arcsin(ze))

    # 5. Aggiunta Stelle di Sfondo (Casuali per densità)
    np.random.seed(42)
    for _ in range(100):
        rand_ra = np.random.uniform(0, 2 * np.pi)
        rand_r = np.random.uniform(0, 90)
        ax.scatter(rand_ra, rand_r, s=np.random.uniform(1, 5), color='#FFD700', alpha=0.4)

    # 6. Disegna Stelle Principali
    for name, (ra_h, dec_d) in stars_main.items():
        lon, r_dist = to_ecliptic(ra_h, dec_d)
        if r_dist < 30:  # Mostra solo stelle visibili nella mappa
            #print(f"{name}  {r_dist}")
            ax.scatter(lon, r_dist, s=100, color='#FFD700', edgecolors='white', marker='*', zorder=10)
            ax.text(lon, r_dist + 3, name, color='white', fontsize=9, ha='center', alpha=0.8)

    # 7. Marcatori Temporali sul cerchio
    for i in [0, 250, 500, 750]:
        y = int(years[i])
        print (y)
        label = f"{y}" if y > 0 else f"{abs(y)} BC"
        ax.text(ra_path[i], r_path[i] - 4, label, color='#FF3333', fontweight='bold', fontsize=6)

    # Centro: Polo Eclittica
    ax.scatter(0, 0, s=150, color='#0066FF', marker='+', label="Polo Eclittica")

    # 8. Rifiniture estetiche
    ax.set_theta_zero_location('N')
 #   ax.set_theta_direction(-1)
    ax.set_ylim(0, 90)

    # Colore griglia e etichette
    ax.grid(True, color='white', alpha=0.2, linestyle='--')
    plt.setp(ax.get_yticklabels(), color="white", alpha=0.5)
    plt.setp(ax.get_xticklabels(), color="white", alpha=0.7)

    plt.title("Ciclo di Precessione",
              color='white', pad=40, fontsize=16, fontweight='bold')

    #legend = ax.legend(bbox_to_anchor=(1.15, 0), facecolor='black', edgecolor='white')
    #plt.setp(legend.get_texts(), color='white')

    plt.legend()
    plt.show()
    plt.savefig('precessione.png')


if __name__ == "__main__":
    plot_dark_ecliptic_map()
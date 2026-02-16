#https://starplot.dev/tutorial/04/

import yaml
from starplot import MapPlot, Projection, _
from starplot.styles import PlotStyle, extensions
#https://starplot.dev/reference-styling/
#https://starplot.dev/reference-styling/#starplot.styles.LegendStyle
#style = PlotStyle.load_from_file("costellazioni.yaml")

coordinateToken = [ "ra_min", "ra_max", "dec_min", "dec_max" ]

def readConstellations (fileName):
    constellationList = None
    with open(fileName) as stream:
        try:
            constellationList = yaml.safe_load(stream)
        except yaml.YAMLError as exc:
            print(exc)
    return constellationList

if __name__ == "__main__":
    style = PlotStyle().extend(
        extensions.BLUE_DARK,
        extensions.MAP,
        {
            "legend": {
                "location": "upper right",  # show legend inside map
                "num_columns": 3,
                "background_alpha": 1,
            },
            #"star":{
            #    "label": {
            #        "font_size" :  15
            #    }
            #},
            #"title": {
            #    "font_size" : 110,
            #    "font_weight": "bold",
            #    "anchor_point" : "center"
            #}
            "figure_background_color": "hsl(212, 27%, 48%)",
        }
    )
    constellationList = readConstellations("costellazioni.yaml")
    constellationRoot = constellationList['costellazioni']
    for element in constellationRoot:
        _ra_min = float(constellationRoot[element]['ra_min']) * 15
        _ra_max = float(constellationRoot[element]['ra_max']) * 15
        _dec_min = float(constellationRoot[element]['dec_min'])
        _dec_max = float(constellationRoot[element]['dec_max'])
        p = MapPlot(
            projection=Projection.MERCATOR, #MILLER,  # specify a non-perspective projection
            ra_min = _ra_min,  # limit the map to a specific area
            ra_max = _ra_max, # larghezza
            dec_min = _dec_min, # altezza
            dec_max = _dec_max,
            resolution = 4000,
            autoscale = True,  # automatically adjust the scale based on the resolution
            style = style,
        )
        p.constellations()
        p.constellation_borders()
        p.gridlines()  # add gridlines

        p.stars(where=[_.magnitude < 12], bayer_labels=True, catalog="big-sky-mag11",)
        p.nebula(where=[(_.magnitude < 12) | (_.magnitude.isnull())], where_labels=[True])
        p.open_clusters(where=[(_.magnitude < 12) | (_.magnitude.isnull())], where_labels=[True])

        p.ecliptic()
        #p.milky_way()
        p.legend()
        p.constellation_labels()  # Plot the Constellation labels last for best placement

        print((f"Saving picture for {element} Constellation ..."))
        p.title(f"{element}")
        p.export(f"{element}.png",  transparent=True)
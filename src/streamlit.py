import pandas as pd
from mplsoccer import Radar, FontManager
import matplotlib.pyplot as plt
import src.plotting as pl
import seaborn as sns
import plotly.express as px

def carga_data():
    data = pd.read_csv("./data/average_cleaned.csv")
    return data
    
def lista_jugadores():
    data = carga_data()
    return list(data.PLAYER_NAME.unique())

def shots_data():
    datos = pd.read_csv("./data/database_shots.csv")
    return datos

def lista_tiradores(): 
    datos = shots_data()
    return list(datos.name.unique())
    
def clusters_data():
    datos = pd.read_csv("./data/clusters.csv")
    return datos

def lista_clusters():
    datos = clusters_data()
    return list(datos.Cluster.unique())

def cluster_description(cluster):
    datos = pd.read_csv("./data/cluster_description.csv")
    data = datos[(datos["Cluster"]== f"{cluster}")]
    return data
 
def grafico_cl(cluster):
    data = clusters_data()
    data = data[(data["Cluster"]== f"{cluster}")]
    return data

def grafico(player):
    data = carga_data()
    data = data[(data["PLAYER_NAME"]== f"{player}")]
    return data


def radar_mosaic(radar_height=0.915, title_height=0.06, figheight=14):
    """ Create a Radar chart flanked by a title and endnote axes.

    Parameters
    ----------
    radar_height: float, default 0.915
        The height of the radar axes in fractions of the figure height (default 91.5%).
    title_height: float, default 0.06
        The height of the title axes in fractions of the figure height (default 6%).
    figheight: float, default 14
        The figure height in inches.

    Returns
    -------
    fig : matplotlib.figure.Figure
    axs : dict[label, Axes]
    """
    if title_height + radar_height > 1:
        error_msg = 'Reduce one of the radar_height or title_height so the total is ≤ 1.'
        raise ValueError(error_msg)
    endnote_height = 1 - title_height - radar_height
    figwidth = figheight * radar_height
    figure, axes = plt.subplot_mosaic([['title'], ['radar'], ['endnote']],
                                      gridspec_kw={'height_ratios': [title_height, radar_height,
                                                                     endnote_height],
                                                   # the grid takes up the whole of the figure 0-1
                                                   'bottom': 0, 'left': 0, 'top': 1,
                                                   'right': 1, 'hspace': 0},
                                      figsize=(figwidth, figheight))
    axes['title'].axis('off')
    axes['endnote'].axis('off')
    return figure, axes


def statsbomb(player):


    URL1 = ('https://github.com/googlefonts/SourceSerifProGFVersion/blob/main/'
            'fonts/SourceSerifPro-Regular.ttf?raw=true')
    serif_regular = FontManager(URL1)
    URL2 = ('https://github.com/googlefonts/SourceSerifProGFVersion/blob/main/'
            'fonts/SourceSerifPro-ExtraLight.ttf?raw=true')
    serif_extra_light = FontManager(URL2)
    URL3 = ('https://github.com/google/fonts/blob/main/ofl/rubikmonoone/'
            'RubikMonoOne-Regular.ttf?raw=true')
    rubik_regular = FontManager(URL3)
    URL4 = 'https://github.com/googlefonts/roboto/blob/main/src/hinted/Roboto-Thin.ttf?raw=true'
    robotto_thin = FontManager(URL4)
    URL5 = 'https://github.com/googlefonts/roboto/blob/main/src/hinted/Roboto-Regular.ttf?raw=true'
    robotto_regular = FontManager(URL5)
    URL6 = 'https://github.com/googlefonts/roboto/blob/main/src/hinted/Roboto-Bold.ttf?raw=true'
    robotto_bold = FontManager(URL6)


    tiros = pd.read_csv("./data/average_cleaned.csv")
    zones = ["PLAYER_NAME", "% LEFT-CORNER-3","% LEFT-MIDR-2","% LEFT-ELBOW-3","% LEFT-ELB/CENT-2",
         "% LEFT-CENTER-3","% LEFT-PAINT","% RIGHT-PAINT","% RIGHT-CENTER-3","% RIGHT-ELB/CENT-2",
         "% RIGHT-ELBOW-3","% RIGHT-MIDR-2","% RIGHT-CORNER-3"]
    player_polygon = tiros[zones]
    values = player_polygon[player_polygon["PLAYER_NAME"] == player]
    values = values.values.tolist()
    values = values[0][1:]
    # parameter names of the statistics we want to show
    params = ["% LEFT-CORNER-3","% LEFT-MIDR-2","% LEFT-ELBOW-3","% LEFT-ELB/CENT-2",
             "% LEFT-CENTER-3","% LEFT-PAINT","% RIGHT-PAINT","% RIGHT-CENTER-3","% RIGHT-ELB/CENT-2",
             "% RIGHT-ELBOW-3","% RIGHT-MIDR-2","% RIGHT-CORNER-3"]

    # The lower and upper boundaries for the statistics
    low =  [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    high = [0.99,0.99,0.99,0.99,0.99,0.99,0.99,0.99,0.99,0.99,0.99,0.99,]
    
    radar = Radar(params, low, high,
              # whether to round any of the labels to integers instead of decimal places
              round_int=[False]*12,
              num_rings=4,  # the number of concentric circles (excluding center circle)
              # if the ring_width is more than the center_circle_radius then
              # the center circle radius will be wider than the width of the concentric circles
              ring_width=1, center_circle_radius=1)
    
    # creating the figure using the function defined above:
    fig, axs = radar_mosaic(radar_height=0.915, title_height=0.06, figheight=14)

    # plot the radar
    radar.setup_axis(ax=axs['radar'], facecolor='None')
    rings_inner = radar.draw_circles(ax=axs['radar'], facecolor='#28252c', edgecolor='#39353f', lw=1.5)
    radar_output = radar.draw_radar(values, ax=axs['radar'])
    radar_poly, rings_outer, vertices = radar_output
    range_labels = radar.draw_range_labels(ax=axs['radar'], fontsize=25, color='#fcfcfc',
                                       fontproperties=robotto_thin.prop)
    param_labels = radar.draw_param_labels(ax=axs['radar'], fontsize=25, color='#fcfcfc',
                                       fontproperties=robotto_regular.prop)

    # adding the endnote and title text (these axes range from 0-1, i.e. 0, 0 is the bottom left)
    # Note we are slightly offsetting the text from the edges by 0.01 (1%, e.g. 0.99)
    endnote_text = axs['endnote'].text(0.99, 0.5, 'Inspired By: StatsBomb / Rami Moghadam',
                                   color='#fcfcfc', fontproperties=robotto_thin.prop,
                                   fontsize=15, ha='right', va='center')
    title1_text = axs['title'].text(0.01, 0.65, player, fontsize=25,
                                fontproperties=robotto_bold.prop,
                                ha='left', va='center', color='#e4dded')

    fig.set_facecolor('#121212')
    # save the figure
    fig.tight_layout()
    plt.savefig('./images/plot.png', dpi=300)



def mapa(player):
    mapita = pd.read_csv("./data/database_shots.csv")
    mapita["coord_x"] = pd.to_numeric(mapita["coord_x"], downcast="float")
    mapita["coord_y"] = pd.to_numeric(mapita["coord_y"], downcast="float")
    mapita["coord_y"] = mapita["coord_y"] * (-1)
    listita = mapita[mapita["name"] == player]
    listita_1 = pd.DataFrame(listita, columns = ['name', "shot", 'coord_x','coord_y'])
    listita_1.shot = listita_1.shot.apply(lambda x: 'in' if 'in' in x else x)
    listita_1.shot = listita_1.shot.apply(lambda x: 'in' if 'dunk' in x else x)
    listita_1.shot = listita_1.shot.apply(lambda x: 'out' if 'out' in x else x)
    plt.figure(figsize=(18,20))
    pl.draw_court(outer_lines=True)
    plt.axis('off')
    plt.xlim(0,260)
    plt.ylim(-283,0)
    markers = {"#local-in": "s", "#local-out": "x"}
    sns.scatterplot(data = listita_1, x = "coord_x", y = "coord_y", s = 300,  hue = "shot", style = "shot")
    plt.legend(loc = 4,bbox_to_anchor=(0.95,0.05), fontsize=6, title='Shots attempted',title_fontsize=8, mode = "expand")
    plt.savefig("./images/map.png",dpi = 600)





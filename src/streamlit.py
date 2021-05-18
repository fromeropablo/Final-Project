import pandas as pd


def carga_data():
    data = pd.read_csv("data/average.cleaned.csv")
    return data


def lista_jugadores():
    data = carga_data()
    return list(data.PLAYER_NAME.unique())

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
    high = [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
    
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

    imagen = fig.set_facecolor('#121212')

    return imagen.save("./images/image.png")
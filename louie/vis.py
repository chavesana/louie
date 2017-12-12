import netorkx as nx
from matplotlib import pyplot as plt
import matplotlib


def plot_graph(graph, ax=None, cmap='coolwarm', node_size=300, node_color='.6',labels=False, font_size=24, font_color='k', **kwargs):
    """
    Plots a graph. Borrowed from Autocnet (https://github.com/USGS-Astrogeology/autocnet)


    Parameters
    ----------
    graph : object
            A networkX or derived graph object

    ax : objext
         A MatPlotLib axes object

    cmap : str
           A MatPlotLib color map string. Default 'Spectral'

    node_size : int
                the size of a node

    node_color : str
                 Matplotlib color for nodes

    labels : boolean
             If true, node names are written over the nodes

    font_size : int
                The font size for labels

    font_color : str


    Returns
    -------
    ax : object
         A MatPlotLib axes object. Either the argument passed in
         or a new object
    """
    if ax is None:
        ax = plt.gca()

    cmap = matplotlib.cm.get_cmap(cmap)

    # Setup edge color based on the health metric
    colors = []
    for s, d, e in graph.edges(data=True):
        if hasattr(e, 'health'):
            colors.append(cmap(e.health)[0])
        else:
            colors.append(cmap(0)[0])

    pos = nx.fruchterman_reingold_layout(graph)
    nx.draw_networkx_nodes(graph, pos, node_size=node_size, node_color=node_color, ax=ax)
    nx.draw_networkx_edges(graph, pos, style='dashed', edge_color=".4",  ax=ax)
    if labels:
        labels = dict((d,d) for d in graph.nodes())
        nx.draw_networkx_labels(graph, pos, labels, font_color=font_color, font_size=font_size,font_weight='bold', ax=ax)
    ax.axis('off')
    return ax

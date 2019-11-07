import BasicAlgorithms as BA
from scipy.cluster.hierarchy import linkage, dendrogram
import matplotlib.pyplot as plt


def augmented_dendrogram(*args, **kwargs):
    ddata = dendrogram(*args, **kwargs)

    if not kwargs.get('no_plot', False):
        for i, d in zip(ddata['icoord'], ddata['dcoord']):
            x = 0.5 * sum(i[1:3])
            y = d[1]

            plt.plot(x, y, 'ro')

            plt.annotate("%.3g" % y, (x, y), xytext=(0, -8),
                         textcoords='offset points',
                         va='top', ha='center')

    return ddata

def agnes_graph_viewer(data, dict_distances):
    agnes_matrix = BA.create_matrix(dict_distances, len(data))

    Z = linkage(agnes_matrix, 'ward')

    plt.figure(1, figsize=(8, 7))
    plt.clf()
    plt.scatter(data, data)
    plt.axis('equal')
    plt.grid(True)
    linkage_matrix = linkage(agnes_matrix, "single")
    plt.clf()
    plt.subplot(1, 2, 1)
    show_leaf_counts = False
    dendrogram(Z, leaf_rotation=90, leaf_font_size=8, labels=data)
#    plt.savefig(r'C:\Users\Ilyes\Desktop\dendrogram_01b.png')
    plt.title("Agnes Graph Viewer")
    plt.show()

    return plt

def kmedoid_graph_viewer():
    return

def dbscan_graph_viewer():
    return


if __name__ == '__main__':
    data = BA.import_seq(r"C:\Users\Ilyes\Desktop\dna_examples.txt")

    taille_data = len(data)
    # Calculate distances between clusters
    dict_distances = dict()
    for i in range(taille_data):
        for j in range(i + 1, taille_data):
            dict_distances[(i, j)] = BA.distance(data[i], data[j])# to save distances

    agnes_graph_viewer(data, dict_distances)

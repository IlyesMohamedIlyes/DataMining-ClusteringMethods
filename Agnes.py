import re
from BasicAlgorithms import *
import GraphViewer as GV

def agnes(data):
    taille_data = len(data)
    dict_clusters = {}
    dict_distances = {}
    # Initialize a cluster for each sequence
    for i in range(taille_data):
        dict_clusters[i] = list() #The key represents the index of the sequence

    # Calculate distances between clusters
    for i in range(taille_data):
        for j in range(i + 1, taille_data):
            dict_distances[(i, j)] = distance(data[i], data[j])# to save distances

    copy_dict_distances = dict_distances.copy()

    taille_dict = taille_data
    message = '***********  ******  AGNES  ******  ***********\n\n'
    message += str.format('Les {0} clusters de départ sont :\n{1}\n\n', taille_dict, dict_clusters)
    print(message)
    cpt = 0
    while taille_dict > 1:
        cpt += 1 # For iteration messages
        # Just getting the first occurance
        for d in dict_distances.items():
            distance_min = d
            break

        # Searching for the minimum distance
        for item_distance in dict_distances.items():
            if distance_min[1] > item_distance[1]:
                distance_min = item_distance

        # Jumeler the two clusters
        ## Get index of the cluster host
        index_host = distance_min[0][0]
        ## Get index of the cluster invite
        index_invite = distance_min[0][1]
        ## Appending the cluster itself
        dict_clusters[index_host].append(index_invite)
        ## Appending content of the cluster
        for c in dict_clusters[index_invite]:
            dict_clusters[index_host].append(c)

        # Take off the cluster invited
        del dict_clusters[index_invite]

        # Take off all items with the index invite
        for index in dict_clusters.keys():
            #
            if index > index_invite:
                del dict_distances[(index_invite, index)]
            else:
                del dict_distances[(index, index_invite)]

        # Change dict_clusters length
        taille_dict -= 1

        # Afficher message
        message_part = str.format('Apres {0} regroupment, les {1} clusters sont :\n{2}\n', cpt, taille_dict, dict_clusters)
        message += message_part
        #print(message_part)

    return message, copy_dict_distances, calculate_intraclass(dict_clusters, copy_dict_distances), calculate_interclass(data, copy_dict_distances), calculate_silhouette(dict_clusters, dict_distances)


if __name__ == '__main__':

    data = import_seq(r"C:\Users\Ilyes\Desktop\dna_examples.txt")

    agnes(data)




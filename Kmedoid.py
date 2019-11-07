import random as rd
import BasicAlgorithms as BA

def choose_random(k_clusters, data_indexes):

    clusters = dict()
    i = 0
    while i < k_clusters:
        random_index = rd.randint(0, len(data_indexes)-1)
        if random_index in clusters:
            continue

        clusters[random_index] = []
        data_indexes.remove(random_index) # To avoid testing on a medoids
        i+=1

    return clusters, data_indexes

def calculate_clusters_kmedoid(data_indexes, clusters, dict_distances):
    # For each sequence, calculate the distance between it and medoids and add it to the closet medoid
    for index_d in data_indexes:
        closet_dist_c = -1  # Contiendra la distance du cluster le plus proche
        index_closet_dist_c = -1  # Contiendra l'index du cluster le plus proche

        for index_c in clusters:
            if index_c > index_d:  # This if is a control for the distance matrix
                dist_c = dict_distances[(index_d, index_c)]
            else:
                dist_c = dict_distances[(index_c, index_d)]

            if closet_dist_c == -1:
                closet_dist_c = dist_c
                index_closet_dist_c = index_c
                continue

            if closet_dist_c > dist_c:
                closet_dist_c = dist_c
                index_closet_dist_c = index_c

        # Adding to the closet medoid
        if closet_dist_c == -1:
            continue

        clusters[index_closet_dist_c].append(index_d)

    return clusters

def calculate_clusters_kmeans(data, data_indexes, clusters):
    # For each sequence, calculate the distance between it and medoids and add it to the closet medoid
    for index_d in data_indexes:
        closet_dist_c = -1  # Contiendra la distance du cluster le plus proche
        index_closet_dist_c = -1  # Contiendra l'index du cluster le plus proche

        for seq_c in clusters:
            dist_c = BA.distance(seq_c, data[index_d])
            if closet_dist_c == -1:
                closet_dist_c = dist_c
                seq_closet_dist_c = seq_c
                continue

            if closet_dist_c > dist_c:
                closet_dist_c = dist_c
                seq_closet_dist_c = seq_c

        # Adding to the closet medoid
        if closet_dist_c == -1:
            continue

        clusters[seq_closet_dist_c].append(index_d)

    return clusters

def reevaluate_intra_clusters_kmedoid(data, clusters, new_data_indexes):
    changed = False
    for index_c in clusters:
        if len(clusters[index_c]) == 0:
            continue
        seq_approched = calculate_approched_sequence(data, clusters[index_c])

        print(data[index_c], '      ///---////      ', seq_approched)
        min_dist = BA.distance(data[index_c], seq_approched)
        min_index = index_c
        # Search for the most close
        for index_d in clusters[index_c]:
            dist = BA.distance(data[index_d], seq_approched)
            if min_dist == -1:
                min_dist = dist
                min_index = index_d
                continue

            if min_dist > dist:
                min_dist = dist
                min_index = index_d
        if min_index == index_c:
            continue

        changed = True
        del clusters[index_c]
        clusters[min_index] = []
        new_data_indexes.append(index_c)
        new_data_indexes.remove(min_index)

    return changed, clusters, new_data_indexes

def reevaluate_intra_clusters_kmeans(data, clusters):
    new_clusters = dict()
    changed = False
    for seq_c in clusters:
        seq_approched = calculate_approched_sequence(data, clusters[seq_c])

        if not changed:
            changed = seq_approched != seq_c
        if seq_approched != seq_c:
            new_clusters[seq_approched] = []
        else:
            new_clusters[seq_c] = clusters[seq_c]

    return new_clusters, changed

def calculate_approched_sequence(data, data_indexes):

    sequence_approchee = ''
    c = ''
    for i in range(len(data[0])): # Sachant que toutes les sequences ont la meme taille
        dict_repetitions = dict()
        for index_d in data_indexes:
            c = data[index_d][i]
            if c not in dict_repetitions:
                dict_repetitions[c] = 1
                continue
            dict_repetitions[c] += 1
        if c == '':
            continue
        max_v = dict_repetitions[c]
        char_max = c
        for (key, value) in dict_repetitions.items():
            if max_v < value:
                char_max = key
                max_v = value

        sequence_approchee += char_max

    return sequence_approchee

def kmeans(data, k_clusters):

    taille_data = len(data)
    data_indexes = []

    # Calculate all distances between each object
    dict_distances = dict()
    for i in range(taille_data):
        data_indexes.append(i)
        for j in range(i + 1, taille_data):
            dict_distances[(i, j)] = BA.distance(data[i], data[j])

    clusters, new_data_indexes = choose_random(k_clusters, data_indexes)



    new_clusters = dict()
    for index_c in clusters:
        new_clusters[data[index_c]] = []

    message = str.format('Clusters are : {0}\n',new_clusters.keys())

    changed = True
    return continue_kmeans(changed, data, new_clusters, new_data_indexes, dict_distances, message)

def continue_kmeans(changed, data, new_clusters, new_data_indexes, dict_distances, message):
    if changed:
        # function
        new_clusters = calculate_clusters_kmeans(data, new_data_indexes, new_clusters)
        message += str.format('Clusters are : {0}\n',new_clusters)
        # Recalculate distances for each cluster and assign new medoid if exists
        new_clusters, changed = reevaluate_intra_clusters_kmeans(data, new_clusters)
        message += str.format('Clusters are : {0}\n', new_clusters)

    return changed, message, BA.calculate_intraclass(new_clusters, dict_distances), BA.calculate_interclass(data, dict_distances), BA.calculate_silhouette(new_clusters, dict_distances)

def kmedoid(data, k_clusters):

    taille_data = len(data)
    data_indexes = []

    # Calculate all distances between each object
    dict_distances = dict()
    for i in range(taille_data):
        data_indexes.append(i)
        for j in range(i + 1, taille_data):
            dict_distances[(i, j)] = BA.distance(data[i], data[j])

    # Choose random medoids
    clusters, new_data_indexes = choose_random(k_clusters, data_indexes)

    print(str.format('Clusters are : {0}\n',clusters.keys()))
    message = ''
    changed = True
    while changed:
        #function
        clusters = calculate_clusters_kmedoid(new_data_indexes, clusters, dict_distances)
        print(str.format('Clusters are : {0}\n', clusters))
        message += str.format('Clusters are : {0}\n', clusters)
        # Recalculate distances for each cluster and assign new medoid if exists
        changed, clusters, new_data_indexes = reevaluate_intra_clusters_kmedoid(data, clusters, new_data_indexes)
        print(str.format('Clusters are : {0}\n', clusters))
        message += str.format('Clusters are : {0}\n', clusters)

    return message, BA.calculate_intraclass(clusters, dict_distances), BA.calculate_interclass(data, dict_distances), BA.calculate_silhouette(clusters, dict_distances), clusters

if __name__ == '__main__':

    data = BA.import_seq(r"C:\Users\Ilyes\Desktop\dna_examples.txt")

    kmedoid(data, 3)
    kmeans(data, 3)
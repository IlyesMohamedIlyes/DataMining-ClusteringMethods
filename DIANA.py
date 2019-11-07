from Leveinshtein import *
import re


def diana(data):
    dict_clusters = {}
    dict_distances = {}
    # create one large cluster with a -1 which is a test cluster
    dict_clusters[-1] = list()
    for i in range(len(data)):
        dict_clusters[-1].append(i)

    # search for the sequence with the highest average dissimilarity
    distance_max = -1
    index_max = -1
    for i in range(len(data)):
        distance_current = 0
        for j in range(i+1, len(data)):
            dict_distances[set(i, j)] = distance(data[i], data[j]) #to save distances
            distance_current += dict_distances[set(i, j)]

        if distance_current > distance_max:
            distance_max = distance_current
            index_max = i

    # create new cluster
    dict_clusters[index_max] = list()

    for index in range(len(data)):
        if index not in dict_clusters[index_max]:
            for index_in_cluster in dict_clusters[index_max]:
                break # DONT DO DIANA


def distance(seq1, seq2):
    dist = 0
    for i in range(len(seq1)):
        if seq1[i] == '-' and seq2[i] == '-':
            dist += 0.75
        elif seq1[i] == '-' or seq2[i] == '-':
                dist += 0.5
        elif seq1[i] != seq2[i] :
            dist += 1

    return dist


def valid_sequence(ch):
    seq = ch.upper()
    if len(seq) == 0:
        return False

    return (len(seq) == seq.count("-") + seq.count("A") + seq.count("T") + seq.count("C") + seq.count("G"))


if __name__ == '__main__':

    data_not_valid = open(r"C:\Users\Ilyes\Desktop\dna_examples.txt", 'r').read()
    data_not_valid = re.split(r'\W+', data_not_valid)
    data = []
    cpt = 50
    for d in data_not_valid:
        if cpt == 0:
            break
        if valid_sequence(d):
            data.append(d)
        cpt -= 1

    diana(data)

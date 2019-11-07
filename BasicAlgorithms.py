import re
import random
import numpy as np


def import_seq(path, cpt=-1):
    data_not_valid = open(path, 'r').read()
    data_not_valid = re.split(r'\W+', data_not_valid)
    data = []
    for d in data_not_valid:
        if cpt == 0:
            break

        if valid_sequence(d):
            data.append(d)

        if cpt == -1:
            pass
        else:
            cpt -= 1

    return data


dict_nucleo = dict()
dict_nucleo['A'] = 'T'
dict_nucleo['C'] = 'G'
dict_nucleo['T'] = 'A'
dict_nucleo['G'] = 'C'


def distance(seq1: str, seq2: str):
    dist = 0
    seq1 = seq1.upper()
    seq2 = seq2.upper()
    for i in range(len(seq1)):
        if seq1[i] == '-' and seq2[i] == '-':
            dist += 0.75
        elif seq1[i] == '-' or seq2[i] == '-':
            dist += 0.5
        elif seq1[i] == seq2[i]:
            dist += 1
        elif dict_nucleo[seq1[i]] == seq2[i]:
            dist += 0.25

    return dist


def valid_sequence(ch):
    seq = ch.upper()
    if len(seq) == 0:
        return False

    return (len(seq) == seq.count("-") + seq.count("A") + seq.count("T") + seq.count("C") + seq.count("G"))


def create_matrix(dict_distance: dict, n):
    l = [[0] * n] * n
    print(n)
    ar = np.array(l, dtype=np.float64)
    for i in range(n - 1):
        for j in range(n - 1):
            if i == j:
                continue
            if i > j:
                ar[i][j] = dict_distance[(j, i)]
                continue

            ar[i][j] = dict_distance[(i, j)]

    return ar


def generate_random_seq(taille):
    sequence = ''
    l = ['A', 'C', 'T', 'G']
    for i in range(taille):
        sequence += l[random.randint(0, 3)]

    return sequence


def calculate_silhouette(element, indexclusterelm, clusters:dict, dict_distances:dict):
    # Calculate a(i) which is the mean distance between the element and elements of the same cluster
    # Calculate b(i) which is the mean distance between the element and elements of other clusters (cluster of element not included)
    # Calcute the silhouette formula

    # a(i)
    a = 0
    leng = len(clusters[indexclusterelm])
    elements = clusters[indexclusterelm]
    for i in range(leng):
        a += dict_distances[(element, element[i])]

    a = a / leng

    # b(i)
    leng = len(clusters)
    b_parts = [0] * leng
    i = 0
    for index_c in clusters:
        # distances with other clusters, self cluster not included
        if index_c == indexclusterelm:
            continue

        cpt = 0
        for elem in clusters[index_c]:
            b_parts[i] += dict_distances[(element, elem)]
            cpt += 1

        b_parts[i] = b_parts[i] / len(cpt)
        i += 1

    b = 0
    for v in b_parts:
        b += v

    b = b / leng

    silhouette = (b - a) / max(a, b)
    return silhouette


def calculate_intraclass(clusters, dict_distances: dict):
    intraclass = 0

    return intraclass

    for index_c in clusters:
        somme = 0
        taille = len(clusters[index_c])
        for i in range(taille):
            for j in range(taille):
                if i == j:
                    continue
                if i > j:
                    intraclass += dict_distances[(j, i)]
                    continue
                intraclass += dict_distances[(i, j)]

        intraclass += somme / taille

    return intraclass


def calculate_interclass(clusters, cg):
    somme = 0
    return somme

    for i in range(len(clusters)):
        for j in range(len(clusters[i])):
            somme += distance(clusters[i][j], cg[i])
    return somme


def silhouette_a(clus, dict_distances):
    n = len(clus)
    l = []
    for i in range(len(clus)):
        a = 0
        for j in range(i + 1, len(clus)):
            try:
                a += dict_distances[(clus[i], clus[j])]
            except KeyError:
                continue
        a /= (n - 1)
        l.append(a)
    return l


def silhouette_b(clusters, clus, dict_distances):
    alll = []

    for i in range(len(clus)):
        l = []
        for j in range(len(clusters)):
            if (clus != clusters):
                n = len(clusters[j])
                s = 0
                for k in range(len(clusters[j])):
                    try:
                        s += dict_distances[(clus[i], clusters[j][k])]
                    except KeyError:
                        continue
                l.append(s)
        alll.append(min(l))
    return alll


def calculate_silhouette(clusters, dict_distances):

    silhouette = []
    return silhouette
    for index_c in clusters:
        s = []
        clus = clusters[index_c]

        a = silhouette_a(clus, dict_distances)
        b = silhouette_b(clusters, clus, dict_distances)

        for j in range(len(clus)):
            try:
                val = (b[j] - a[j]) / (max(a[j], b[j]))
            except ZeroDivisionError:
                print('ATTENTION! ZeroDivisionError detected.')
                continue
            s.append(val)
        silhouette.append(s)

    print(silhouette)
    return silhouette


def adding_sequence(x, y):
    sequence = convert_coords_to_seq(x, y)
    sequence = '>' + sequence + '\n'
    return sequence

def convert_seq_to_coords(seq):
    # x normalization is 85.46666666666667
    # y normalization is 56.5

    l = int(len(seq)/2)

    x = 0.0
    y = 0.0
    for i in range(l):
        x += ord(seq[i]) + i

    for i in range(l+1, l*2):
        y += ord(seq[i]) + i

    x /= l
    y /= (l*2)

    # Normalize
    x /= 85.46666666666667
    y /= 56.5
    return x, y


def convert_coords_to_seq(x, y):
    seq = generate_random_seq(60)
    return seq


if __name__ == '__main__':
    pass
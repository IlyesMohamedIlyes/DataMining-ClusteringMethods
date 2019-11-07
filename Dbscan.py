
import BasicAlgorithms as BA
############################################ DBSCAN
from copy import deepcopy
import math


def dist(x, y):
    ######la methode est defini selon le type de la variable

    # Example points in 3-dimensional space...
    if type(x) == type(" "):

        k = 0

        for i in range(0, min(len(x), len(y))):
            # print (i)
            if x[i] == y[i]:
                k = k + 1
        # t=creation(x,y,0,1,1)
        # return t[len(t)-1][len(t[len(t)-1])-1]
        return len(x) - k
    else:
        return math.sqrt((x[0] - y[0]) ** 2 + (x[1] - y[1]) ** 2)
def init_tab_voisin(ensemble):
    v = []
    for i in range(0, len(ensemble)):
        v.append([])
    return v
def tab_distance(ensemble, distance):
    dic = dict()
    for i in range(0, len(ensemble)):
        dic[str(i)] = dict()

    for i in range(0, len(ensemble)):

        tabvoisin = []
        nbr = 0
        for j in range(0, len(ensemble)):
            if not i == j:
                d = dist(ensemble[i], ensemble[j])
                dic[str(i)][str(j)] = d
                dic[str(j)][str(i)] = d
                if d <= distance:
                    tabvoisin.append(j)
                    nbr = nbr + 1

            j = j + 1
        dic[str(i)]["t"] = tabvoisin
        dic[str(i)]["n"] = nbr
    return dic
def cluster(indensemble, t, v, cluster, all_cluster, minpnt, distance):
    c = deepcopy(cluster)
    while (len(v) > 0):
        temp = v[0]
        if t[str(v[0])]["n"] >= minpnt:
            tableau = deepcopy(t[str(v[0])]["t"])
            v.extend(list(tableau))
            v = list(set(v))

        """for i in range(0,len(v)):
            if not temp==v[i] and  t[str(v[i])][str(temp)]<=distance :
                #print(v[i],temp,t[str(v[i])])
                t[str(v[i])]["t"].remove(temp)
        """
        pas_suprimer = 0
        for cle, value in t.items():
            if not int(cle) == temp and value[str(temp)] <= distance:
                if value["n"] >= minpnt and temp == 3:
                    print("cle :" + cle + " temp:" + str(temp))

                value["t"].remove(temp)
        j = 0
        cond2 = 0
        while (j < len(indensemble) and cond2 == 0):
            if temp == indensemble[j][0]:

                cond2 = 1
            else:
                j = j + 1

        indensemble.remove(indensemble[j])

        c.append(temp)
        v.remove(temp)
    return c
def dbscan_h(d, pnt, ens):
    # print("ensemble : ",ens)
    ensemble = ens
    parcour = []
    voisin = []
    indensemble = []
    distance = d
    minpnt = pnt
    for i in range(0, len(ensemble)):
        indensemble.append([i, ensemble[i]])
    print("ind ensemble ", indensemble)
    t = tab_distance(ensemble, distance)
    print("tab dist", t)
    # nbr = 0
    """
    for kle,value in t.items():
        if value["n"]>=minpnt:
            nbr=nbr+1
            print(kle,value["t"])
    """

    all_cluster = []
    it = 0
    while (len(indensemble) > 0):

        tab = deepcopy(t[str(indensemble[0][0])]["t"])
        it = it + 1
        if t[str(indensemble[0][0])]["n"] >= minpnt:
            print("cc1")

            for i in range(0, len(tab)):
                if not indensemble[0][0] == tab[i] and t[str(tab[i])][str(indensemble[0][0])] <= distance:
                    # print(indensemble[0][0],t[str(tab[i])])
                    t[str(tab[i])]["t"].remove(indensemble[0][0])
            temp = indensemble[0][0]
            print("avant 1", indensemble)
            indensemble.remove(indensemble[0])
            print("apres1 ", indensemble)
            c = cluster(indensemble, t, tab, [temp], all_cluster, minpnt, distance)
            print("cluster 1 ", c)
            all_cluster.append(c)

        else:

            cond = 0
            k = 0
            print("cc2")

            while (k < len(tab) and cond == 0):
                if t[str(tab[k])]["n"] >= minpnt:
                    cond = 1
                    p = tab[k]
                    tab = deepcopy(t[str(tab[k])]["t"])

                else:
                    k = k + 1

            if cond == 0:
                """for c,value in t.items():
                    if not int(c)==indensemble[0][0] and value[str(indensemble[0][0])]<=distance:

                        value["t"].remove(indensemble[0][0])
                """
                indensemble.remove(indensemble[0])
            else:
                j = 0
                cond2 = 0
                while (j < len(indensemble) and cond2 == 0):
                    if p == indensemble[j][0]:
                        cond2 = 1
                    else:
                        j = j + 1

                for i in range(0, len(tab)):
                    if not p == tab[i] and t[str(tab[i])][str(p)] <= distance:
                        t[str(tab[i])]["t"].remove(indensemble[j][0])
                temp = indensemble[j][0]
                indensemble.remove(indensemble[j])
                c = cluster(indensemble, t, tab, [temp], all_cluster, minpnt, distance)
                print("c 2 ", c)
                all_cluster.append(c)
        # nbr = 0
        # print ("it ",it)
        print("it ", it)
        print("indens ", len(indensemble))
    return all_cluster

def create_new_cluster(current_visited_obj, taille_data, dict_distances, vector_unvisited_object, rad, minPnt, dict_data, clusters):
    new_cluster = []
    for index_unvisited in range(taille_data):
        #
        # We don't need to valuate objects already in a cluster
        if dict_data[index_unvisited] == True:
            continue

        if current_visited_obj > index_unvisited:
            distance = dict_distances[(index_unvisited, current_visited_obj)]
        elif current_visited_obj < index_unvisited:
            distance = dict_distances[(current_visited_obj, index_unvisited)]
        else:
            continue

        # Add to new_cluster objects
        if distance < rad:
            new_cluster.append(index_unvisited)

    if len(new_cluster) < minPnt:
        # Create the cluster
        new_cluster.append(current_visited_obj)
        # Mark Visited all the objects
        for c in new_cluster:
            dict_data[c] = True
            # Take off the element of unvisited objects
            try:
                vector_unvisited_object.remove(c)
            except ValueError:
                continue

            create_new_cluster(c, taille_data, dict_distances, vector_unvisited_object, rad, minPnt, dict_data, clusters)

    clusters.append(new_cluster)


def dbscan(data, rad, minPnt):

    taille_data = len(data)
    dict_data = {}
    vector_unvisited_object = [] # This vector will contain the unvisited objects.
                                    # Will help us to choose the first random unvisited object

    # Mark all objects as unvisited
    for i in range(taille_data):
        vector_unvisited_object.append(i)
        dict_data[i] = False

    # Calculate all distances between each object
    dict_distances = dict()
    for i in range(taille_data):
        for j in range(i + 1, taille_data):
            dict_distances[(i, j)] = BA.distance(data[i], data[j])

    clusters = []
    message = '***********  ******  DBSCAN  ******  ***********\n\n'
    print(message)
    cpt = 0

    while False in dict_data.values():
        cpt += 1  # For iteration messages
        # Random unvisited object
        current_visited_obj = vector_unvisited_object[0]

        # Mark the choosed object as visited
        dict_data[current_visited_obj] = True
        ## Take it off the vector_unvisited_object
        vector_unvisited_object.remove(current_visited_obj)

        # Get distances and return the new cluster which is not verified
        create_new_cluster(current_visited_obj, taille_data, dict_distances, vector_unvisited_object, rad, minPnt, dict_data, clusters)

        message_part = str.format('\nProcess n°= : {0} got result :\n{1}', cpt, clusters)
        print(message_part)
        message += message_part

    return message, BA.calculate_intraclass(clusters, dict_distances), BA.calculate_interclass(data, dict_distances), BA.calculate_silhouette(clusters, dict_distances)


if __name__ == '__main__':

    data = BA.import_seq(r"C:\Users\Ilyes\Desktop\dna_examples.txt")

    message = dbscan(data, 38, 2)

    #print(dbscan_h(38, 2, data))

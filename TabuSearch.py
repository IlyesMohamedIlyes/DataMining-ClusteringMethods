
import copy
from Leveinshtein import *
import re

def distance(seq1, seq2):
    return Levenshtein(seq1, seq2)

def create_voisins(data):

    dict_voisins = dict()

    for i in range(len(data)):
        for j in range(i + 1, len(data)):
            if i not in dict_voisins:
                dict_voisins[i] = {}
                dict_voisins[i][j] = distance(data[i], data[j])
            else:
                dict_voisins[i][j] = distance(data[i], data[j])

            if j not in dict_voisins:
                dict_voisins[j] = {}
                dict_voisins[j][i] = distance(data[j], data[i])
            else:
                dict_voisins[j][i] = distance(data[j], data[i])

        return dict_voisins

def create_primary_solution(noeuds, dict_voisins):

    noeud_init = 0
    noeud_final = noeud_init

    primary_solution = []
    distance = 0
    deja_visite = noeud_init
    noeud_precedent = None

    while deja_visite not in primary_solution:
        temp = copy.deepcopy(dict_voisins[deja_visite])
        temp.pop(noeud_precedent, None)
        noeud_prochain = None
        for d in temp.values():
            if noeud_prochain == None:
                noeud_prochain = d

            if noeud_prochain > d:
                noeud_prochain = d

        distance += dict_voisins[deja_visite][noeud_prochain]
        primary_solution.append(deja_visite)
        noeud_precedent = deja_visite
        deja_visite = noeud_prochain

    primary_solution.append(noeuds[0])
    distance += dict_voisins[noeud_precedent][noeud_final]

    return primary_solution, distance

def find_voisins(solution, dict_voisins):
    solutions_voisines = []
    print(solution)
    for n in solution[1:-1]:
        index1 = []
        n_index = solution.index(n)
        index1.append(n_index)
        index1.append(n_index + 1)

    for m in solution[1:-1]:
        index2 = []
        m_index = solution.index(m)
        index2.append(m_index)
        index2.append(m_index + 1)

        bool_sol = set(solution[index1[0]:(index1[-1] +1)]) & set(solution[index2[0]:(index2[-1] +1)])

        if bool_sol:
            continue

        temp = copy.deepcopy(solution)

        for i in range(1):
            temp[index1[i]] = solution[index2[i]]
            temp[index2[i]] = solution[index1[i]]

        distance = 0
        for k in temp[:-1]:
            next_node = temp[temp.index(k) + 1]
            distance = distance + dict_voisins[k][next_node]

        temp.append(distance)
        if temp not in solutions_voisines:
            solutions_voisines.append(temp)

    solutions_voisines.sort(key=lambda x: x[len(solutions_voisines) - 1])

    return solutions_voisines


def tabu_search(first_solution, distance_of_first_solution, dict_of_neighbours, iters, size, n_opt=1):
    count = 1
    solution = first_solution
    tabu_list = list()
    best_cost = distance_of_first_solution
    best_solution_ever = solution

    while count <= iters:
        neighborhood = create_voisins(solution, dict_of_neighbours)
        index_of_best_solution = 0
        best_solution = neighborhood[index_of_best_solution]
        best_cost_index = len(best_solution) - 1
        found = False
        while found is False:
            i = 0
            first_exchange_node, second_exchange_node = [], []
            n_opt_counter = 0
            while i < len(best_solution):
                if best_solution[i] != solution[i]:
                    first_exchange_node.append(best_solution[i])
                    second_exchange_node.append(solution[i])
                    n_opt_counter += 1
                    if n_opt_counter == n_opt:
                        break
                i = i + 1

            exchange = first_exchange_node + second_exchange_node
            if first_exchange_node + second_exchange_node not in tabu_list and second_exchange_node + first_exchange_node not in tabu_list:
                tabu_list.append(exchange)
                found = True
                solution = best_solution[:-1]
                cost = neighborhood[index_of_best_solution][best_cost_index]
                if cost < best_cost:
                    best_cost = cost
                    best_solution_ever = solution
            elif index_of_best_solution < len(neighborhood):
                best_solution = neighborhood[index_of_best_solution]
                index_of_best_solution = index_of_best_solution + 1

        while len(tabu_list) > size:
            tabu_list.pop(0)

        count = count + 1
    best_solution_ever.pop(-1)

    return best_solution_ever, best_cost

def valid_sequence(ch):
    seq = ch.upper()
    if len(seq) == 0:
        return False

    return (len(seq) == seq.count("-") + seq.count("A") + seq.count("T") + seq.count("C") + seq.count("G"))


if __name__ == '__main__':

    max_iter = 100
    tabu_list_size = 15
    max_candidates = 50

    data_not_valid = open(r"C:\Users\Ilyes\Desktop\dna_examples.txt", 'r').read()

    data_not_valid = re.split(r'\W+', data_not_valid )
    data = []
    for d in data_not_valid:
        if valid_sequence(d):
            data.append(d)

    dict_of_neighbours = create_voisins(data)

    first_solution, distance_of_first_solution = create_primary_solution(data, dict_of_neighbours)

    best_sol, best_cost = tabu_search(first_solution, distance_of_first_solution, dict_of_neighbours, max_iter,
                                      tabu_list_size)

    print("Best solution: {0}, with total distance: {1}.".format(best_sol, best_cost))



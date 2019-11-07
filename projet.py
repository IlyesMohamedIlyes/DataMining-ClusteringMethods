import sys

def menu():
    print ("\n\n\n")
    print (30 * "-" + "  MENU " + 30 * "-")
    print ("1.  SEQUENCES ALEATOIRES")
    print ("2.  SEQUENCES A CHOISIR")
    print ("3.  IMPORTER UN FICHIER")
    print ("0. Exit")
    
def valid_sequence(ch):
    seq=ch.upper()
    return (len(seq) == seq.count("-")+seq.count("A")+ seq.count("T")+seq.count("C")+seq.count("G"))
########################################################################

def import_seq ():
    t=open('dna_examples.txt',"r")
    r=t.read()
    seq=r.split("\n")
    seq_import=[]
    
    for i in range (1,100, 2):
        seq_import.append(seq[i])
        
        
        
    d=34
    pnt=5
    #enss=import_seq ()
    print("la liste import : ",seq_import)
    listedbscan=dbscan(d,pnt,seq_import)
    
    print("dbscan clusters : ",listedbscan)
          
    return 
#########################################################################


def Levenshtein(chaine1,chaine2):
        
        cout=0
        
        longueur_chaine1, longueur_chaine2=len(chaine1), len(chaine2)
        distances=[[0 for x in range(longueur_chaine2+1)] for y in range(longueur_chaine1+1)]
        

        for i in range(1,longueur_chaine1+1):
                distances[0][i]= i
        for i in range(1,longueur_chaine2+1):
                distances[i][0]= i
                
        for i in range(1,longueur_chaine2+1):
                for j in range(1,longueur_chaine1+1):
                        if chaine1[i-1] != chaine2[j-1]:
                                cout=1
                        else:
                                cout=0

                        distances[i][j]=min(distances[i-1][j-1]+cout,distances[i][j-1]+1,distances[i-1][j]+1)
                        
        


       # print(distances)
        #print("le score LEVENSHTEIN est : ",distances[longueur_chaine1][longueur_chaine2])
        return distances[longueur_chaine1][longueur_chaine2]

def Levenshtein2(chaine1,chaine2):
        
        cout=0
        
        longueur_chaine1, longueur_chaine2=len(chaine1), len(chaine2)
        distances=[[0 for x in range(longueur_chaine2+1)] for y in range(longueur_chaine2+1)]
        
        for i in range(1,longueur_chaine2+1):
                distances[0][i]= i
        for i in range(1,longueur_chaine2+1):
                distances[i][0]= i
        #print (longueur_chaine1, longueur_chaine2)
        for i in range(1,longueur_chaine2+1):
                for j in range(1,longueur_chaine2+1):
                    
                    if chaine1[i-1] != chaine2[j-1]:
                            cout=1
                    else:
                            cout=0

                    distances[i][j]=min(distances[i-1][j-1]+cout,distances[i][j-1]+1,distances[i-1][j]+1)
                        
        
        return distances[longueur_chaine2][longueur_chaine2]




def kmeans_choix():
    nbre_cg=int(input("Entrez le nombre des centres de gravite(nomre de kluster) : "))
    nbre_pts=int(input("Entrez le nombre des instances : "))

    tab_cg =[[0 for x in range(60)] for y in range(nbre_cg)]
    tab_pts =[[0 for x in range(60)] for y in range(nbre_pts)]
    tab_distance =[[0 for x in range(nbre_cg)] for y in range(nbre_pts)]
    tab_distance2 =[[0 for x in range(nbre_cg)] for y in range(nbre_pts)]

    print("Les coordonnes des centres de gravites :")
    a=0
    while a < nbre_cg:
        ch=input("Entrez les coordonnees du centre de gravite : ")
        
        if (valid_sequence(ch)):
            seq=ch.upper()
            seq2=list(seq)
            i=0
            while i < len(ch):
                tab_cg[a][i]=seq2[i]
                i+=1
        else:
            print ("sequence non valide !")
            a-=1
        a+=1

    #print(tab_cg)

    print("Les coordonnes des instances :")
    a=0
    while a < nbre_pts:
        ch=input("Entrez les coordonnes de l'instance : ")
        
        if (valid_sequence(ch)):
            seq=ch.upper()
            seq2=list(seq)
            i=0
            while i < len(ch):
                tab_pts[a][i]=seq2[i]
                i+=1
        else:
            print ("sequence non valide !")
            a-=1
        a+=1

    #print(tab_pts)

    #calcule distance par similarite
    somme=0
    i1=0
    while i1<nbre_cg :
        i2=0
        while i2<nbre_pts:
            j=0
            instance=""
            cg=""

            while j<60:
                if tab_cg[i1][j] != 0:
                    cg=cg+str(tab_cg[i1][j])
                if tab_pts[i2][j] != 0:
                    instance=instance + str(tab_pts[i2][j])
                    
                if tab_cg[i1][j]==tab_pts[i2][j]:
                    if tab_cg[i1][j]!= 0 :
                        if tab_cg[i1][j]=="-":
                            somme=somme+0.25
                        else:
                            somme+=1
                    else:
                        somme=somme+0
                else:
                    if tab_cg[i1][j]==0 or tab_pts[i2][j]==0 :
                        somme=somme+0
                    else:
                        if tab_cg[i1][j]=="-" or tab_pts[i2][j]=="-" :
                            somme=somme+0.5
                        else:
                            somme=somme+0
                
                j+=1
            score=Levenshtein(cg,instance)
            tab_distance2[i2][i1]=score
            tab_distance[i2][i1]=somme
            i2+=1
            somme=0
            
        i1+=1
    print("\nLa table de distance de kmeans par similarite : \n", tab_distance)
    print(" \n \nLa table de distance de kmeans par Levenshtein : \n", tab_distance2)

    
    for i in range(0,nbre_pts):
        max=tab_distance[i][0]
        k=0
        for j in range(1,nbre_cg):
            if tab_distance[i][j] > max:
                max=tab_distance[i][j]
                k=j
        print ("instance numero", i+1," dans Cluster numero", k+1)

def seq_adn ():
    import random
    from random import randint
    char="ACTG"
    ch=""
    i=1
    n=14
    if n > 0 and n <= 1000 :
        while i <= n :
            ch += char[randint(0,len(char)-1)]
            i +=1
    #print(ch)
    return ch







def cgg(tab_pts,nbre_pts):
    cgglobale=""
    cpt=0
    for i in range(0,14):
        if tab_pts[0][i] != 0:
            cpt+=1
    
    for i in range(0,cpt):
        seq=""
        for j in range(0,nbre_pts):
            if tab_pts[j][i] != 0:
                seq=seq+str(tab_pts[j][i])
#print(seq)
        nbre_a=seq.count("A")
        nbre_c=seq.count("C")
        nbre_t=seq.count("T")
        nbre_g=seq.count("G")
        maxx=max(nbre_a,nbre_c,nbre_t,nbre_g)
        if nbre_a==maxx:
            cgglobale=cgglobale+"A"
        elif nbre_c==maxx:
            cgglobale=cgglobale+"C"
        elif nbre_t==maxx:
            cgglobale=cgglobale+"T"
        elif nbre_g==maxx:
            cgglobale=cgglobale+"G"
    print ("\nLe centre de gravite globale :  " + cgglobale + "\n")
    return cgglobale

######################################################################



######################################################################
def interclasse(cgg,tab_cg,nbre_cg):
    tab_distance3=[0 for x in range(60)]
    tab_distance4=[0 for x in range(60)]
    somme=0
    i2=0
    while i2<nbre_cg:
        j=0
        instance=""
        cg=""

        while j<len(cgg):
            if tab_cg[i2][j] != 0:
                
                cg=cg+str(tab_cg[i2][j])

            if tab_cg[i2][j]==cgg[j]:
                somme=somme+1

             
            j+=1
        score=Levenshtein2(cg,cgg)
        tab_distance3[i2]=score
        tab_distance4[i2]=somme
        i2+=1
        somme=0
    som1=0
    som2=0
    for i in range(0,14):
        som1=som1+tab_distance3[i]
        som2=som2+tab_distance4[i]


    print("\nInertie inter classe par similarite : " + str (som2))
    print("Inertie inter classe par Levenshtein : "+ str (som1))
    if (som2 > som1 ) :
        print ("Le clustring par similarite est mieux que celui par Levenshtein.\n")
    else:
        print ("Le clustring par Levenshtein est mieux que celui par similarite.\n")


def kmeans_aleatoire(nbre_cg, nbre_pts):
    dict_clusters_instances = dict()  # Or {}
    sequences = []
    intra1=0
    intra2=0
    
    tab_cg =[[0 for x in range(60)] for y in range(nbre_cg)]
    tab_pts =[[0 for x in range(60)] for y in range(nbre_pts)]
    tab_distance =[[0 for x in range(nbre_cg)] for y in range(nbre_pts)]
    tab_distance2 =[[0 for x in range(nbre_cg)] for y in range(nbre_pts)]
    tab_distance3=[[0 for x in range(nbre_pts)] for y in range(nbre_pts)]

    
    print("\n\nLes coordonnees des centres de gravites :\n")
    a=0
    while a < nbre_cg:
        ch=seq_adn()
        sequences.append(ch) # pour avoir la sequence à travers l'index
        seq2=list(ch)

        i=0
        while i < len(ch):
            tab_cg[a][i]=seq2[i]
            i+=1
        a += 1
    
    #print(tab_cg)

    print("\n \nLes coordonnees des instances :\n")
    ens=[]
    a=0
    while a < nbre_pts:
        ch = seq_adn()
        ens.append(ch)
        seq2=list(ch)
        
        i=0
        while i < len(ch):
            tab_pts[a][i]=seq2[i]
            i+=1
        a+=1

#print(tab_pts)


    #calcule distance par similarite
    somme=0
    i1=0
    while i1<nbre_cg :
        i2=0
        while i2<nbre_pts:
            j=0
            instance=""
            cg=""

            while j<60:
                if tab_cg[i1][j] != 0:
                    cg=cg+str(tab_cg[i1][j])
                if tab_pts[i2][j] != 0:
                    instance=instance + str(tab_pts[i2][j])
                    
                if tab_cg[i1][j]==tab_pts[i2][j]:
                    if tab_cg[i1][j]!= 0 :
                        somme=somme+1
                    else:
                        somme=somme+0
                
                j+=1




            score=Levenshtein(cg,instance)
            tab_distance2[i2][i1]=score
            intra1=intra1+score
            tab_distance[i2][i1]=somme
            intra2=intra2+somme
            i2+=1
            somme=0
            
        i1+=1
    print("\nLa table de distance de kmeans par similarite : \n"+ str(tab_distance))
    print(" \n \nLa table de distance par Levenshtein : \n"+ str(tab_distance2))
   
#######  affichage des inercies intraClasse (somme de distance entre cg et les seq )
    print("\nInertie intra classe par similarite : "+ str(intra1))
    print("Inertie intra classe par Levenshtein : "+ str(intra2))
    if (intra1 < intra2 ) :
        print ("Le clustring par similarite est mieux que celui par Levenshtein.\n")
    else:
        print ("Le clustring par Levenshtein est mieux que celui par similarite.\n")
    
    cgg1=cgg(tab_pts,nbre_pts)



    interclasse(cgg1,tab_cg,nbre_cg)

    #traitement clusters

    for i in range(0,nbre_pts):
        max=tab_distance[i][0]
        k=0
        for j in range(1,nbre_cg):
            if tab_distance[i][j] > max:
                max=tab_distance[i][j]
                k=j
            if k+1 not in dict_clusters_instances:  # k est le numero du cluster
                dict_clusters_instances[k+1] = []

            dict_clusters_instances[k+1].append(i+1)  # i est l'index de la seq // ou on peut ajouter la sequence
        print ("instance numero" , i+1 , " dans cluster numero", k+1)


    return dict_clusters_instances, sequences
'''
    tab_distance3=AGNES (nbre_pts,tab_pts)
    d=4
    pnt=5
    enss=import_seq ()
    print("la liste import : ",enss)
    listedbscan=dbscan(d,pnt,enss)
    print("dbscan clusters : ",listedbscan)
'''

        
print("\n \n \n ")
print ("                             Bonjour :) ")
loop=True      



################################################ AGNES
def AGNES (nbre_pts,tab_pts):
    print("\n \nALGORITHME AGNES : \n \n ")
    reference=dict() #dictionnaire de reference de clusters
    for i in range (0,nbre_pts):
        lis=[]
        lis.append(i+1)
        reference[i+1]=lis
    print("Les clusters de depart : ",reference.values())
    
    
    liste=[] #liste contenant les instances
    for i in range (0,nbre_pts):
        chh=""
        for j in range (0,11):
            if tab_pts[i][j] != 0:
                chh=chh+tab_pts[i][j]
        liste.append(chh)
    #print (liste)
    
    while len(reference) > 1: #boucler jusqu'a ce qu'on aura 1 cluster
        tab_d=[[0 for x in range(len(reference))] for y in range(len(reference))]     

        #remplir la table avec les distance
        a=-1        
        for i in reference:
            a+=1
            b=0
            for j in reference:
                if a==b :
                    tab_d[a][b]=0
                else:
                    s=0
                    d=0
                    for k in range(0,len(reference[i])):
                        for m in range(0,len(reference[j])):
                            s=s+Levenshtein2(liste[reference[i][k]-1],liste[reference[j][m]-1])
                            d+=1
                    tab_d[a][b]=s/d
                b+=1

        #recherche minimum dans la table                
        min=tab_d[0][1]
        instance1=1
        instance2=2
        for i in range (0,len(reference)):
            for j in range (i+1,len(reference)):
                if min >tab_d[i][j]:
                    min=tab_d[i][j]
                    instance1=i+1
                    instance2=j+1
        a=1
        b=1
        for ref in reference: #recuperer la reference du cluster qu'on va regrouper
            #print ref
            if a==instance1:
                instance1=ref
            if b==instance2:
                instance2=ref
            a+=1
            b+=1
            
        #reference[instance1].append(instance2)
        for lo in reference[instance2]:
            reference[instance1].append(lo)
        del reference[instance2]
        print ("les clusters sont : ",reference.values())

    return


############################################ DBSCAN
from copy import deepcopy
import math
def dist(x,y):
    ######la methode est defini selon le type de la variable

    # Example points in 3-dimensional space...
    if type(x)==type(" "):

        k=0
        
        for i in range(0,min(len(x),len(y))):
            #print (i)
            if x[i]==y[i]:
                k=k+1
        #t=creation(x,y,0,1,1)
        #return t[len(t)-1][len(t[len(t)-1])-1]
        return len(x)-k
    else:
        return math.sqrt((x[0]-y[0])**2+(x[1]-y[1])**2)
def init_tab_voisin(ensemble):
    v=[]
    for i in range(0,len(ensemble)):
       v.append([])
    return v
def tab_distance(ensemble,distance):
    dic=dict()
    for i in range(0,len(ensemble)):
        dic[str(i)]=dict()

    for i in range(0,len(ensemble)):

        tabvoisin=[]
        nbr=0
        for j in range(0,len(ensemble)):
            if not i==j:
                d=dist(ensemble[i],ensemble[j])
                dic[str(i)][str(j)]=d
                dic[str(j)][str(i)] = d
                if d<=distance:

                    tabvoisin.append(j)
                    nbr=nbr+1

            j=j+1
        dic[str(i)]["t"] =tabvoisin
        dic[str(i)]["n"] =nbr
    return dic
def cluster(indensemble,t,v,cluster,all_cluster,minpnt,distance):
    c=deepcopy(cluster)
    while(len(v)>0):
        temp=v[0]
        if t[str(v[0])]["n"]>=minpnt:
            tableau=deepcopy(t[str(v[0])]["t"])
            v.extend(list(tableau))
            v = list(set(v))

        """for i in range(0,len(v)):
            if not temp==v[i] and  t[str(v[i])][str(temp)]<=distance :
                #print(v[i],temp,t[str(v[i])])
                t[str(v[i])]["t"].remove(temp)
        """
        pas_suprimer=0
        for cle, value in t.items():
            if not int(cle)==temp and value[str(temp)]<=distance:
                if value["n"]>=minpnt and temp==3:
                    print("cle :" + cle + " temp:" + str(temp))

                value["t"].remove(temp)
        j = 0
        cond2 = 0
        while (j < len(indensemble) and cond2==0):
            if temp == indensemble[j][0]:

                cond2 = 1
            else:
                j = j + 1

        indensemble.remove(indensemble[j])

        c.append(temp)
        v.remove(temp)
    return c




def dbscan(d,pnt,ens):
    #print("ensemble : ",ens)
    ensemble =ens
    parcour = []
    voisin = []
    indensemble = []
    distance=d
    minpnt=pnt
    for i in range(0, len(ensemble)):
        indensemble.append([i, ensemble[i]])
    print("ind ensemble ",indensemble)
    t = tab_distance(ensemble, distance)
    print("tab dist",t)
    #nbr = 0
    """
    for kle,value in t.items():
        if value["n"]>=minpnt:
            nbr=nbr+1
            print(kle,value["t"])
    """

    all_cluster = []
    it=0
    while (len(indensemble) > 0):

        tab = deepcopy(t[str(indensemble[0][0])]["t"])
        it=it+1
        if t[str(indensemble[0][0])]["n"] >= minpnt:
            print("cc1")

            for i in range(0, len(tab)):
                if not indensemble[0][0] == tab[i] and t[str(tab[i])][str(indensemble[0][0])] <= distance:
                    # print(indensemble[0][0],t[str(tab[i])])
                    t[str(tab[i])]["t"].remove(indensemble[0][0])
            temp = indensemble[0][0]
            print("avant 1",indensemble)
            indensemble.remove(indensemble[0])
            print("apres1 ",indensemble)
            c = cluster(indensemble, t, tab, [temp], all_cluster, minpnt, distance)
            print("cluster 1 ",c)
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
                print("c 2 ",c)
                all_cluster.append(c)
    #nbr = 0
        #print ("it ",it)
        print ("it ",it)
        print ("indens ",len(indensemble))
    return all_cluster

def afficher_kmeans_aleatoire(dict_cl_inst, sequences):

    for item_index in range(len(dict_cl_inst)):
        print('Le cluser n°=', item_index+1, 'contient :\n')
        values = dict_cl_inst[item_index+1]
        print(values)
        print(len(sequences))
        for index in values:
            print(sequences[index-1])

##########################################################################

###  Execution
while loop:
    menu()    
    choice = int(input("Entrez votre choix [1-3]: "))

     
    if choice== 1:
        nbre_cg = int(input("Entrez le nombre de cluster : "))
        nbre_pts = int(input("Entrez le nombre des instances : "))
        dict_clusters_instances, seqs = kmeans_aleatoire(nbre_cg, nbre_pts)

        afficher_kmeans_aleatoire(dict_clusters_instances, seqs)

    elif choice==2:
        kmeans_choix()
    elif choice==0:
        loop=False
    elif choice==3:
        import_seq()
         

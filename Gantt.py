import csv
import networkx as nx
import matplotlib.pyplot as plt
import numpy as np


def opencsv(fichier):
    matrice = []
    with open(fichier, 'r') as file:
        csvreader = csv.reader(file, delimiter=";")
        for ligne in csvreader:
            matrice.append(ligne)
    return matrice


def graphegenerate(matrice):
    graphe = nx.DiGraph()
    for ligne in matrice:
        graphe.add_node(ligne[0], weight=ligne[1])
        tabsplit = ligne[2].split(',')
        for i in range(len(tabsplit)):
            if bool(tabsplit[i]):
                graphe.add_edge(tabsplit[i], ligne[0])
    return graphe


def graphelvl(graphe):
    nodelayer = []
    while len(list(nodelayer)) < len(graphe.nodes):
        for node in graphe.nodes:
            if not list(graphe.predecessors(node)):
                graphe.nodes[node]["layer"] = 0
                nodelayer.append(node)
            else:
                max = 0
                for predecessor in graphe.predecessors(node):
                    predecessorlvl = int((graphe.nodes[predecessor]["layer"]))
                    if predecessorlvl > max:
                        max = predecessorlvl
                graphe.nodes[node]["layer"] = max + 1
                nodelayer.append(node)
    return graphe


def niveaumax(graphe):
    listlayer = [(graphe.nodes[node]['layer']) for node in graphe.nodes()]
    maxlayer = max(listlayer)
    return maxlayer


def calculdateauplustot(graphe):
    dateauplustot = {}
    while len(dateauplustot) < len(graphe.nodes):
        for nod in graphe.nodes():
            listepredecesseurs = list(graphe.predecessors(nod))
            if nod not in dateauplustot:
                cheminmax = 0
                traite = True
                for pred in listepredecesseurs:
                    if pred in dateauplustot:
                        cheminmax = max(cheminmax, (dateauplustot[pred] + int(graphe.nodes.data("weight")[pred])))
                    else:
                        traite = False
                if traite:  # on n'inscrit la valeur du nœud dans la table que si on a traité tous ses predecesseurs !
                    dateauplustot[nod] = cheminmax
                    graphe.nodes[nod]['dateauplustot'] = cheminmax
    return graphe


def dateauplustard(graphe):
    # listesuccesseurs = []
    dateauplustard = {}
    dateauplustard['fin'] = (graphe.nodes['fin']['dateauplustot'])
    graphe.nodes['fin']['dateauplustard'] = graphe.nodes['fin']['dateauplustot']
    print("date au plus tot fin = date au plus tard = ", dateauplustard['fin'])
    while len(dateauplustard) < len(graphe):
        for nod in graphe.nodes():
            listesuccesseurs = list(graphe.successors(nod))
            if nod not in dateauplustard:
                mindepuisfin = dateauplustard['fin']
                traite = True
                for succ in listesuccesseurs:
                    if succ in dateauplustard:
                        mindepuisfin = min(mindepuisfin, (dateauplustard[succ] - int(graphe.nodes.data('weight')[nod])))
                    else:
                        traite = False
                if traite:
                    dateauplustard[nod] = mindepuisfin
                    graphe.nodes[nod]['dateauplustard'] = mindepuisfin
    return graphe


def calculmarges(graphe):
    for node in graphe.nodes():
        graphe.nodes[node]['marge'] = (graphe.nodes[node]['dateauplustard'] - graphe.nodes[node]['dateauplustot'])
    return graphe


def creationdebutfin(graphe):
    noeudsdefin = []
    for node in graphe.nodes():
        if not list(graphe.successors(node)):
            noeudsdefin.append(node)
    graphe.add_node('debut', layer=-1, weight=0)
    graphe.add_node('fin', layer=niveaumax(graphe) + 1, weight=0)
    for node in graphe.nodes():
        if graphe.nodes[node]['layer'] == 0:
            graphe.add_edge('debut', node)
    for node in noeudsdefin:
        graphe.add_edge(node, 'fin')
    return graphe


def chemincritique(graphe):
    for node in graphe.nodes():
        if int(graphe.nodes[node]['marge'])==0:
            nodecritique.append(node)
            graphe.nodes[node]['chemincritique']=True
        else:
            graphe.nodes[node]['chemincritique']=False
    return nodecritique,graphe




tableau = opencsv("test.csv")
# print("matrice : ",list(tableau))
G = graphegenerate(tableau)
G = graphelvl(G)
creationdebutfin(G)
#print("successeurs de : ", [(n, ":", list(G.successors(n))) for n in G.nodes()])
#print("nombre de niveaux de g : ", niveaumax(G) + 1)
nbreniveauxgraphinitial = niveaumax(G)
calculdateauplustot(G)
dateauplustard(G)
calculmarges(G)
nodecritique = []
chemincritique(G)
#print(list(G.predecessors('A')))
print(len(G.nodes), "node : ", G.nodes.data())
print("edge : ", G.edges.data())
print("niveau :", G.nodes.data("layer"))
print("dates au plus tôt : ", G.nodes.data("dateauplustot"))
print("date au plus tard : ", G.nodes.data("dateauplustard"))
print("marge : ", G.nodes.data("marge"))
print("chemin critique : ", G.nodes.data("chemincritique"))
print("list critique : ", nodecritique)


fig, ax = plt.subplots()
pos = nx.multipartite_layout(G, subset_key="layer")  # organise par niveau de tâche
nx.draw_networkx(G, pos=pos, ax=ax)
edge_labels = nx.draw_networkx_edge_labels(G, pos=pos, edge_labels=nx.get_edge_attributes(G, "weight"))
ax.set_title("Mon diagramme")
fig.tight_layout()
plt.show()

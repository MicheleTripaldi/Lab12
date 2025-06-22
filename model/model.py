import copy

import networkx as nx

from database.DAO import DAO


class Model:
    def __init__(self):
        self._retailer = None
        self._grafo = nx.Graph()
        self._idMap = {}



    def buildGraph(self,country,anno):
        self._grafo.clear()
        self._retailer = DAO.getAllRetailer(country)
        for r in self._retailer:
            self._idMap[r.Retailer_code] = r
        self._grafo.add_nodes_from(self._retailer)
        self.getAllEdges(country,anno)
        return self._grafo

    def getAllEdges(self,country,anno):
        edges = DAO.getAllEdges(country,anno,self._idMap)
        for ed in edges:
            self._grafo.add_edge(ed.nodo1,ed.nodo2, weight=ed.peso)

    def getVolumi(self):

        lista_tuple = []
        nodi = self._grafo.nodes()
        for nodo in nodi:
            vicini = self._grafo.neighbors(nodo)
            volume = 0
            stringa = ""
            for vicino in vicini:
                volume += self._grafo[nodo][vicino]["weight"]
            retailer = self._idMap[nodo.Retailer_code]
            nome = retailer.Retailer_name
            lista_tuple.append((volume, nome))
            """print(volume, nome)"""
        lista_tuple.sort(key=lambda x: x[0], reverse=True)
        return lista_tuple

    def getNumNodi(self):
        return len(self._grafo.nodes)

    def getNumArchi(self):
        return len(self._grafo.edges)

    ############################################################
    def percorsoOttimo(self, n):
        self._pesoMax = 0
        self._ottimo = []
        parziale = []
        self._ricorsione(parziale, n)
        return self._ottimo, self._pesoMax

    def _ricorsione(self, parziale, n):
        if len(parziale) == (n + 1):
            if self.calcolaPeso(parziale) > self._pesoMax:
                self._pesoMax = self.calcolaPeso(parziale)
                self._ottimo = copy.deepcopy(parziale)
        else:
            if len(parziale) == 0:
                for nodo in self._retailer:
                    parziale.append(nodo)
                    self._ricorsione(parziale, n)
                    parziale.pop()
            else:
                if len(parziale) < n:
                    for nodo in self._grafo.neighbors(parziale[-1]):
                        if nodo not in parziale:
                            parziale.append(nodo)
                            self._ricorsione(parziale, n)
                            parziale.pop()

                elif len(parziale) == n:
                    if parziale[0] in self._grafo.neighbors(parziale[-1]):
                        parziale.append(parziale[0])
                        self._ricorsione(parziale, n)
                        parziale.pop()

    def calcolaPeso(self, parziale):
        peso = 0

        for i in range(len(parziale) - 1):
            if self._grafo.has_edge(parziale[i], parziale[i + 1]):
                peso += self._grafo[parziale[i]][parziale[i + 1]]['weight']

        return peso
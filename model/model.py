import networkx as nx

from database.DAO import DAO


class Model:
    def __init__(self,):
        self._retailer = None
        self._grafo = nx.Graph()
        self._idMapRetailer = {}


    def buildGraph(self,country,anno):
        self._grafo.clear()
        self._retailer = DAO.getAllRetailer(country)
        for r in self._retailer:
            self._idMapRetailer[r.Retailer_code] = r
        self._grafo.add_nodes_from(self._retailer)
        self.getAllEdges(country,anno)
        return self._grafo

    def getAllEdges(self,country,anno):
        edges = DAO.getAllEdges(country,anno,self._idMapRetailer)
        for ed in edges:
            self._grafo.add_edge(ed.nodo1,ed.nodo2,weight = ed.peso)

    def getVolumi(self):
        volume_vendita = {}
        for retailer in self._grafo.nodes:
            volume = sum(data["weight"] for _, _, data in self._grafo.edges(retailer, data=True))
        # Ordina per volume decrescente
        retailer_ordinati = sorted(volume_vendita.items(), key=lambda x: x[1], reverse=True)
        return retailer_ordinati


    def getGradoNodo(self, nodo):
        return self._grafo.degree(nodo)


    def getNumNodi(self):
        return len(self._grafo.nodes)

    def getNumEdges(self):
        return len(self._grafo.edges)
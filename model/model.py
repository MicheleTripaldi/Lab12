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

    def getAllEdges(self,country,anno):
        edges = DAO.getAllEdges(country,anno,self._idMapRetailer)
        for ed in edges:
            self._grafo.add_edge(ed.nodo1,ed.nodo2,weight = ed.peso)


    def getNumNodi(self):
        return len(self._grafo.nodes)

    def getNumEdges(self):
        return len(self._grafo.edges)
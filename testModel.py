from database.DAO import DAO
from model.model import Model

myModel = Model()

G = myModel.buildGraph("France",2015)
print(myModel.getNumNodi(), myModel.getNumEdges())
lista_nodi = DAO.getAllRetailer("France")
n = 1
volume_vendita = {}
for retailer in G.nodes:
    volume = sum(data["weight"] for _, _, data in G.edges(retailer, data=True))
    """
    #G.edges(retailer, data=True):
    #Ottiene tutti gli archi incidenti al nodo retailer nel grafo G.
    Restituisce una lista (o iterator) di tuple:
    (nodo1, nodo2, attributi), dove:
    nodo1 e nodo2 sono i nodi collegati dall’arco,
    attributi è un dizionario con tutte le proprietà dell’arco (ad esempio, {"weight": 5}).
    for _, _, data in ...:
    Cicla su tutti questi archi, ignorando i nomi dei nodi (_ significa variabile “non usata”), e prende solo il dizionario data degli attributi.
    data["weight"]:
    Estrae il valore associato alla chiave "weight" dall’attributo dell’arco (cioè il peso).
    sum(...):
    Somma tutti questi pesi.
        volume_vendita[retailer] = volume
    """

# Ordina per volume decrescente
retailer_ordinati = sorted(volume_vendita.items(), key=lambda x: x[1], reverse=True)
print(retailer_ordinati)



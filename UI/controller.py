import flet as ft

from database.DAO import DAO
from model import model


class Controller:
    def __init__(self, view, model):
        # the view, with the graphical elements of the UI
        self._view = view
        # the model, which implements the logic of the program and holds the data
        self._model = model

        self._listYear = []
        self._listCountry = []

    def fillDD(self):
        county = DAO.getAllCountry()
        for c in county:
            self._view.ddcountry.options.append(ft.dropdown.Option(c))

        anno = [2015,2016,2017,2018]
        for a in anno:
            self._view.ddyear.options.append(ft.dropdown.Option(a))


    def handle_graph(self, e):
        country = self._view.ddcountry.value
        anno = self._view.ddyear.value

        if country is None or country == "":
            self._view.create_alert("No country selected")
            return
        if anno is None or anno == "":
            self._view.create_alert("No year selected")
            return

        # converto l'anno in intero
        try:
            anno = int(anno)
        except ValueError:
            self._view.txt_result.controls.clear()
            self._view.txt_result.controls.append(ft.Text(" data non valida"))
            self._view.update_page()
            return

        #creiamo il dizionario
        self._model.buildGraph(country, anno)
        self._view.txt_result.controls.append(ft.Text("Grafo creato correttamente"))
        self._view.txt_result.controls.append(ft.Text(f"il grafo ha: {self._model.getNumNodi()} nodi e {self._model.getNumArchi()} archi"))
        self._view.update_page()



    def handle_volume(self, e):
        country = self._view.ddcountry.value
        anno = self._view.ddyear.value

        if country is None or country == "":
            self._view.create_alert("No country selected")
            return
        if anno is None or anno == "":
            self._view.create_alert("No year selected")
            return

        # converto l'anno in intero
        try:
            anno = int(anno)
        except ValueError:
            self._view.txt_result.controls.clear()
            self._view.txt_result.controls.append(ft.Text(" data non valida"))
            self._view.update_page()
            return

        # creiamo il dizionario
        self._model.buildGraph(country, anno)

        volumi = self._model.getVolumi()
        self._view.txtOut2.controls.append(ft.Text(volumi))

        """OPPURE FACEVO COSI
        volumi = self._model.getVolumi()
        for i in range(0,len(volumi)):
            self._view.txt_result.controls.append(ft.Text(volumi[i]))
        """

        self._view.update_page()

    def handle_path(self, e):
        n = int(self._view.txtN.value)
        self._view.txtOut3.controls.clear()

        soluzione, peso = self._model.percorsoOttimo(n)
        self._view.txtOut3.controls.append(ft.Text(f"peso cammino massimo:{peso}"))
        for i in range(len(soluzione)-1):
                self._view.txtOut3.controls.append(ft.Text(f"{soluzione[i].Retailer_name} --> {soluzione[i+1].Retailer_name}: {self._model._grafo[soluzione[i]][soluzione[i+1]]['weight']}"))

        self._view.update_page()


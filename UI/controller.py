import flet as ft

from database.DAO import DAO


class Controller:
    def __init__(self, view, model):
        # the view, with the graphical elements of the UI
        self._view = view
        # the model, which implements the logic of the program and holds the data
        self._model = model

        self._listYear = []
        self._listCountry = []

    def fillDD(self):
        country = DAO.getAllCountry()
        for c in country:
            self._view.ddcountry.options.append(ft.dropdown.Option(c))


        anno = [2015,2016,2017,2018]
        for a in anno:
            self._view.ddyear.options.append(ft.dropdown.Option(a))

        self._view.update_page()


    def handle_graph(self, e):
        country = self._view.ddcountry.value
        anno = self._view.ddyear.value

        if country is None or country == "":
            self._view.create_alert("Seleziona una nazione")
            return

        if anno is None or anno  == "":
            self._view.create_alert("Seleziona un anno")
            return
        # converto in intero
        try:
            anno = int(anno)
        except ValueError:
            self._view.txt_result.controls.clear()
            self._view.txt_result.controls.append(ft.Text("data non valida"))
            self._view.update_page()
            return

        self._model.buildGraph(country,anno)
        self._view.txt_result.controls.append(ft.Text("Grafo correttamente creato"))
        self._view.txt_result.controls.append(ft.Text(f"numero di vertici: {self._model.getNumNodi()} - numero di archi: {self._model.getNumEdges()}"))
        self._view.update_page()







    def handle_volume(self, e):
        pass


    def handle_path(self, e):
        pass

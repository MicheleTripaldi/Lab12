from dataclasses import dataclass

from model.Retailer import Retailer


@dataclass
class Arco:
    nodo1: Retailer
    nodo2: Retailer
    peso: int
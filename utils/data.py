import requests
import pandas as pd


class CustomStructure:
    def __init__(self, data: dict):
        self.data = data

    def get(self, key: str, default = None):
        if not (key in self.data):
            return default
        elif self.data[key] is None:
            return default
        else:
            return self.data[key]


def get_pokedex() -> pd.DataFrame:
    """
    Fonction qui récupère les données des Pokémons. 

    Sortie
        données des Pokémons
    """
    pass


def get_types() -> pd.DataFrame:
    """
    Fonction qui récupère les données des types. 

    Sortie
        données des types
    """
    pass

import requests
import pandas as pd
import streamlit as st


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


@st.cache_data(ttl=3600,max_entries=1000,show_spinner=False)
def get_pokedex() -> pd.DataFrame:
    """
    Fonction qui récupère les données des Pokémons. 

    Sortie
        données des Pokémons
    """
    response = requests.get("https://tyradex.app/api/v1/pokemon",headers={"User-Agent": "RobotPokemon", "Content-type": "application/json"})
    if response.status_code==200:
        pokedex = response.json()
        data = []
        for p in pokedex:
            pokemon = CustomStructure(p)
            if pokemon.get("pokedex_id",0)==0:
                continue
            temp = {
                "id": pokemon.get("pokedex_id"),
                "generation": pokemon.get("generation"),
                "categorie": pokemon.get("category"),
                "nom_fr": pokemon.get("name",{}).get("fr"),
                "nom_en": pokemon.get("name",{}).get("en"),
                "sprite": pokemon.get("sprites",{}).get("regular"),
            }
            types = pokemon.get("types",[])
            if len(types)>0:
                temp["type_1"] = types[0].get("name")
            else:
                temp["type_1"] = None
            if len(types)==2:
                temp["type_2"] = types[1].get("name")
            else:
                temp["type_2"] = None
            temp["stat_pv"] = pokemon.get("stats",{}).get("hp")
            temp["stat_att"] = pokemon.get("stats",{}).get("atk")
            temp["stat_def"] = pokemon.get("stats",{}).get("def")
            temp["stat_att_spe"] = pokemon.get("stats",{}).get("spe_atk")
            temp["stat_def_spe"] = pokemon.get("stats",{}).get("spe_def")
            temp["stat_vit"] = pokemon.get("stats",{}).get("vit")
            temp["stat_tot"] = pokemon.get("stats",{}).get("hp",0)+pokemon.get("stats",{}).get("atk",0)+pokemon.get("stats",{}).get("def",0)+pokemon.get("stats",{}).get("spe_atk",0)+pokemon.get("stats",{}).get("spe_def",0)+pokemon.get("stats",{}).get("vit",0)
            evolution = CustomStructure(pokemon.get("evolution",{}))
            if len(evolution.get("pre",[]))>0:
                temp2 = []
                for pe in evolution.get("pre",[]):
                    temp2.append(str(pe.get("pokedex_id")))
                temp["pre_evolution"] = ", ".join(temp2)
            else:
                temp["pre_evolution"] = None
            if len(evolution.get("next",[]))>0:
                temp2 = []
                for ne in evolution.get("next",[]):
                    temp2.append(str(ne.get("pokedex_id")))
                temp["evolution"] = ", ".join(temp2)
            else:
                temp["evolution"] = None
            try:
                temp["taille_m"] = float(pokemon.get("height").replace(" m","").replace(",","."))
            except Exception:
                temp["taille_m"] = None
            try:
                temp["poids_kg"] = float(pokemon.get("weight").replace(" kg","").replace(",","."))
            except Exception:
                temp["poids_kg"] = None
            temp["sexe_m"] = pokemon.get("sexe",{}).get("male")
            temp["sexe_f"] = pokemon.get("sexe",{}).get("female")
            data.append(temp)
        return pd.DataFrame(data).set_index("id")
    else:
        print(f"Erreur {response.status_code} - {response.reason}")
        print(response.content)
        return None


@st.cache_data(ttl=3600,max_entries=1000,show_spinner=False)
def get_types() -> pd.DataFrame:
    """
    Fonction qui récupère les données des types. 

    Sortie
        données des types
    """
    response = requests.get("https://tyradex.app/api/v1/types",headers={"User-Agent": "RobotPokemon", "Content-type": "application/json"})
    if response.status_code==200:
        types = response.json()
        data = []
        for t in types:
            type = CustomStructure(t)
            temp = {
                "id": type.get("id"),
                "nom_fr": type.get("name",{}).get("fr"),
                "nom_en": type.get("name",{}).get("en"),
                "sprite": type.get("sprites"),
            }
            resistances = type.get("resistances",[])
            for temp2 in resistances:
                temp[temp2.get("name")] = temp2.get("multiplier")
            data.append(temp)
        return pd.DataFrame(data).set_index("id")
    else:
        print(f"Erreur {response.status_code} - {response.reason}")
        print(response.content)
        return None

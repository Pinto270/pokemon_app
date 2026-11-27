import pandas as pd
import streamlit as st
from streamlit_js_eval import streamlit_js_eval


window_width = streamlit_js_eval(js_expressions='window.innerWidth',default=704,key='WIDTH')


def increment(borne_sup: int):
    """
    Fonction qui incrémente l'indice de navigation. 

    Entrée
        borne_sup: borne supérieure de navigation
    """
    assert isinstance(borne_sup,int), f"borne_sup doit être un int, pas {type(borne_sup)}"
    st.session_state.indice = min(borne_sup,st.session_state.indice+1)


def decrement(borne_inf: int = 0):
    """
    Fonction qui décrémente l'indice de navigation. 
    
    Entrée
        borne_inf: borne inférieure de navigation
    """
    assert isinstance(borne_inf,int), f"borne_inf doit être un int, pas {type(borne_inf)}"
    st.session_state.indice = max(borne_inf,st.session_state.indice-1)


class PokedexPage:
    def __init__(self, chemin_donnees: str = "./donnees"):
        """
        Composant pour page de Pokédex. 

        Paramètre
            chemin_donnees: chemin du dossier des données
        """
        assert isinstance(chemin_donnees,str), f"chemin_donnees doit être un str, pas {type(chemin_donnees)}"
        self.pokedex = pd.read_csv(chemin_donnees+"/pokedex.csv",index_col=0)
        assert self.pokedex.index.names==["id"], "le pokédex doit avoir 'id' pour index"
        for col in ["generation","categorie","nom_fr","sprite","type_1","type_2","stat_pv","stat_att","stat_def","stat_att_spe","stat_def_spe","stat_vit","stat_tot","pre_evolution","evolution","taille_m","poids_kg"]:
            assert col in self.pokedex.columns, f"le pokédex doit contenir la colonne '{col}'"
        self.types = pd.read_csv(chemin_donnees+"/types.csv")
        for col in ["nom_fr","sprite","Normal","Plante","Feu","Eau","Électrik","Glace","Combat","Poison","Sol","Vol","Psy","Insecte","Roche","Spectre","Dragon","Ténèbres","Acier","Fée"]:
            assert col in self.types.columns, f"les types doit contenir la colonne '{col}'"
        self.types.set_index("nom_fr",inplace=True)

    def header(self):
        """
        Fonction qui affiche l'en-tête de la page. 
        """
        st.set_page_config(page_title="Pokédex",page_icon="📔")
        st.title("Pokédex")

    def settings(self) -> bool:
        """
        Fonction qui affiche et enregistre les réglages. 

        Sortie
            si le Pokédex est initialisé
        """
        st.header("Sélectionner une génération")
        gens_list = self.pokedex.generation.unique()
        gen = st.selectbox("Génération",options=gens_list,placeholder="Sélectionner une génération")
        self.pokemon_list = self.pokedex[self.pokedex.generation==gen].nom_fr.to_list()
        pokemon = st.selectbox("Pokémon",options=self.pokemon_list,placeholder="Sélectionner un Pokémon",disabled=gen is None)
        st.session_state.indice = self.pokemon_list.index(pokemon)
        if st.button("Sélectionner"):
            return True
        else:
            return False

    @st.fragment
    def navigation(self):
        """
        Fonction qui gère la navigation dans le Pokédex. 
        """
        st.progress((st.session_state.indice+1)/len(self.pokemon_list),f"Piste {st.session_state.indice+1}/{len(self.pokemon_list)}")
        with st.container(horizontal=True):
            st.button("< Précédent",on_click=decrement)
            st.space("stretch")
            st.button("Suivant >",on_click=increment,kwargs={"borne_sup": len(self.pokemon_list)-1})
        id = self.pokedex[self.pokedex.nom_fr==self.pokemon_list[st.session_state.indice]].index[0]
        pokemon = self.pokedex.loc[id]
        st.subheader(pokemon.nom_fr)
        st.text("")
        with st.container():
            st.markdown("**Informations**")
            if window_width<500:
                st.image(pokemon.sprite,width=300)
                st.text("")
                with st.container(width=300,horizontal=True,horizontal_alignment="center"):
                    st.image(self.types.loc[pokemon.type_1,"sprite"],width=50)
                    if pokemon.type_2==pokemon.type_2:
                        st.image(self.types.loc[pokemon.type_2,"sprite"],width=50)
                st.text("")
                st.text(f"Nom anglais : {pokemon.nom_en}")
                st.text(pokemon.categorie)
                st.text(f"Taille : {pokemon.taille_m} m")
                st.text(f"Poids : {pokemon.poids_kg} kg")
                st.text(f"{pokemon.sexe_f} % femelle ; {pokemon.sexe_m} % mâle")
            else:
                col1, col2 = st.columns(2)
                with col1:
                    st.image(pokemon.sprite,width=300)
                    st.text("")
                    with st.container(width=300,horizontal=True,horizontal_alignment="center"):
                        st.image(self.types.loc[pokemon.type_1,"sprite"],width=50)
                        if pokemon.type_2==pokemon.type_2:
                            st.image(self.types.loc[pokemon.type_2,"sprite"],width=50)
                with col2:
                    with st.container(height="stretch",vertical_alignment="center"):
                        st.text(f"Nom anglais : {pokemon.nom_en}")
                        st.text(pokemon.categorie)
                        st.text(f"Taille : {pokemon.taille_m} m")
                        st.text(f"Poids : {pokemon.poids_kg} kg")
                        st.text(f"{pokemon.sexe_f} % femelle ; {pokemon.sexe_m} % mâle")
        st.text("")
        with st.container():
            st.markdown("**Évolution**")
            evolutions = []
            if pokemon.pre_evolution==pokemon.pre_evolution:
                for i in pokemon.pre_evolution.split(", "):
                    evolutions.append(int(i))
            evolutions.append(id)
            if pokemon.evolution==pokemon.evolution:
                for i in pokemon.evolution.split(", "):
                    evolutions.append(int(i))
            with st.container(horizontal=True):
                if len(evolutions)==1:
                    st.text("Aucune lignée évolutive")
                else:
                    if window_width<500:
                        for i in evolutions:
                            st.image(self.pokedex.loc[i,"sprite"],width=100)
                    else:
                        col1, col2, col3 = st.columns(3)
                        with col1:
                            for i in range(0,len(evolutions),3):
                                st.image(self.pokedex.loc[evolutions[i],"sprite"],width=150)
                        with col2:
                            for i in range(1,len(evolutions),3):
                                st.image(self.pokedex.loc[evolutions[i],"sprite"],width=150)
                        with col3:
                            for i in range(2,len(evolutions),3):
                                st.image(self.pokedex.loc[evolutions[i],"sprite"],width=150)
        st.text("")
        with st.container():
            st.markdown("**Statistiques**")
            st.dataframe(pd.DataFrame({
                "Statistique": ["Points de vie","Attaque","Défense","Attaque spéciale","Défense spéciale","Vitesse","Total"],
                " ": [pokemon.stat_pv,pokemon.stat_att,pokemon.stat_def,pokemon.stat_att_spe,pokemon.stat_def_spe,pokemon.stat_vit,pokemon.stat_tot]
            }),hide_index=True)


pokedex = PokedexPage()
pokedex.header()

with st.sidebar:
    init = pokedex.settings()

with st.container():
    if init:
        pokedex.navigation()
    else:
        st.info("Aucun Pokémon n'est sélectionné.")

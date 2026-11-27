import random
import pandas as pd
import streamlit as st


@st.dialog("🎉 Nouveautés")
def new_features(texte: str):
    """
    Fonction qui affiche les nouveautés (dernières fonctionnalités). 

    Entrée
        texte: texte à afficher
    """
    assert isinstance(texte,str), f"texte doit être un str, pas {type(texte)}"
    st.markdown(texte)
    if st.button("OK"):
        st.session_state.show_news = False
        st.rerun()

@st.fragment(run_every=5)
def image(df: pd.DataFrame):
    """
    Fonction qui affiche des Pokémons au hasard toutes les 5 secondes. 

    Entrée
        df: données (images des Pokémons)
    """
    assert isinstance(df,pd.DataFrame), f"df doit être un DataFrame, pas {type(df)}"
    with st.container(horizontal=True):
        for i in random.sample(df.index.to_list(),k=3):
            st.image(pokedex.loc[i,"sprite"],width=200)

st.set_page_config(page_title="Accueil",page_icon="🏠")

if not ("show_news" in st.session_state):
    st.session_state.show_news = False

if st.session_state.show_news:
    new_features(
        """
        ### Nouvelles fonctionnalités
        - Fonctionnalité 1
        - Fonctionnalité 2
        """
    )


st.title("App Pokémon")

with st.container():
    st.text("Ce site contient 2 pages. Utilisez le menu sur la gauche pour passer d'une page à l'autre.")
    st.markdown("* **Quiz** : devinez le Pokémon.")
    st.markdown("* **Pokédex** : informations sur tous les Pokémons.")
    st.markdown("Les données proviennent de [Tyradex](https://tyradex.app).")

pokedex = pd.read_csv("donnees/pokedex.csv",index_col=0)
image(pokedex)

import random
import pandas as pd
import streamlit as st


class QuizPage:
    def __init__(self, chemin_donnees: str = "./donnees"):
        """
        Composant pour quiz Pokémon. 

        Paramètre
            chemin_donnees: chemin du dossier des données
        """
        assert isinstance(chemin_donnees,str), f"chemin_donnees doit être un str, pas {type(chemin_donnees)}"
        self.pokedex = pd.read_csv(chemin_donnees+"/pokedex.csv",index_col=0)
        assert self.pokedex.index.names==["id"], "le pokédex doit avoir 'id' pour index"
        for col in ["generation","categorie","nom_fr","sprite","type_1","type_2","stat_tot","pre_evolution","evolution","taille_m","poids_kg"]:
            assert col in self.pokedex.columns, f"le pokédex doit contenir la colonne '{col}'"
        self.types = pd.read_csv(chemin_donnees+"/types.csv")
        for col in ["nom_fr","sprite"]:
            assert col in self.types.columns, f"les types doit contenir la colonne '{col}'"
        self.types.set_index("nom_fr",inplace=True)
        self.pokemon_list = self.pokedex.nom_fr.to_list()
        self.pokemon_list.sort()
        self.answer = None
        self.guesses = None
        self.finished = False

    def header(self):
        """
        Fonction qui affiche l'en-tête de la page. 
        """
        st.set_page_config(page_title="Quiz",page_icon="📝")
        st.title("Devinez le Pokémon!")

    def settings(self) -> bool:
        """
        Fonction qui affiche et enregistre les réglages. 

        Sortie
            si le quiz est initialisé
        """
        st.header("Réglages de la partie")
        gens = st.multiselect("Si vous voulez une ou plusieurs génération(s) en particulier",options=self.pokedex.generation.unique(),default=None,placeholder="Sélectionner une ou plusieurs générations(s)")
        if st.button("Lancer la partie"):
            if len(gens)>0:
                self.pokedex = self.pokedex[self.pokedex.generation.isin(gens)].copy()
                self.pokemon_list = self.pokedex.nom_fr.to_list()
                self.pokemon_list.sort()
            return True
        return False

    def initialize_quiz(self):
        """
        Fonction qui initialise le quiz. 
        """
        self.answer = self.pokedex.loc[random.choice(self.pokedex.index)]
        self.answer_type = [self.answer.type_1]
        if self.answer.type_2==self.answer.type_2:
            self.answer_type.append(self.answer.type_2)
        self.guesses = []

    @st.fragment
    def navigation(self):
        """
        Fonction qui gère la navigation dans le quiz. 
        """
        st.progress(len(self.guesses)/6,f"Essai #{len(self.guesses)+1} sur 6")
        if len(self.guesses)>=3:
            with st.container(horizontal=True):
                st.markdown("**Type** : ")
                for t in self.answer_type:
                    st.image(self.types.loc[t,"sprite"],width=50)
        else:
            st.markdown(f"**Type** : révélée après 3 essais... 🔒")
        if len(self.guesses)>=5:
            st.markdown(f"**Catégorie** : {self.answer.categorie}")
        else:
            st.markdown(f"**Catégorie** : révélé après 5 essais... 🔒")
        for guess_i in self.guesses:
            i = self.pokedex[self.pokedex.nom_fr==guess_i].index[0]
            guess = self.pokedex.loc[i]
            with st.container(border=True):
                st.text(guess.nom_fr)
                with st.container(horizontal=True):
                    if guess.generation>self.answer.generation:
                        st.metric("Génération",guess.generation,delta="!=",delta_color="red",delta_arrow="down")
                    elif guess.generation<self.answer.generation:
                        st.metric("Génération",guess.generation,delta="!=",delta_color="red",delta_arrow="up")
                    else:
                        st.metric("Génération",guess.generation,delta="==",delta_color="green",delta_arrow="off")
                    guess_type = [guess.type_1]
                    if guess.type_2==guess.type_2:
                        guess_type.append(guess.type_2)
                    intersection = list(set(guess_type)&set(self.answer_type))
                    if guess_type==self.answer_type:
                        st.metric("Type"," - ".join(guess_type),delta="==",delta_color="green",delta_arrow="off")
                    elif len(intersection)>0:
                        st.metric("Type"," - ".join(guess_type),delta="!=",delta_color="yellow",delta_arrow="off")
                    else:
                        st.metric("Type"," - ".join(guess_type),delta="!=",delta_color="red",delta_arrow="off")
                    if guess.stat_tot>self.answer.stat_tot:
                        st.metric("Total stats",guess.stat_tot,delta="!=",delta_color="red",delta_arrow="down")
                    elif guess.stat_tot<self.answer.stat_tot:
                        st.metric("Total stats",guess.stat_tot,delta="!=",delta_color="red",delta_arrow="up")
                    else:
                        st.metric("Total stats",guess.stat_tot,delta="==",delta_color="green",delta_arrow="off")
                    if guess.taille_m>self.answer.taille_m:
                        st.metric("Taille (m)",guess.taille_m,delta="!=",delta_color="red",delta_arrow="down")
                    elif guess.taille_m<self.answer.taille_m:
                        st.metric("Taille (m)",guess.taille_m,delta="!=",delta_color="red",delta_arrow="up")
                    else:
                        st.metric("Taille (m)",guess.taille_m,delta="==",delta_color="green",delta_arrow="off")
                    if guess.poids_kg>self.answer.poids_kg:
                        st.metric("Poids (kg)",guess.poids_kg,delta="!=",delta_color="red",delta_arrow="down")
                    elif guess.poids_kg<self.answer.poids_kg:
                        st.metric("Poids (kg)",guess.poids_kg,delta="!=",delta_color="red",delta_arrow="up")
                    else:
                        st.metric("Poids (kg)",guess.poids_kg,delta="==",delta_color="green",delta_arrow="off")
        if len(self.guesses)>0:
            if self.guesses[-1]==self.answer.nom_fr:
                self.finished = True
                st.info(f"Bravo! Le Pokémon est {self.answer.nom_fr}.")
                st.image(self.answer.sprite,width=250)
            elif len(self.guesses)==6:
                self.finished = True
                st.info(f"Zut... Le Pokémon était {self.answer.nom_fr}.")
                st.image(self.answer.sprite,width=250)
        if self.finished:
            restart = st.button("Recommencer")
            if restart:
                st.rerun()
        else:
            guess_pokemon = st.selectbox("Votre réponse :",options=self.pokemon_list,index=None,help="Sélectionnez votre réponse, puis cliquez sur 'Soumettre'.",filter_mode="contains",placeholder="Sélectionner un Pokémon")
            submit = st.button("Soumettre",help="Cliquez 2 fois pour soumettre.",disabled=guess_pokemon is None)
            if submit:
                self.guesses.append(guess_pokemon)
                self.pokemon_list.remove(guess_pokemon)


quiz = QuizPage()
quiz.header()

with st.sidebar:
    init = quiz.settings()

if init:
    quiz.initialize_quiz()
    quiz.navigation()
else:
    st.info("La partie n'est pas lancée.")

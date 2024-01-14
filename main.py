import tkinter as tk
from PIL import Image, ImageTk
import requests
from io import BytesIO

class PokedexApp(tk.Tk):

    def __init__(self):
        super().__init__()
        self.title('Pokédex')
        self.geometry('640x512')  # Taille de la fenêtre
        self.resizable(width=False, height=False)

        # Charger et afficher l'image de fond du Pokédex
        self.pokedex_background = Image.open('pokedex.jpg').resize((640, 512))
        self.pokedex_photo = ImageTk.PhotoImage(self.pokedex_background)
        self.background_label = tk.Label(self, image=self.pokedex_photo)
        self.background_label.place(x=0, y=0, relwidth=1, relheight=1)

        # Zone d'affichage de l'image du Pokémon
        self.pokemon_image_label = tk.Label(self, bg="#453132")
        self.pokemon_image_label.place(x=100, y=170, width=140, height=120)

        # Labels pour le nom et le type du Pokémon
        self.pokemon_name_label = tk.Label(self, text="", fg="black", bg="#6BA66E")
        self.pokemon_name_label.place(x=85, y=380)

        self.pokemon_type_label = tk.Label(self, text="", fg="black", bg="#6BA66E")
        self.pokemon_type_label.place(x=85, y=400)

        # Initialisation des données des Pokémon
        self.pokemon_index = 0
        self.pokemon_data = self.load_pokemon_list()

        # Boutons de navigation
        self.prev_button = tk.Button(self, text='<<', command=self.show_previous_pokemon)
        self.prev_button.place(x=205, y=397, width=20, height=10)

        self.next_button = tk.Button(self, text='>>', command=self.show_next_pokemon)
        self.next_button.place(x=245, y=397, width=20, height=10)

        # Boutons pour gérer les équipes
        self.add_team1 = tk.Button(self, text='+', command=self.add_to_team1)
        self.add_team1.place(x=467, y=267, width=31, height=31)

        self.remove_team1 = tk.Button(self, text='-', command=self.remove_from_team1)
        self.remove_team1.place(x=503, y=267, width=31, height=31)

        self.add_team2 = tk.Button(self, text='+', command=self.add_to_team2)
        self.add_team2.place(x=349, y=349, width=31, height=31)

        self.remove_team2 = tk.Button(self, text='-', command=self.remove_from_team2)
        self.remove_team2.place(x=385, y=349, width=31, height=31)

        # Afficher le premier Pokémon
        self.show_pokemon()


        # Barre de recherche
        self.search_var = tk.StringVar()
        self.search_entry = tk.Entry(self, textvariable=self.search_var)
        self.search_entry.place(x=360, y=160, width=160, height=20)
        self.search_button = tk.Button(self, text='Rechercher', command=self.perform_search)
        self.search_button.place(x=360, y=190, width=80, height=20)

        # Initialiser les équipes
        self.team1 = []
        self.team2 = []
        self.team1_labels = []  # Labels pour les images de l'équipe 1
        self.team2_labels = []  # Labels pour les images de l'équipe 2

        self.init_team_labels()  # Initialiser les labels des équipes

    def init_team_labels(self):
        label_width = 35
        label_height = 32
        spacing = 37
        team1_start_x, team1_start_y = 336, 233  # Position de départ pour l'équipe 1
        team2_start_x, team2_start_y = 435, 321  # Position de départ pour l'équipe 2
        # Créer et positionner les labels de l'équipe 1
        for i in range(6):
            label_team1 = tk.Label(self, bg="#0093FF")
            label_team1.place(x=team1_start_x + (i * spacing), y=team1_start_y, width=label_width, height=label_height)
            self.team1_labels.append(label_team1)
            label_team2 = tk.Label(self, bg="#0093FF")
            label_team2.place(x=team2_start_x + (i * spacing), y=team2_start_y, width=label_width, height=label_height)
            self.team2_labels.append(label_team2)
            if i == 2:
                team1_start_y += 34
                team2_start_y += 34
                team1_start_x -= 111
                team2_start_x -= 111


    def load_pokemon_list(self):
        url = "https://pokeapi.co/api/v2/pokemon?limit=151"
        response = requests.get(url)
        return response.json()['results']

    def show_pokemon(self):
        pokemon_url = self.pokemon_data[self.pokemon_index]['url']
        response = requests.get(pokemon_url)
        pokemon_details = response.json()

        # Afficher l'image
        image_url = pokemon_details['sprites']['front_default']
        image_response = requests.get(image_url)
        image = Image.open(BytesIO(image_response.content)).resize((160, 160))
        photo = ImageTk.PhotoImage(image)
        self.pokemon_image_label.configure(image=photo)
        self.pokemon_image_label.image = photo

        # Afficher le nom et le type
        name = pokemon_details['name'].capitalize()
        type_name = pokemon_details['types'][0]['type']['name'].capitalize()
        self.pokemon_name_label.configure(text=f"Nom: {name}")
        self.pokemon_type_label.configure(text=f"Desc: Pokémon \r de type {type_name}")
    def show_next_pokemon(self):
        self.pokemon_index = (self.pokemon_index + 1) % 151
        self.show_pokemon()

    def show_previous_pokemon(self):
        self.pokemon_index = (self.pokemon_index - 1) % 151
        self.show_pokemon()

    def perform_search(self):
        search_text = self.search_var.get().lower()
        for i, pokemon in enumerate(self.pokemon_data):
            if search_text == pokemon['name']:
                self.pokemon_index = i
                self.show_pokemon()
                break

    def update_team_display(self, team, labels):

        for i in range(6):
            if i < len(team):
                pokemon = team[i]
                # Récupérer les détails du Pokémon
                pokemon_details_response = requests.get(pokemon['url'])
                if pokemon_details_response.status_code == 200:
                    pokemon_details = pokemon_details_response.json()

                    # Vérifier si la clé 'sprites' et 'front_default' sont présentes
                    if 'sprites' in pokemon_details and 'front_default' in pokemon_details['sprites']:
                        image_url = pokemon_details['sprites']['front_default']
                        image_response = requests.get(image_url)
                        if image_response.status_code == 200:
                            image = Image.open(BytesIO(image_response.content)).resize((35, 35))
                            photo = ImageTk.PhotoImage(image)
                            labels[i].configure(image=photo)
                            labels[i].image = photo  # Conserver une référence
                        else:
                            labels[i].configure(image='')
                    else:
                        labels[i].configure(image='')
                else:
                    labels[i].configure(image='')
            else:
                labels[i].configure(image='')

    def add_to_team1(self):
        if len(self.team1) < 6:
            self.team1.append(self.pokemon_data[self.pokemon_index])
            self.update_team_display(self.team1, self.team1_labels)

    def add_to_team2(self):
        if len(self.team2) < 6:
            self.team2.append(self.pokemon_data[self.pokemon_index])
            self.update_team_display(self.team2, self.team2_labels)

    def remove_from_team1(self):
        if self.team1:
            self.team1.pop()
            self.update_team_display(self.team1, self.team1_labels)

    def remove_from_team2(self):
        if self.team2:
            self.team2.pop()
            self.update_team_display(self.team2, self.team2_labels)


if __name__ == "__main__":
    app = PokedexApp()
    app.mainloop()

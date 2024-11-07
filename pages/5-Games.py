import streamlit as st
import random

# Liste des mots avec leur correspondance
# Format: {"anglais": "arabe"}
words = {
    "cat": "قطة",
    "dog": "كلب",
    "book": "كتاب",
    "sun": "شمس",
    "moon": "قمر",
    "tree": "شجرة",
    "star": "نجمة",
    "house": "بيت",
    "water": "ماء",
    "bread": "خبز"
}

# Dimensions de la grille
grid_size = 10
grid = [[" " for _ in range(grid_size)] for _ in range(grid_size)]

# Positionne les mots horizontalement ou verticalement dans la grille
def place_word(word, row, col, direction):
    if direction == "horizontal":
        if col + len(word) <= grid_size:
            for i, letter in enumerate(word):
                grid[row][col + i] = letter
            return True
    elif direction == "vertical":
        if row + len(word) <= grid_size:
            for i, letter in enumerate(word):
                grid[row + i][col] = letter
            return True
    return False

# Ajoute les mots aléatoirement dans la grille
placed_words = []
for english, arabic in words.items():
    word = english  # On peut choisir "arabic" si on veut faire l'inverse
    placed = False
    attempts = 0
    while not placed and attempts < 100:
        row, col = random.randint(0, grid_size - 1), random.randint(0, grid_size - 1)
        direction = random.choice(["horizontal", "vertical"])
        placed = place_word(word, row, col, direction)
        attempts += 1
    if placed:
        placed_words.append((english, arabic, row, col, direction))

# Interface Streamlit
st.title("Mots Croisés Bilingues (Arabe-Anglais)")
st.write("Essayez de deviner les mots en anglais en fonction des indices en arabe.")

# Affiche la grille avec des cases éditables pour que l'utilisateur puisse entrer ses réponses
for i in range(grid_size):
    cols = st.columns(grid_size)
    for j in range(grid_size):
        if grid[i][j] != " ":
            cols[j].text_input("", "", max_chars=1, key=f"{i}-{j}")
        else:
            cols[j].text(" ")

# Affiche les indices
st.write("\n### Indices :")
for english, arabic, row, col, direction in placed_words:
    st.write(f"{arabic} (en {direction} à partir de {row + 1}, {col + 1})")

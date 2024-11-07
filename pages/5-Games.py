import streamlit as st
import random

# Liste des mots avec leur correspondance en arabe
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

# Fonction pour placer les mots
def place_word(word, row, col, direction):
    if direction == "horizontal" and col + len(word) <= grid_size:
        for i, letter in enumerate(word):
            grid[row][col + i] = letter
        return True
    elif direction == "vertical" and row + len(word) <= grid_size:
        for i, letter in enumerate(word):
            grid[row + i][col] = letter
        return True
    return False

# Placer les mots aléatoirement dans la grille
placed_words = []
for english, arabic in words.items():
    placed = False
    attempts = 0
    while not placed and attempts < 100:
        row, col = random.randint(0, grid_size - 1), random.randint(0, grid_size - 1)
        direction = random.choice(["horizontal", "vertical"])
        placed = place_word(english, row, col, direction)
        attempts += 1
    if placed:
        placed_words.append((english, arabic, row, col, direction))

# Interface Streamlit
st.title("Mots Croisés Bilingues (Arabe-Anglais)")
st.write("Remplissez la grille en fonction des indices en arabe et vérifiez vos réponses.")

# Affichage de la grille avec numérotation des lignes et colonnes
st.write("### Grille")
grid_input = []
for i in range(grid_size):
    row_inputs = []
    cols = st.columns(grid_size + 1)
    cols[0].markdown(f"**{i+1}**")  # Numéro de ligne
    for j in range(grid_size):
        if grid[i][j] != " ":
            cell = cols[j + 1].text_input("", "", max_chars=1, key=f"{i}-{j}")
        else:
            cell = cols[j + 1].text(" ")
        row_inputs.append(cell)
    grid_input.append(row_inputs)

# Affiche la numérotation des colonnes en haut
st.write("**Colonne**")
col_numbers = "  ".join([f"{num+1:2}" for num in range(grid_size)])
st.write(col_numbers)

# Affichage des indices
st.write("### Indices")
for english, arabic, row, col, direction in placed_words:
    st.write(f"{arabic} : Mot en {direction} (ligne {row + 1}, colonne {col + 1})")

# Vérification de la solution
def check_solution():
    correct = True
    for english, arabic, row, col, direction in placed_words:
        if direction == "horizontal":
            user_input = "".join(grid_input[row][col:col + len(english)])
        else:  # direction == "vertical"
            user_input = "".join([grid_input[row + i][col] for i in range(len(english))])
        if user_input.lower() != english:
            correct = False
            break
    return correct

# Bouton pour vérifier
if st.button("Vérifier"):
    if check_solution():
        st.success("Félicitations ! Vous avez bien rempli la grille.")
    else:
        st.error("Certains mots sont incorrects. Essayez à nouveau.")


import streamlit as st
import pandas as pd

def encrypt_rail_fence(text, key):
    rail = [['' for _ in range(len(text))] for _ in range(key)]
    direction_down = False
    row, col = 0, 0

    for char in text:
        if row == 0 or row == key - 1:
            direction_down = not direction_down
        rail[row][col] = char  # Keep spaces during encryption
        col += 1
        row += 1 if direction_down else -1

    return rail

def decrypt_rail_fence(cipher, key):
    rail = [['' for _ in range(len(cipher))] for _ in range(key)]
    direction_down = None
    row, col = 0, 0

    # Marquer les positions dans le rail avec '*'
    for _ in range(len(cipher)):
        if row == 0 or row == key - 1:
            direction_down = not direction_down
        rail[row][col] = '*'
        col += 1
        row += 1 if direction_down else -1

    # Placer les caractères du texte chiffré dans le rail
    index = 0
    for i in range(key):
        for j in range(len(cipher)):
            if rail[i][j] == '*' and index < len(cipher):
                rail[i][j] = cipher[index]
                index += 1

    # Lire le texte déchiffré à partir du rail, y compris les espaces
    decrypted_text = []
    direction_down = False
    row, col = 0, 0

    for _ in range(len(cipher)):
        if row == 0 or row == key - 1:
            direction_down = not direction_down
        decrypted_text.append(rail[row][col])  # Lire chaque caractère
        col += 1
        row += 1 if direction_down else -1

    return ''.join(decrypted_text)


def render_rail(rail):
    data = pd.DataFrame(rail)
    data.columns = [f"Col{i}" for i in range(len(data.columns))]
    st.write("Visualisation des niveaux du Rail Fence :")
    st.dataframe(data.fillna(' '))

# Streamlit Interface
st.title("Rail Fence Cipher avec k niveaux")
st.write("Chiffrez ou déchiffrez un message en utilisant la méthode Rail Fence avec un fichier texte.")

# Upload a file
uploaded_file = st.file_uploader("Choisissez un fichier texte (.txt)", type=["txt"])

if uploaded_file is not None:
    message = uploaded_file.read().decode("utf-8")
    st.text(f"Message chargé : {message}")
else:
    st.warning("Veuillez importer un fichier texte pour continuer.")
    st.stop()

key = st.number_input("Entrez le nombre de niveaux (k) :", min_value=2, step=1)

action = st.radio("Choisissez une action :", ("Chiffrer", "Déchiffrer"))

if st.button("Exécuter"):
    if action == "Chiffrer":
        rail = encrypt_rail_fence(message, key)  # Maintain spaces during encryption
        cipher_text = ''.join([''.join(row) for row in rail if row])
        st.success(f"Message chiffré : {cipher_text}")
        render_rail(rail)
        # Provide download link for the encrypted text
        st.download_button(
            label="Télécharger le texte chiffré",
            data=cipher_text,
            file_name="message_chiffre.txt",
            mime="text/plain"
        )

    elif action == "Déchiffrer":
        rail = decrypt_rail_fence(message, key)
        decrypted_text = ''.join([''.join(row) for row in rail if row])
        st.success(f"Message déchiffré : {decrypted_text}")
        #render_rail(rail)  # Display the rail fence visualization with levels
            
            
            


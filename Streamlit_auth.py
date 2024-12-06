import streamlit as st
import pandas as pd


# Charger les données utilisateurs depuis un fichier CSV
def load_user_data(file_path="users.csv"):
    try:
        users_df = pd.read_csv(file_path)
        return users_df
    except FileNotFoundError:
        st.error("Le fichier users.csv est introuvable. Veuillez le créer.")
        return pd.DataFrame(
            columns=[
                "name",
                "password",
                "email",
                "failed_login_attempts",
                "logged_in",
                "role",
            ]
        )


# Sauvegarder les données utilisateurs dans un fichier CSV (optionnel)
def save_user_data(users_df, file_path="users.csv"):
    users_df.to_csv(file_path, index=False)


# Fonction d'authentification
def authenticate(username, password, users_df):
    user = users_df[users_df["name"] == username]
    if not user.empty and user["password"].values[0] == password:
        return True
    return False


# Charger les données utilisateurs
users_df = load_user_data()

# Vérifier si l'utilisateur est déjà connecté ou non
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if not st.session_state.logged_in:
    # Affichage de la page de connexion
    st.title("Login")
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")

    # Vérification que les champs ne sont pas vides
    if st.button("Login"):
        if username == "" or password == "":
            st.error("Veuillez entrer un nom d'utilisateur et un mot de passe.")
        elif authenticate(username, password, users_df):
            st.session_state.logged_in = True
            st.session_state.username = username
            st.success("Connexion réussie!")
            st.rerun()
        else:
            st.error("Nom d'utilisateur ou mot de passe incorrect.")
else:
    # Si l'utilisateur est connecté, afficher les pages de l'application
    user_role = users_df[users_df["name"] == st.session_state.username]["role"].values[
        0
    ]

    st.sidebar.header(f"Bienvenue {st.session_state.username} ({user_role})")

    # Menu de navigation
    menu = st.sidebar.selectbox(
        "Sélectionner une page", ("Accueil", "Les photos de mon chat", "Administration")
    )

    if menu == "Accueil":
        st.header("Streamlit is hell")
        st.image(
            "https://i.giphy.com/media/v1.Y2lkPTc5MGI3NjExa3pyY2pkYmU5MGlxNmg0aDZsM3luZXkxdnJsbTY4enhkYmI0OXN3eCZlcD12MV9pbnRlcm5hbF9naWZfYnlfaWQmY3Q9Zw/Lopx9eUi34rbq/giphy.gif",
            use_container_width=True,
        )

    elif menu == "Les photos de mon chat":
        st.header("Bienvenue dans l'album de mon chat 🐱")
        col1, col2, col3 = st.columns(3)

        with col1:
            st.image(
                "https://static.streamlit.io/examples/cat.jpg", caption="Chat"
            )  # changer la taille si l'envie
        with col2:
            st.image(
                "https://static.streamlit.io/examples/dog.jpg", caption="Chat Grand"
            )
        with col3:
            st.image(
                "https://static.streamlit.io/examples/owl.jpg", caption="Chat Volant"
            )

    elif menu == "Administration" and user_role == "admin":
        st.header("Administration")
        st.write("Vous avez accès à cette page car vous êtes un administrateur.")
        st.dataframe(users_df)

    # Déconnexion
    if st.sidebar.button("Déconnexion"):
        st.session_state.logged_in = False
        st.session_state.username = ""
        # Redirige directement vers la page de connexion sans avoir besoin de recharger la page
        st.rerun()

# pip freeze > requirements.txt

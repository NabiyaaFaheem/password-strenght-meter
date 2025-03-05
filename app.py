

import re
import random
import string
import streamlit as st
from datetime import datetime
import plotly.graph_objects as go

# Store last password in history
password_history = []

# Language options
LANGUAGES = {
    "English": {
        "title": "🔐 Password Strength Meter",
        "enter_password": "Enter your password:",
        "show_password": "Show password",
        "strength_score": "### Password Strength Score:",
        "strong": "✅ Strong Password!",
        "moderate": "⚠️ Moderate Password",
        "weak": "❌ Weak Password",
        "suggestions": "### Suggestions:",
        "generate_password": "Generate Strong Password",
        "password_history": "🕒 Last Saved Password"
    },
    "Spanish": {
        "title": "🔐 Medidor de Fortaleza de Contraseña",
        "enter_password": "Ingrese su contraseña:",
        "show_password": "Mostrar contraseña",
        "strength_score": "### Puntuación de Fortaleza de Contraseña:",
        "strong": "✅ ¡Contraseña Fuerte!",
        "moderate": "⚠️ Contraseña Moderada",
        "weak": "❌ Contraseña Débil",
        "suggestions": "### Sugerencias:",
        "generate_password": "Generar Contraseña Fuerte",
        "password_history": "🕒 Última Contraseña Guardada"
    },
    "French": {
        "title": "🔐 Indicateur de Sécurité du Mot de Passe",
        "enter_password": "Entrez votre mot de passe:",
        "show_password": "Afficher le mot de passe",
        "strength_score": "### Score de Sécurité du Mot de Passe:",
        "strong": "✅ Mot de Passe Fort!",
        "moderate": "⚠️ Mot de Passe Modéré",
        "weak": "❌ Mot de Passe Faible",
        "suggestions": "### Suggestions:",
        "generate_password": "Générer un Mot de Passe Fort",
        "password_history": "🕒 Dernier Mot de Passe Enregistré"
    },
    "German": {
        "title": "🔐 Passwort-Stärke-Messer",
        "enter_password": "Geben Sie Ihr Passwort ein:",
        "show_password": "Passwort anzeigen",
        "strength_score": "### Passwort-Sicherheitsbewertung:",
        "strong": "✅ Starkes Passwort!",
        "moderate": "⚠️ Moderates Passwort",
        "weak": "❌ Schwaches Passwort",
        "suggestions": "### Vorschläge:",
        "generate_password": "Starkes Passwort Generieren",
        "password_history": "🕒 Letztes Gespeichertes Passwort"
    }
}

# Function to check password strength
def check_password_strength(password):
    score = 0
    feedback = []
    
    if len(password) >= 8:
        score += 1
    else:
        feedback.append("Make it at least 8 characters long.")
    
    if re.search(r"[A-Z]", password):
        score += 1
    else:
        feedback.append("Include at least one uppercase letter.")
    
    if re.search(r"[a-z]", password):
        score += 1
    else:
        feedback.append("Include at least one lowercase letter.")
    
    if re.search(r"\d", password):
        score += 1
    else:
        feedback.append("Include at least one digit (0-9).")
    
    if re.search(r"[!@#$%^&*]", password):
        score += 1
    else:
        feedback.append("Include at least one special character (!@#$%^&*).")
    
    if re.search(r"(.)\1{2,}", password):
        feedback.append("Avoid repeated characters (e.g., 'aaa', '111').")
    
    common_passwords = ["password", "123456", "qwerty", "password123", "admin", "letmein"]
    if password.lower() in common_passwords:
        score = 1  # Automatically weak
        feedback = ["Avoid using common passwords like 'password123'."]
    
    return score, feedback

# Function to generate a strong password
def generate_strong_password():
    length = 12
    characters = string.ascii_letters + string.digits + "!@#$%^&*"
    return ''.join(random.choice(characters) for _ in range(length))

# Function to create a gauge chart
def create_gauge_chart(score):
    fig = go.Figure(go.Indicator(
        mode="gauge+number",
        value=score,
        domain={'x': [0, 1], 'y': [0, 1]},
        title={'text': "Password Strength"},
        gauge={
            'axis': {'range': [0, 5]},
            'bar': {'color': "blue" if score >= 4 else "orange" if score == 3 else "red"},
            'steps': [
                {'range': [0, 2], 'color': "red"},
                {'range': [2, 4], 'color': "orange"},
                {'range': [4, 5], 'color': "green"}
            ]
        }
    ))
    return fig

# Main function
def main():
    st.set_page_config(page_title="Password Strength Meter", layout="wide")
    selected_language = st.selectbox("🌍 Select Language", list(LANGUAGES.keys()))
    lang = LANGUAGES[selected_language]
    
    st.markdown(f"<h1 style='text-align: center; color: #4CAF50;'>{lang['title']}</h1>", unsafe_allow_html=True)
    
    password = st.text_input(lang['enter_password'], type="password")
    show_password = st.checkbox(lang['show_password'])
    if show_password and password:
        st.text(f"Your password: {password}")
    
    if password:
        score, feedback = check_password_strength(password)
        st.plotly_chart(create_gauge_chart(score))
        st.write(f"{lang['strength_score']} {score}/5")
        
        if score == 5:
            st.success(lang['strong'])
        elif score >= 3:
            st.warning(lang['moderate'])
        else:
            st.error(lang['weak'])
        
        if feedback:
            st.write(lang['suggestions'])
            for tip in feedback:
                st.write(f"- {tip}")
        
        password_history.clear()
        password_history.append(password)
    
    if st.button(lang['generate_password']):
        strong_password = generate_strong_password()
        st.write(f"**{lang['generate_password']}:** `{strong_password}`")
        password_history.clear()
        password_history.append(strong_password)
    
    if password_history:
        st.markdown(f"<h2 style='color: #FF9800;'>{lang['password_history']}</h2>", unsafe_allow_html=True)
        st.write(f"🔹 `{password_history[-1]}`")

if __name__ == "__main__":
    main()
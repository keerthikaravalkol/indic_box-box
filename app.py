import streamlit as st
import geocoder
from db import init_db, save_submission
import os

st.set_page_config(page_title="Indic Box-Box", layout="centered")
init_db()

# Session State for Login
if 'authenticated' not in st.session_state:
    st.session_state.authenticated = False

# Login
if not st.session_state.authenticated:
    st.title("🔐 Welcome to Indic Box-Box")
    user_email = st.text_input("Enter your email to start:")
    if st.button("Login") and user_email:
        st.session_state.authenticated = True
        st.session_state.email = user_email
        st.success("✅ Logged in successfully!")
        st.rerun()
    st.stop()

# Get Geo Info
g = geocoder.ip('me')
location = f"{g.city}, {g.country}" if g.ok else "Unknown"
latlng = g.latlng if g.ok else [None, None]

# UI Form
st.title("🏁 Submit Your Formula 1 Voice ✍️🎙️")

name = st.text_input("Your Name")

category = st.selectbox("Select F1 Category", [
    "Drivers", "Teams", "Cars", "Rules & Regulations", "Flags", "Tyres",
    "DRS", "F1 Circuits", "Fan Theories", "F1 Memes & Jokes", "Driver Rivalries"
])

language = st.selectbox("Select Language", [
    "English", "Telugu", "Hindi", "Tamil", "Kannada", "Malayalam", "Marathi", "Gujarati",
    "Bengali", "Punjabi", "Urdu", "Odia", "Assamese", "Other"
])

title = st.text_input("Title of your content")
content = st.text_area("Write your content (you can use any Indian language)")

# ✅ Upload audio only (no recording)
audio_file = st.file_uploader("Upload audio (optional)", type=["mp3", "wav", "m4a"])
audio_path = None

if audio_file:
    os.makedirs("audio", exist_ok=True)
    audio_path = os.path.join("audio", audio_file.name)
    with open(audio_path, "wb") as f:
        f.write(audio_file.read())
    st.audio(audio_path)

# Submit button
if st.button("Submit"):
    save_submission(
        name=name,
        email=st.session_state.email,
        location=location,
        lat=latlng[0],
        lon=latlng[1],
        category=category,
        language=language,
        title=title,
        content=content,
        audio_path=audio_path
    )

    st.success("✅ Your submission has been saved!")
    st.markdown(f"📍 Detected Location: **{location}** (Lat: {latlng[0]}, Lon: {latlng[1]})")

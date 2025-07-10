import streamlit as st

# 👇 MUST be first Streamlit command
st.set_page_config(page_title="🎬 Movie Recommender", layout="wide")

import pickle
import pandas as pd
import os

# ---------------- Load Pickled Data ----------------
import joblib
import streamlit as st

import pickle
import joblib

@st.cache_data
def load_data():
    movies = joblib.load("artifacts/movie_list_compressed.joblib")
    similarity = joblib.load("artifacts/similarity_compressed.joblib")
    return movies, similarity
    # movies = pickle.load(open("artifacts/movie_list.pkl", "rb"))
    # similarity = pickle.load(open("artifacts/similarity.pkl", "rb"))
    return movies, similarity

movies, similarity = load_data()


# Make sure artifacts folder exists
import streamlit as st
import os
import gdown
import joblib

# Make sure artifacts folder exists
if not os.path.exists("artifacts"):
    os.makedirs("artifacts")

# Google Drive file IDs
movie_list_id = "1aTaFxMtggJiCHJBpzC1bZrXT5Gccmmbo"
similarity_id = "1p_Y0LjDV8stiUaNsDZvzECJ6rydgt4yR"

# File paths
movie_list_path = "artifacts/movie_list_compressed.joblib"
similarity_path = "artifacts/similarity_compressed.joblib"

# Download files if not already present
if not os.path.exists(movie_list_path):
    gdown.download(f"https://drive.google.com/uc?id={movie_list_id}", movie_list_path, quiet=False)

if not os.path.exists(similarity_path):
    gdown.download(f"https://drive.google.com/uc?id={similarity_id}", similarity_path, quiet=False)

# Load the data
@st.cache_data
def load_data():
    movies = joblib.load(movie_list_path)
    similarity = joblib.load(similarity_path)
    return movies, similarity

movies, similarity = load_data()


# --- Sidebar ---
with st.sidebar:
    st.image("images/logo.JPG", use_container_width=True)
    st.title("🎥 Recommender")
    st.markdown("Created by: *Ebenezer Kwaw*")
    st.markdown("---")
    st.write("Select a movie to get content-based recommendations based on cast, crew, and keywords.")

# ---------------- Recommendation Logic ----------------
def recommend(movie):
    if movie not in movies['title'].values:
        return []
    index = movies[movies['title'] == movie].index[0]
    distances = sorted(list(enumerate(similarity[index])), key=lambda x: x[1], reverse=True)[1:6]
    recommended_titles = [movies.iloc[i[0]].title for i in distances]
    return recommended_titles

# ---------------- Main App UI ----------------
st.title("🎬 Movie Recommender System")
st.markdown("Select a movie and discover similar recommendations powered by NLP and cosine similarity.")

selected_movie = st.selectbox("🎞️ Choose a movie:", movies['title'].values)

if st.button("🚀 Recommend"):
    recommendations = recommend(selected_movie)
    if recommendations:
        st.subheader("🎯 Top Recommendations:")
        for i, rec in enumerate(recommendations, 1):
            st.markdown(f"**{i}.** {rec}")
    else:
        st.warning("Movie not found or no recommendations available.")

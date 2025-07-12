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
import gdown
import os
import joblib

def load_data():
    # Make sure the artifacts folder exists
    os.makedirs("artifacts", exist_ok=True)

    # File paths
    movie_file = "artifacts/movie_list_compressed.joblib"
    similarity_file = "artifacts/similarity.pkl"

    # Google Drive file IDs (from your links)
    movie_file_id = "1p_Y0LjDV8stiUaNsDZvzECJ6rydgt4yR"
    similarity_file_id = "1ojEtIeXADD8_s13QUfRT0Jzg68M3Y9I_"

    # gdown URLs
    movie_url = f"https://drive.google.com/uc?id={movie_file_id}"
    similarity_url = f"https://drive.google.com/uc?id={similarity_file_id}"

    # Download files if not present
    if not os.path.exists(movie_file):
        print("Downloading movie_list_compressed.joblib...")
        gdown.download(movie_url, movie_file, quiet=False, fuzzy=True)

    if not os.path.exists(similarity_file):
        print("Downloading similarity.pkl...")
        gdown.download(similarity_url, similarity_file, quiet=False, fuzzy=True)

    # Confirm files exist before loading
    if not os.path.exists(movie_file):
        raise FileNotFoundError(f"{movie_file} was not found after download.")
    if not os.path.exists(similarity_file):
        raise FileNotFoundError(f"{similarity_file} was not found after download.")

    # Load and return data
    movies = joblib.load(movie_file)
    similarity = joblib.load(similarity_file)

    return movies, similarity


@st.cache_data
def load_data():
    movies = joblib.load("artifacts/movie_list_compressed.joblib")
    similarity = joblib.load("artifacts/similarity_compressed.joblib")
    return movies, similarity
    # movies = pickle.load(open("artifacts/movie_list.pkl", "rb"))
    # similarity = pickle.load(open("artifacts/similarity.pkl", "rb"))
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

import streamlit as st
import requests
import pandas as pd

# Function to fetch the movie poster
def fetch_poster(movie_id):
    api_key = "2ab91ff72878bdf3fb7ee131d211345d"
    url = f"https://api.themoviedb.org/3/movie/{movie_id}?api_key={api_key}&language=en-US"
    data = requests.get(url)
    
    if data.status_code == 200:
        data = data.json()
        poster_path = data['poster_path']
        full_path = f"https://image.tmdb.org/t/p/w500/{poster_path}"
        return full_path
    else:
        return None

# Function to recommend movies
def recommend(movie):
    index = movies[movies['title'] == movie].index[0]
    distances = sorted(list(enumerate(similarity[index])), reverse=True, key=lambda x: x[1])
    recommended_movie_names = []
    recommended_movie_posters = []
    for i in distances[1:6]:
        # Fetch the movie poster
        movie_id = movies.iloc[i[0]].movie_id
        recommended_movie_posters.append(fetch_poster(movie_id))
        recommended_movie_names.append(movies.iloc[i[0]].title)

    return recommended_movie_names, recommended_movie_posters

# Load movie data and similarity matrix
movies = pd.read_pickle("model/movie.pkl")
similarity = pd.read_pickle("model/similarity.pkl")

# Set page title and favicon
st.set_page_config(
    page_title="Movie Recommender System",
    page_icon=":clapper:",
)

# Set app header with custom styles
st.title("🎬 Movie Recommender System")
st.markdown(
    """
    <style>
        div.stButton > button:first-child {
            background-color: #ff6347;
            color: white;
            font-weight: bold;
            padding: 10px;
            border-radius: 5px;
            border: none;
            cursor: pointer;
        }
        div.stButton > button:hover {
            background-color: #ff4500;
        }
    </style>
    """,
    unsafe_allow_html=True,
)

# Movie selection dropdown
selected_movie = st.selectbox(
    "Select a movie",
    movies['title'].values
)

# Button to show recommendations
if st.button('Show Recommendations'):
    recommended_movie_names, recommended_movie_posters = recommend(selected_movie)

    # Display recommended movies with posters
    col1, col2, col3, col4, col5 = st.columns(5)
    with col1:
        st.image(recommended_movie_posters[0], caption=recommended_movie_names[0], use_column_width=True)
    with col2:
        st.image(recommended_movie_posters[1], caption=recommended_movie_names[1], use_column_width=True)
    with col3:
        st.image(recommended_movie_posters[2], caption=recommended_movie_names[2], use_column_width=True)
    with col4:
        st.image(recommended_movie_posters[3], caption=recommended_movie_names[3], use_column_width=True)
    with col5:
        st.image(recommended_movie_posters[4], caption=recommended_movie_names[4], use_column_width=True)

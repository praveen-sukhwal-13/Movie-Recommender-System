import streamlit as st
import pickle
import requests

st.set_page_config(page_title="Moreso", page_icon="🎬", layout="wide")


# Cache the loading files to improve performance
@st.cache_data
def load_movies_data():
    return pickle.load(open("movies_list.pkl", 'rb'))


@st.cache_data
def load_similarity_data():
    return pickle.load(open("similarity.pkl", 'rb'))


movies = load_movies_data()
similarity = load_similarity_data()
movies_list = movies['title'].values

# Custom header styling
st.markdown(
    """
    <style>
        .header {
            font-size: 3rem;
            color: #1abc9c; /* Custom color for the header */
            font-weight: bold;
            text-align: center; /* Center-align the header */
            margin-top: 2rem;
            margin-bottom: 2rem;
        }
    </style>
    """, unsafe_allow_html=True)

# Display the header with the new style
st.markdown('<div class="header">Moreso</div>', unsafe_allow_html=True)

# Dropdown to select a movie
select_value = st.selectbox("Select movie from dropdown", movies_list)


@st.cache_data  # Used caching for improving performance
def fetch_poster(movie_id):
    api_key = "873c728f"
    url = f"http://www.omdbapi.com/?i={movie_id}&apikey={api_key}"
    data = requests.get(url)
    data = data.json()

    poster_path = data.get("Poster")
    if poster_path and poster_path != "N/A":
        return poster_path
    else:
        return "https://via.placeholder.com/500x750?text=No+Image+Available"


@st.cache_data
def recommend(movie):
    index = movies[movies['title'] == movie].index[0]
    distance = sorted(list(enumerate(similarity[index])), reverse=True, key=lambda vector: vector[1])
    recommend_movie = []
    recommend_poster = []
    for i in distance[1:6]:
        movies_id = movies.iloc[i[0]].id
        recommend_movie.append(movies.iloc[i[0]].title)
        recommend_poster.append(fetch_poster(movies_id))
    return recommend_movie, recommend_poster


# Show recommendations when the button is clicked
if st.button("Show Recommend"):
    movie_name, movie_poster = recommend(select_value)
    col1, col2, col3, col4, col5 = st.columns(5)

    with col1:
        st.text(movie_name[0])
        st.image(movie_poster[0])

    with col2:
        st.text(movie_name[1])
        st.image(movie_poster[1])

    with col3:
        st.text(movie_name[2])
        st.image(movie_poster[2])

    with col4:
        st.text(movie_name[3])
        st.image(movie_poster[3])

    with col5:
        st.text(movie_name[4])
        st.image(movie_poster[4])

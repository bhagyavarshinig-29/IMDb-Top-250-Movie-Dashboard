import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# ---------------------------------
# PAGE CONFIGURATION
# ---------------------------------

st.set_page_config(
    page_title="IMDb Movie Dashboard",
    page_icon="🎬",
    layout="wide"
)

st.title("🎬 IMDb Top 250 Movies Dashboard")
st.write("Interactive Movie Analytics and Data Exploration")

st.divider()

# ---------------------------------
# Q1. DATASET LOADING AND PREPARATION
# ---------------------------------

st.header("1. Dataset Loading and Preparation")

try:
    df = pd.read_csv("imdb_top_250.csv")

    st.success("IMDb Dataset Loaded Successfully!")

    st.subheader("First 10 Records")
    st.dataframe(df.head(10), use_container_width=True)

    st.subheader("Dataset Information")

    col1, col2 = st.columns(2)

    with col1:
        st.metric("Total Rows", df.shape[0])

    with col2:
        st.metric("Total Columns", df.shape[1])

    st.write("Column Names:")
    st.write(list(df.columns))

    st.write("Data Types:")
    st.write(df.dtypes.astype(str))

    st.write("Missing Values:")
    st.write(df.isnull().sum())

except FileNotFoundError:
    st.error("CSV file not found! Place imdb_top_250.csv in the project folder.")
    st.stop()

# ---------------------------------
# PREPARE DATA
# ---------------------------------

# Identify important columns

def find_column(possible_names):
    for name in possible_names:
        if name in df.columns:
            return name

    return None


title_col = find_column(["title", "Title", "primaryTitle", "originalTitle"])
rating_col = find_column(["averageRating", "rating", "Rating"])
votes_col = find_column(["numVotes", "votes", "NumVotes"])
genre_col = find_column(["genres", "genre", "Genres"])
country_col = find_column(["countriesOfOrigin", "country", "countries", "Country"])
gross_col = find_column(["grossWorldwide", "worldwideGross", "GrossWorldwide"])

if title_col is None or rating_col is None:
    st.error("Required title or averageRating column is missing.")
    st.write("Available columns:", list(df.columns))
    st.stop()

# Convert numeric columns

df[rating_col] = pd.to_numeric(df[rating_col], errors="coerce")

if votes_col:
    df[votes_col] = pd.to_numeric(df[votes_col], errors="coerce")
else:
    df["numVotes"] = 0
    votes_col = "numVotes"

if gross_col:
    df[gross_col] = pd.to_numeric(
        df[gross_col].astype(str).str.replace(r"[$,]", "", regex=True),
        errors="coerce"
    )

# ---------------------------------
# Q2. DASHBOARD KPI METRICS
# ---------------------------------

st.divider()

st.header("2. Movie Analytics Dashboard")

total_movies = len(df)
average_rating = df[rating_col].mean()
highest_rating = df[rating_col].max()
total_votes = df[votes_col].sum()

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric("Total Movies", f"{total_movies:,}")

with col2:
    st.metric("Average IMDb Rating", f"{average_rating:.2f}")

with col3:
    st.metric("Highest Rating", f"{highest_rating:.2f}")

with col4:
    st.metric("Total Votes", f"{total_votes:,.0f}")

st.success("Movie Analytics Dashboard Created Successfully!")

# ---------------------------------
# Q3. DATA VISUALIZATION
# ---------------------------------

st.divider()

st.header("3. Data Visualizations")

tab1, tab2, tab3, tab4 = st.tabs([
    "Genre Analysis",
    "Rating Analysis",
    "Rating vs Votes",
    "Worldwide Gross"
])

# Genre Analysis

with tab1:

    st.subheader("Number of Movies by Genre")

    if genre_col:

        genre_data = df[genre_col].dropna().astype(str).str.split(",")

        genre_data = genre_data.explode().str.strip()

        genre_counts = genre_data.value_counts()

        fig, ax = plt.subplots(figsize=(10, 5))

        genre_counts.plot(kind="bar", ax=ax)

        ax.set_title("Number of Movies in Each Genre")
        ax.set_xlabel("Genres")
        ax.set_ylabel("Number of Movies")
        plt.xticks(rotation=45)

        st.pyplot(fig)
        plt.close(fig)

    else:
        st.info("Genre column is not available.")

# Rating Analysis

with tab2:

    st.subheader("Distribution of IMDb Ratings")

    rating_data = df[rating_col].dropna()

    fig, ax = plt.subplots(figsize=(10, 5))

    ax.hist(rating_data, bins=15, edgecolor="black")

    ax.set_title("IMDb Rating Distribution")
    ax.set_xlabel("IMDb Rating")
    ax.set_ylabel("Number of Movies")

    st.pyplot(fig)
    plt.close(fig)

# Scatter Plot

with tab3:

    st.subheader("IMDb Rating vs Number of Votes")

    scatter_data = df.dropna(subset=[rating_col, votes_col])

    fig, ax = plt.subplots(figsize=(10, 5))

    ax.scatter(
        scatter_data[rating_col],
        scatter_data[votes_col],
        alpha=0.6
    )

    ax.set_title("IMDb Rating vs Number of Votes")
    ax.set_xlabel("Average IMDb Rating")
    ax.set_ylabel("Number of Votes")

    st.pyplot(fig)
    plt.close(fig)

# Worldwide Gross

with tab4:

    st.subheader("Top 10 Movies by Worldwide Gross")

    if gross_col:

        gross_data = df.dropna(subset=[gross_col])

        top_movies = gross_data.sort_values(
            by=gross_col,
            ascending=False
        ).head(10)

        fig, ax = plt.subplots(figsize=(12, 6))

        ax.bar(
            top_movies[title_col].astype(str),
            top_movies[gross_col]
        )

        ax.set_title("Top 10 Movies by Worldwide Gross")
        ax.set_xlabel("Movie Titles")
        ax.set_ylabel("Worldwide Gross")

        plt.xticks(rotation=45, ha="right")

        st.pyplot(fig)
        plt.close(fig)

        st.dataframe(
            top_movies[[title_col, gross_col]],
            use_container_width=True
        )

    else:
        st.info("Worldwide gross column is not available.")

# ---------------------------------
# Q4. DASHBOARD LAYOUT
# ---------------------------------

st.divider()

st.header("4. Additional Dataset Information")

with st.expander("View Dataset Information"):

    st.write("Total Records:", len(df))

    st.write("Total Columns:", len(df.columns))

    st.write("Available Columns:", list(df.columns))

    st.write("Available Movie Information:")

    st.write("Movie Title:", title_col)
    st.write("IMDb Rating:", rating_col)
    st.write("Votes:", votes_col)
    st.write("Genre:", genre_col)
    st.write("Country:", country_col)
    st.write("Worldwide Gross:", gross_col)

st.info("Explore the dashboard using the tabs and interactive filters.")

# ---------------------------------
# Q5. INTERACTIVE MOVIE EXPLORER
# ---------------------------------

st.divider()

st.header("5. Interactive Movie Explorer")

# Prepare genre options

if genre_col:

    all_genres = sorted(
        set(
            genre.strip()
            for values in df[genre_col].dropna().astype(str)
            for genre in values.split(",")
            if genre.strip()
        )
    )

else:
    all_genres = []

# Prepare country options

if country_col:

    all_countries = sorted(
        set(
            country.strip()
            for values in df[country_col].dropna().astype(str)
            for country in values.replace("[", "").replace("]", "").replace("'", "").replace('"', "").split(",")
            if country.strip()
        )
    )

else:
    all_countries = []

# Reset function

def reset_filters():

    st.session_state["genre_filter"] = "All"
    st.session_state["country_filter"] = []
    st.session_state["rating_filter"] = (
        float(df[rating_col].min()),
        float(df[rating_col].max())
    )
    st.session_state["votes_filter"] = 0
    st.session_state["search_filter"] = ""
    st.session_state["sort_filter"] = "Descending"

# Default values

if "genre_filter" not in st.session_state:
    st.session_state["genre_filter"] = "All"

if "country_filter" not in st.session_state:
    st.session_state["country_filter"] = []

if "rating_filter" not in st.session_state:
    st.session_state["rating_filter"] = (
        float(df[rating_col].min()),
        float(df[rating_col].max())
    )

if "votes_filter" not in st.session_state:
    st.session_state["votes_filter"] = 0

if "search_filter" not in st.session_state:
    st.session_state["search_filter"] = ""

if "sort_filter" not in st.session_state:
    st.session_state["sort_filter"] = "Descending"

col1, col2 = st.columns(2)

with col1:

    selected_genre = st.selectbox(
        "Select Movie Genre",
        ["All"] + all_genres,
        key="genre_filter"
    )

    selected_countries = st.multiselect(
        "Select Countries",
        all_countries,
        key="country_filter"
    )

    min_rating = float(df[rating_col].min())
    max_rating = float(df[rating_col].max())

    rating_range = st.slider(
        "Select IMDb Rating Range",
        min_value=min_rating,
        max_value=max_rating,
        value=st.session_state["rating_filter"],
        key="rating_filter"
    )

with col2:

    minimum_votes = st.number_input(
        "Minimum Number of Votes",
        min_value=0,
        value=0,
        step=1000,
        key="votes_filter"
    )

    search_title = st.text_input(
        "Search Movie Title",
        key="search_filter"
    )

    sort_order = st.radio(
        "Sort IMDb Ratings",
        ["Ascending", "Descending"],
        key="sort_filter"
    )

# Apply filters

filtered_df = df.copy()

if selected_genre != "All" and genre_col:

    filtered_df = filtered_df[
        filtered_df[genre_col].fillna("").str.contains(
            selected_genre,
            case=False,
            regex=False
        )
    ]

if selected_countries and country_col:

    country_pattern = "|".join(
        [country.replace("|", r"\|") for country in selected_countries]
    )

    filtered_df = filtered_df[
        filtered_df[country_col].fillna("").astype(str).str.contains(
            country_pattern,
            case=False,
            regex=True
        )
    ]

filtered_df = filtered_df[
    filtered_df[rating_col].between(
        rating_range[0],
        rating_range[1]
    )
]

filtered_df = filtered_df[
    filtered_df[votes_col] >= minimum_votes
]

if search_title:

    filtered_df = filtered_df[
        filtered_df[title_col].fillna("").astype(str).str.contains(
            search_title,
            case=False,
            regex=False
        )
    ]

filtered_df = filtered_df.sort_values(
    by=rating_col,
    ascending=(sort_order == "Ascending")
)

st.subheader("Filtered Movie Results")

st.metric("Movies Found", len(filtered_df))

st.dataframe(filtered_df, use_container_width=True)

st.button(
    "Reset All Filters",
    on_click=reset_filters
)

# ---------------------------------
# Q6. SESSION STATE AND FORM HANDLING
# ---------------------------------

st.divider()

st.header("6. Session State and Movie Search Form")

if "selected_movie" not in st.session_state:
    st.session_state.selected_movie = None

with st.form("movie_search_form"):

    st.subheader("Search for Your Favourite Movie")

    movie_title = st.text_input("Enter Movie Title")

    if all_genres:

        preferred_genre = st.selectbox(
            "Preferred Genre",
            all_genres
        )

    else:
        preferred_genre = st.selectbox(
            "Preferred Genre",
            ["All"]
        )

    minimum_rating = st.slider(
        "Minimum IMDb Rating",
        min_value=float(df[rating_col].min()),
        max_value=float(df[rating_col].max()),
        value=float(df[rating_col].min())
    )

    submitted = st.form_submit_button("Search Movie")

# Process form after submission

if submitted:

    search_results = df.copy()

    if movie_title.strip():

        search_results = search_results[
            search_results[title_col].fillna("").astype(str).str.contains(
                movie_title.strip(),
                case=False,
                regex=False
            )
        ]

    if preferred_genre != "All" and genre_col:

        search_results = search_results[
            search_results[genre_col].fillna("").astype(str).str.contains(
                preferred_genre,
                case=False,
                regex=False
            )
        ]

    search_results = search_results[
        search_results[rating_col] >= minimum_rating
    ]

    if not search_results.empty:

        st.session_state.selected_movie = search_results.iloc[0].to_dict()

        st.success("Matching Movie Found Successfully!")

    else:

        st.session_state.selected_movie = None

        st.info("No matching movie found. Try different search preferences.")

# Display selected movie

if st.session_state.selected_movie is not None:

    movie = st.session_state.selected_movie

    st.subheader("Selected Movie Information")

    st.write("Movie Title:", movie[title_col])

    st.write(
        "Genre:",
        movie[genre_col] if genre_col else "Not Available"
    )

    st.metric(
        "IMDb Rating",
        f"{movie[rating_col]:.2f}"
    )

    st.metric(
        "Number of Votes",
        f"{movie[votes_col]:,.0f}"
    )

    st.success("Movie Information Displayed Successfully!")

st.divider()

st.success("IMDb Movie Analytics Application Completed Successfully!")

st.caption("Streamlit Practical Examination | Maximum Marks: 50")
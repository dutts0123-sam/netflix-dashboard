import pandas as pd
import streamlit as st

st.markdown("""
<style>

/* Sidebar background */
[data-testid="stSidebar"] {
    background-color: #1E1E1E;
}

/* Sidebar text */
[data-testid="stSidebar"] * {
    color: white;
}

/* Sidebar header */
[data-testid="stSidebar"] h1,
[data-testid="stSidebar"] h2,
[data-testid="stSidebar"] h3 {
    color: #E50914;
}

/* Labels */
label {
    color: #FF6666 !important;
    font-weight: bold;
}

</style>
""", unsafe_allow_html=True)
import plotly.express as px
@st.cache_data
def load_data():
    df=pd.read_csv("netflix_data.csv")
    df["date_added"]=pd.to_datetime(df["date_added"],errors="coerce")
    df["year_added"]=df["date_added"].dt.year
    return df


st.set_page_config(page_title="Netflix Dashboard", layout="wide")

left, right = st.columns([8, 2])

# with right:
#     st.image( r"C:\Users\Sameer Dutt\Downloads\images.png", width=120)

# st.image(r"C:\Users\Sameer Dutt\Downloads\images.png", width=180)

st.markdown("""
<h1 style="color:#E50914;text-align:left;">
🎬 NETFLIX DASHBOARD
</h1>
""", unsafe_allow_html=True)

df = load_data()
st.sidebar.header("DASHBOARD FILTER ↓")

type_filter = st.sidebar.multiselect(
    "Select Content Type",
    options=df["type"].dropna().unique(),
    default=df["type"].dropna().unique()
)

country_filter = st.sidebar.multiselect(
    "Select Country",
    options=df["country"].dropna().unique()
)

rating_filter = st.sidebar.multiselect(
    "Select Rating",
    options=df["rating"].dropna().unique()
)

year_filter = st.sidebar.slider(
    "Select Release Year",
    int(df["release_year"].min()),
    int(df["release_year"].max()),
    (2000, 2021)
)

fil_df=df[df["type"].isin(type_filter)]
if country_filter:
    fil_df=fil_df[fil_df["country"].isin(country_filter)]
if rating_filter:
    fil_df=fil_df[fil_df["rating"].isin(rating_filter)]
if year_filter:
    fil_df=fil_df[(fil_df["release_year"]>=year_filter[0]) &
                  (fil_df["release_year"]<=year_filter[1])]
st.subheader("📊 KEY METRICS")
col1,col2,col3,col4=st.columns(4)
total=len(fil_df)
movies=len(fil_df[fil_df["type"]=="Movie"])
tvshows=len(fil_df[fil_df["type"]=="TV Show"])
countries=fil_df["country"].nunique()
col1.metric("Total Titles",total)
col2.metric("Movies",movies)
col3.metric("Tv Shows",tvshows)
col4.metric("Countries",countries)
st.divider()
col1, col2 = st.columns(2)

with col1:
    st.markdown("""
    <h3 style='color:#E50914;
               text-align:center;'>
    🎥 MOVIES VS TV SHOWS
    </h3>
    """, unsafe_allow_html=True)

    res = fil_df["type"].value_counts()

    fig = px.pie(
        names=res.index,
        values=res.values,
        color_discrete_sequence=px.colors.sequential.Reds
    )

    fig.update_layout(
        paper_bgcolor="#141414",
        plot_bgcolor="#141414",
        font=dict(color="white", size=16)
    )

    st.plotly_chart(fig, width="stretch")


with col2:
    st.markdown("""
    <h3 style='color:#E50914;
               text-align:center;'>
    📈 CONTENT OVER YEARS
    </h3>
    """, unsafe_allow_html=True)

    res1 = fil_df["year_added"].value_counts().sort_index()

    fig = px.line(
        x=res1.index,
        y=res1.values,
        markers=True
    )

    fig.update_traces(
        line=dict(color="#FF6666", width=3),
        marker=dict(size=8, color="#E50914")
    )

    fig.update_layout(
        paper_bgcolor="#141414",
        plot_bgcolor="#141414",
        font=dict(color="white", size=16),
        xaxis_title="Year Added",
        yaxis_title="Count"
    )

    st.plotly_chart(fig, width="stretch")

st.divider()
col1, col2 = st.columns(2)

with col1:
    st.markdown(
        "<h3 style='color:#E50914;'>TOP CONTENT PRODUCTING COUNTRIES</h3>",
        unsafe_allow_html=True
    )

    cnt_counts = fil_df["country"].value_counts().head(10)
    fig = px.bar(
        x=cnt_counts.values,
        y=cnt_counts.index,
        color=cnt_counts.values,
        color_continuous_scale="Reds"
    )
    st.plotly_chart(fig, width="stretch")

with col2:
    st.markdown(
        "<h3 style='color:#E50914;'>RATING DISTRIBUTION</h3>",
        unsafe_allow_html=True
    )

    rat_counts = fil_df["rating"].value_counts()
    fig = px.bar(
        x=rat_counts.index,
        y=rat_counts.values,
        color=rat_counts.values,
        color_continuous_scale="Reds"
    )
    st.plotly_chart(fig, width="stretch")

st.divider()

st.markdown(
    "<h3 style='color:#E50914;'>TOP GENRES</h3>",
    unsafe_allow_html=True
)

genres = fil_df["listed_in"].str.split(",").explode()
gencnt = genres.value_counts().head(10)

fig = px.bar(
    x=gencnt.index,
    y=gencnt.values,
    color=gencnt.values,
    color_continuous_scale="Reds"
)
st.plotly_chart(fig, width="stretch")

st.divider()

st.markdown(
    "<h3 style='color:#E50914;'>GLOBAL DISTRIBUTION OF CONTENT</h3>",
    unsafe_allow_html=True
)

cnt_values = (
    fil_df["country"]
    .dropna()
    .str.split(",")
    .explode()
    .str.strip()
    .replace("", pd.NA)
    .dropna()
    .value_counts()
    .reset_index(name="count")
)

fig = px.choropleth(
    cnt_values,
    locations="country",
    color="count",
    locationmode="country names",
    color_continuous_scale="Reds",
    range_color=(0, cnt_values["count"].max())
)

st.plotly_chart(fig, width="stretch")

st.divider()

st.markdown(
    "<h3 style='color:#E50914;'>DATASET PREVIEW</h3>",
    unsafe_allow_html=True
)

st.markdown("<h5 style='color:white;'>Enter title to search</h5>", unsafe_allow_html=True)
txtsrc = st.text_input("", placeholder="Search title...")

if txtsrc:
    fil_df = fil_df[fil_df["title"].str.contains(txtsrc, case=False)]

st.write(fil_df)
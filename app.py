import streamlit as st
import pandas as pd

# -------------------
# PAGE CONFIG
# -------------------

st.set_page_config(
    page_title="Approach per Count Index (ACI)",
    layout="wide"
)

# -------------------
# LOAD DATA
# -------------------

df = pd.read_csv("aci.csv")

# -------------------
# FORMAT DATA
# -------------------

df["ACI"] = df["ACI"].round(3)

# sort leaderboard first
df = df.sort_values(
    "ACI",
    ascending=False
).reset_index(drop=True)

# create rank column
df["Rank"] = df.index + 1

# reorder columns
df = df[
    ["Rank", "player_name", "batting_team", "ACI", "Pitches"]
]

# rename columns
df = df.rename(columns={
    "player_name": "Player",
    "batting_team": "Team",
    "Pitches": "Pitches Seen"
})

# -------------------
# TITLE
# -------------------

st.title("Approach per Count Index (ACI)")

st.markdown("""
ACI measures how often MLB hitters make a favorable swing/take decision based on:

- Count context
- Pitch location
- Personalized hot/cold zones
- Damage-hunting philosophy
- Intelligent 2-strike protection

Built using MLB Statcast data.
""")

# -------------------
# TEAM FILTER
# -------------------

teams = ["All Teams"] + sorted(df["Team"].dropna().unique())

selected_team = st.selectbox(
    "Filter by Team",
    teams
)

if selected_team != "All Teams":
    df = df[df["Team"] == selected_team]

# -------------------
# SEARCH
# -------------------

player_search = st.text_input("Search Player")

if player_search:
    df = df[
        df["Player"].str.contains(
            player_search,
            case=False,
            na=False
        )
    ]

# -------------------
# DISPLAY TABLE
# -------------------

st.dataframe(
    df,
    hide_index=True,
    use_container_width=True
)

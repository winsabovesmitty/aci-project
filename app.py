import streamlit as st
import pandas as pd

# -------------------
# PAGE CONFIG
# -------------------

st.set_page_config(
    page_title="Approach Count Index",
    layout="wide"
)

# -------------------
# LOAD DATA
# -------------------

df = pd.read_csv("aci.csv")

# -------------------
# CLEAN FORMATTING
# -------------------

df["ACI"] = df["ACI"].round(3)

df = df.rename(columns={
    "player_name": "Player",
    "batting_team": "Team",
    "ACI": "ACI",
    "Pitches": "Pitches Seen"
})

# -------------------
# TITLE
# -------------------

st.title("Approach per Count Index (ACI)")

st.markdown("""
ACI measures how often MLB hitters make the correct swing/take decision based on:

- Count context
- Pitch location
- Personalized hot/cold zones
- Damage-hunting philosophy
- Intelligent 2-strike protection

Built using MLB Statcast data.
""")

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
# SORTING DEFAULT
# -------------------

df = df.sort_values(
    "ACI",
    ascending=False
)

# -------------------
# DISPLAY TABLE
# -------------------

st.dataframe(
    df,
    hide_index=True,
    use_container_width=True
)

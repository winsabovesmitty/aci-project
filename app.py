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

st.caption(
    "Developed by Brandon Smith | https://medium.com/@WinsAboveSmitty"
)

st.markdown("""
**What is ACI:**  
ACI measures hitter approach quality by evaluating swing/take decisions through count leverage, pitch location, personalized hot/cold zones, and intelligent 2-strike protection using MLB Statcast data.

**Formula:**  
ACI = Good Decisions / Total Pitches Seen
- Each pitch is scored binary (1 = good decision, 0 = poor decision) based on count context.
- Only hitters in the top 25% of MLB pitch volume are included.

**Examples of "Good Decisions" include:**
- Swinging at damage pitches in advantage counts (e.g. 2-0, 2-1, 3-1)
- Taking edge/shadow pitches when ahead
- Attacking hitter-specific hot zones
- Punishing elevated hanging breaking balls
- Protecting competitive pitches with 2 strikes
- Taking obvious chase pitches with 2 strikes

**Example:**  
A take on the edge at 2-0 may be scored positively, while that same take at 2-2 may be scored negatively due to count leverage and protection expectations.
""")

# -------------------
# SECTION BREAK
# -------------------

st.divider()

st.subheader("2026 MLB Leaderboard")

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

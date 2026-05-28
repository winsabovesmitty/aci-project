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
# ROUND ACI VALUES
# -------------------

aci_cols = [
    "ACI",
    "ACI_20",
    "ACI_40",
    "ACI_80"
]

df[aci_cols] = df[aci_cols].round(3)

# -------------------
# SORT LEADERBOARD
# -------------------

df = df.sort_values(
    "ACI",
    ascending=False
).reset_index(drop=True)

# -------------------
# RANK
# -------------------

df["Rank"] = df.index + 1

# -------------------
# PERCENTILE
# -------------------

total_players = len(df)

df["Percentile"] = (
    (
        1 - ((df["Rank"] - 1) / total_players)
    ) * 100
).astype(int).astype(str) + "th"

# -------------------
# COLUMN ORDER
# -------------------

df = df[
    [
        "Rank",
        "player_name",
        "batting_team",
        "ACI",
        "ACI_20",
        "ACI_40",
        "ACI_80",
        "Percentile",
        "Pitches"
    ]
]

# -------------------
# RENAME COLUMNS
# -------------------

df = df.rename(columns={
    "player_name": "Player",
    "batting_team": "Team",
    "ACI": "Season ACI",
    "ACI_20": "20 PA",
    "ACI_40": "40 PA",
    "ACI_80": "80 PA",
    "Pitches": "Pitches Seen",
    "Percentile": "ACI Percentile"
})

# -------------------
# TITLE + METHODOLOGY
# -------------------

st.title("Approach per Count Index (ACI)")

st.caption(
    "Developed by Brandon Smith | https://medium.com/@WinsAboveSmitty"
)

st.markdown("""
**What is ACI:**  
ACI measures hitter approach quality by evaluating contextual swing/take decisions using MLB Statcast pitch-level data.

Unlike traditional offensive metrics, ACI is process-focused rather than outcome-focused, attempting to measure how consistently a hitter executes favorable offensive decisions based on count leverage and pitch context.

---

### Binary Pitch Scoring

Each pitch receives:
- `1` = favorable decision
- `0` = unfavorable decision

based on:
- count state
- pitch location
- swing/take behavior
- hitter-specific hot/cold zones
- damage opportunity
- 2-strike protection expectations

```text
ACI = Good Decisions / Total Pitches Seen

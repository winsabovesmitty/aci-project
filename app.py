import streamlit as st
import pandas as pd

# ==================================================
# PAGE CONFIG
# ==================================================

st.set_page_config(
    page_title="Approach per Count Index (ACI)",
    layout="wide"
)

# ==================================================
# LOAD DATA
# ==================================================

df = pd.read_csv("aci.csv")

# ==================================================
# ROUND ACI VALUES
# ==================================================

aci_cols = [
    "ACI",
    "ACI_20",
    "ACI_40",
    "ACI_80"
]

df[aci_cols] = df[aci_cols].round(3)

# ==================================================
# SORT LEADERBOARD
# ==================================================

df = df.sort_values(
    "ACI",
    ascending=False
).reset_index(drop=True)

# ==================================================
# CREATE RANK
# ==================================================

df["Rank"] = df.index + 1

# ==================================================
# CREATE PERCENTILE
# ==================================================

total_players = len(df)

df["Percentile"] = (
    (
        1 - ((df["Rank"] - 1) / total_players)
    ) * 100
).astype(int).astype(str) + "th"

# ==================================================
# COLUMN ORDER
# ==================================================

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

# ==================================================
# RENAME COLUMNS
# ==================================================

df = df.rename(columns={
    "player_name": "Player",
    "batting_team": "Team",
    "ACI": "Season ACI",
    "ACI_20": "20 PA",
    "ACI_40": "40 PA",
    "ACI_80": "80 PA",
    "Percentile": "ACI Percentile",
    "Pitches": "Pitches Seen"
})

# ==================================================
# PAGE HEADER
# ==================================================

st.title("Approach per Count Index (ACI)")

st.caption(
    "Developed by Brandon Smith | "
    "https://medium.com/@WinsAboveSmitty"
)

# ==================================================
# MODEL OVERVIEW
# ==================================================

st.markdown("""
### What is ACI?

Approach per Count Index (ACI) is a contextual hitting approach model built using MLB Statcast pitch-level data.

Rather than measuring offensive production, ACI attempts to measure:

> how consistently a hitter executes favorable swing/take decisions based on count leverage and pitch context.

ACI is intentionally process-focused rather than results-focused.

---

### Binary Pitch Scoring

Each pitch receives:

- `1` = favorable decision
- `0` = unfavorable decision

based on:
- count leverage
- pitch location
- swing/take behavior
- hitter-specific hot/cold zones
- damage opportunity
- 2-strike protection expectations

ACI = Good Decisions / Total Pitches Seen

Only hitters in the top 25% of MLB pitch volume are included.

---

### Count-Based Decision Framework

#### Hunting Counts
(0-0, 1-0, 2-0, 2-1, 3-1)

Expected behavior:
- attack damage pitches
- swing at hitter-specific hot zones
- punish elevated hanging breaking balls
- avoid passive misses on hittable pitches
- avoid expanding at chase pitches

#### Pivot Counts
(0-1, 1-1)

Expected behavior:
- maintain selective aggression
- attack mistake pitches
- avoid unnecessary chase expansion

#### Survival Counts
(All 2-strike counts)

Expected behavior:
- protect competitive pitches
- defend edge/shadow locations
- avoid obvious chase swings outside protection range

---

### Example Positive Decisions

Examples include:
- swinging at middle-middle fastballs in leverage counts
- attacking personalized hot zones
- taking edge pitches at 2-0 rather than expanding
- protecting competitive pitches with 2 strikes
- taking obvious chase pitches with 2 strikes

---

### Example Context Shift

A take on the edge at 2-0 may grade positively due to leverage and selectivity expectations, while that same take at 2-2 may grade negatively due to 2-strike protection expectations.

---

### Rolling Windows

The leaderboard includes:
- Season ACI
- Last 20 PA ACI
- Last 40 PA ACI
- Last 80 PA ACI

Trend colors compare rolling windows against Season ACI:
- Green = improving approach
- Yellow = stable approach
- Red = declining approach
""")

# ==================================================
# SECTION BREAK
# ==================================================

st.divider()

# ==================================================
# LEADERBOARD HEADER
# ==================================================

st.subheader("2026 MLB Leaderboard")

# ==================================================
# KPI CARDS
# ==================================================

league_aci = df["Season ACI"].mean()
league_20 = df["20 PA"].mean()
qualified_hitters = len(df)

kpi1, kpi2, kpi3 = st.columns(3)

with kpi1:
    st.metric(
        "MLB Avg Season ACI",
        f"{league_aci:.3f}"
    )

with kpi2:
    st.metric(
        "MLB Avg 20 PA ACI",
        f"{league_20:.3f}"
    )

with kpi3:
    st.metric(
        "Qualified Hitters",
        qualified_hitters
    )

st.caption(
    "Leaderboard sorted by Season ACI."
)

st.caption(
    "Trend colors compare rolling windows against Season ACI."
)

# ==================================================
# FILTERS
# ==================================================

filter_col1, filter_col2 = st.columns([1, 2])

teams = ["All Teams"] + sorted(
    df["Team"].dropna().unique()
)

with filter_col1:
    selected_team = st.selectbox(
        "Filter by Team",
        teams
    )

with filter_col2:
    player_search = st.text_input(
        "Search Player"
    )

# ==================================================
# APPLY FILTERS
# ==================================================

if selected_team != "All Teams":
    df = df[df["Team"] == selected_team]

if player_search:
    df = df[
        df["Player"].str.contains(
            player_search,
            case=False,
            na=False
        )
    ]

# ==================================================
# TREND COLORING
# ==================================================

def color_trend(val, season):

    if pd.isna(val):
        return ""

    delta = val - season

    # Improving
    if delta >= 0.015:
        return (
            "background-color: #d4edda; "
            "color: black;"
        )

    # Declining
    elif delta <= -0.015:
        return (
            "background-color: #f8d7da; "
            "color: black;"
        )

    # Stable
    else:
        return (
            "background-color: #fff3cd; "
            "color: black;"
        )

# ==================================================
# STYLE TABLE
# ==================================================

styled_df = (
    df.style
      .format({
          "Season ACI": "{:.3f}",
          "20 PA": "{:.3f}",
          "40 PA": "{:.3f}",
          "80 PA": "{:.3f}"
      })
      .apply(
          lambda row: [
              "",  # Rank
              "",  # Player
              "",  # Team
              "",  # Season ACI
              color_trend(
                  row["20 PA"],
                  row["Season ACI"]
              ),
              color_trend(
                  row["40 PA"],
                  row["Season ACI"]
              ),
              color_trend(
                  row["80 PA"],
                  row["Season ACI"]
              ),
              "",  # Percentile
              ""   # Pitches Seen
          ],
          axis=1
      )
)

# ==================================================
# DISPLAY TABLE
# ==================================================

st.dataframe(
    styled_df,
    hide_index=True,
    use_container_width=True
)

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
    "ACI_HUNT",
    "ACI_2K",
    "ACI_RISP",
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
        "ACI_HUNT",
        "ACI_2K",
        "ACI_RISP",
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
    "ACI_HUNT": "Hitter's Count ACI",
    "ACI_2K": "2-Strike ACI",
    "ACI_RISP": "RISP ACI",
    "ACI_20": "Last 20 PA",
    "ACI_40": "Last 40 PA",
    "ACI_80": "Last 80 PA",
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

Approach per Count Index (ACI) is a contextual decision-quality model built using MLB Statcast pitch-level data.

Rather than measuring offensive production, ACI attempts to measure how consistently a hitter executes favorable swing/take decisions based on count leverage, pitch context, damage opportunity, and chase discipline.

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

### Count Framework

| Count Type | Philosophy |
|---|---|
| Hunting Counts (0-0, 1-0, 2-0, 2-1, 3-1) | Attack damage pitches and hitter-specific hot zones while avoiding chase expansion |
| Pivot Counts (0-1, 1-1) | Maintain selective aggression and attack mistake pitches |
| 2-Strike Counts | Protect competitive pitches while avoiding obvious chase swings |

---

### Example Decisions

Positive decisions may include:
- attacking middle-middle fastballs in leverage counts
- punishing hanging breaking balls
- taking edge pitches at 2-0 rather than expanding
- protecting competitive pitches with 2 strikes
- taking obvious chase pitches with 2 strikes

A take on the edge at 2-0 may grade positively due to leverage and selectivity expectations, while that same take at 2-2 may grade negatively due to 2-strike protection expectations.

---

### Rolling Windows

The leaderboard includes:
- Season ACI
- Hitter's Count ACI
- 2-Strike ACI
- RISP ACI
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

st.caption(
    "Last Updated: 6/16/26"
)

# ==================================================
# KPI CARDS
# ==================================================

# ==================================================
# KPI CARDS
# ==================================================

league_aci = df["Season ACI"].mean()
league_hunt = df["Hitter's Count ACI"].mean()
league_2k = df["2-Strike ACI"].mean()
league_risp = df["RISP ACI"].mean()
qualified_hitters = len(df)

kpi1, kpi2, kpi3, kpi4, kpi5 = st.columns(5)

with kpi1:
    st.metric(
        "MLB Avg ACI",
        f"{league_aci:.3f}"
    )

with kpi2:
    st.metric(
        "MLB Avg Hitter's Count ACI",
        f"{league_hunt:.3f}"
    )

with kpi3:
    st.metric(
        "MLB Avg 2-Strike ACI",
        f"{league_2k:.3f}"
    )

with kpi4:
    st.metric(
        "MLB Avg RISP ACI",
        f"{league_risp:.3f}"
    )

with kpi5:
    st.metric(
        "Qualified Hitters",
        qualified_hitters
    )

st.caption(
    "Season ACI measures overall decision quality."
)

st.caption(
    "Situational ACIs evaluate approach quality in hitter's counts, "
    "2-strike counts, and runners-in-scoring-position situations."
)

st.caption(
    "Trend colors compare Last 20 / 40 / 80 PA ACI against Season ACI "
    "(Green = improving, Yellow = stable, Red = declining)."
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
    "Hitter's Count ACI": "{:.3f}",
    "2-Strike ACI": "{:.3f}",
    "RISP ACI": "{:.3f}",
    "Last 20 PA": "{:.3f}",
    "Last 40 PA": "{:.3f}",
    "Last 80 PA": "{:.3f}"
})
      .apply(
          lambda row: [
    "",  # Rank
    "",  # Player
    "",  # Team
    "",  # Season ACI
    "",  # Hitter's Count ACI
    "",  # 2-Strike ACI
    "",  # RISP ACI
    color_trend(
        row["Last 20 PA"],
        row["Season ACI"]
    ),
    color_trend(
        row["Last 40 PA"],
        row["Season ACI"]
    ),
    color_trend(
        row["Last 80 PA"],
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

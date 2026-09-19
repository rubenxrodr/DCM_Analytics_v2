# =========================================================
# WEEK OVERVIEW
# =========================================================

from pathlib import Path

import pandas as pd
import streamlit as st


# =========================================================
# PAGE CONFIG
# =========================================================

st.set_page_config(
    page_title="Week Overview",
    page_icon="🏀",
    layout="wide",
)


# =========================================================
# PATHS
# =========================================================

PROJECT_ROOT = Path(__file__).resolve().parents[2]

TEAM_OVERVIEW_DIR = (
    PROJECT_ROOT
    / "data"
    / "lineup"
)

DCM_PATH = (
    PROJECT_ROOT
    / "data"
    / "dcm"
    / "master"
    / "dcm_master.csv"
)

ATHLETICS_IMAGE_PATH = (
    PROJECT_ROOT
    / "yDashboard"
    / "assets"
    / "athletics.png"
)


# =========================================================
# LOAD DCM MASTER
# =========================================================

dcm_master = pd.read_csv(DCM_PATH)

# Remove leading "*" from column names
#dcm_master.columns = dcm_master.columns.str.lstrip("*")

# Week is stored as an integer in dcm_master
dcm_master["Week"] = pd.to_numeric(
    dcm_master["Week"],
    errors="coerce",
)

dcm_master = dcm_master.dropna(
    subset=["Week"]
)

dcm_master["Week"] = dcm_master["Week"].astype(int)


# =========================================================
# WEEK SELECTOR
# =========================================================
# =========================================================
# TITLE
# =========================================================

col1, col2 = st.columns([5, 1])

with col1:
    st.title("Week Overview")

IMAGE_PATH = PROJECT_ROOT / "yDashboard" / "assets" / "athletics.png"

with col2:
    st.image(IMAGE_PATH, width=100)

st.caption(
    "4A — Team-level offensive, defensive, and process performance"
)

st.divider()


available_weeks = sorted(
    dcm_master["Week"].unique()
)

selected_week = st.selectbox(
    "Week",
    available_weeks,
    index=len(available_weeks) - 1,
    format_func=lambda x: f"Week {int(x)}",
)


# =========================================================
# LOAD WEEKLY TEAM OVERVIEW
# =========================================================

team_overview_filename = (
    f"team_overview_4a_week{int(selected_week):02d}.csv"
)

TEAM_OVERVIEW_PATH = (
    TEAM_OVERVIEW_DIR
    / team_overview_filename
)

if TEAM_OVERVIEW_PATH.exists():

    team_overview = pd.read_csv(
        TEAM_OVERVIEW_PATH
    )

    team_overview.columns = (
        team_overview.columns.str.lstrip("*")
    )

else:

    team_overview = None

    st.warning(
        f"Team Overview data for Week {int(selected_week)} "
        "is not available yet."
    )


# =========================================================
# FILTER DCM MASTER
# =========================================================

dcm_week = dcm_master[
    dcm_master["Week"] == selected_week
].copy()


# =========================================================
# TEAM OVERVIEW
# =========================================================

if team_overview is not None:

    st.divider()

  
    # -----------------------------------------------------
    # TEAM DATA
    # -----------------------------------------------------

    # The weekly team overview file should contain one
    # team-level row.
    #
    # If multiple rows exist, use the first row for the
    # team-level cards.

    team = team_overview.iloc[0]




# =========================================================
# TEAM SNAPSHOT
# =========================================================

st.subheader("Team Snapshot")

col1, col2, col3, col4, col5,col6 = st.columns(6)

with col1:
    st.metric(
        "Minutes",
        f"{team['Minutes']:.1f}"
    )
teamtotalposs = team["Completed Def Poss"] + team["Completed Off Poss"]
with col2:
    st.metric(
        "Possessions",
        f"{teamtotalposs:.0f}"
    )

with col3 : 
    st.metric(
        "CompletedDefensive Possessions",
        f"{team['Completed Def Poss']:.0f}"
    )
with col4:
    st.metric(
        "PM / 40",
        f"{team['PM_p40']:.1f}"
    )

with col5:
    st.metric(
        "Net RTG",
        f"{team['Net_RTG']:.1f}"
    )

with col6:
    st.metric(
        "Plus / Minus",
        f"{team['Plus_Minus']:.0f}"
    )


st.divider()


# =========================================================
# OFFENSE
# =========================================================

st.header("Offense")

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric(
        "ORTG",
        f"{team['ORTG']:.1f}"
    )

with col2:
    st.metric(
        "Off PPP",
        f"{team['Off PPP']:.3f}"
    )

with col3:
    st.metric(
        "Score Rate",
        f"{team['Score Rate']:.1%}"
    )

with col4:
    st.metric(
        "Completed Off Poss",
        f"{team['Completed Off Poss']:.0f}"
    )


# ---------------------------------------------------------
# OFFENSIVE FOUR FACTORS
# ---------------------------------------------------------

st.subheader("Offensive Four Factors")

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric(
        "eFG%",
        f"{team['O_eFG%']:.1%}"
    )

with col2:
    st.metric(
        "TOV%",
        f"{team['O_TOV%']:.1%}"
    )

with col3:
    st.metric(
        "ORB%",
        f"{team['O_ORB%']:.1%}"
    )

with col4:
    st.metric(
        "FTR",
        f"{team['O_FTR']:.1%}"
    )


st.divider()


# =========================================================
# DEFENSE
# =========================================================

st.header("Defense")

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric(
        "DRTG",
        f"{team['DRTG']:.1f}"
    )

with col2:
    st.metric(
        "Def PPP",
        f"{team['Def PPP']:.3f}"
    )

with col3:
    st.metric(
        "Stop Rate",
        f"{team['Stop Rate']:.1%}"
    )

with col4:
    st.metric(
        "Completed Def Poss",
        f"{team['Completed Def Poss']:.0f}"
    )


# ---------------------------------------------------------
# DEFENSIVE FOUR FACTORS
# ---------------------------------------------------------

st.subheader("Defensive Four Factors")

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric(
        "eFG% Allowed",
        f"{team['D_eFG%']:.1%}"
    )

with col2:
    st.metric(
        "TOV% Forced",
        f"{team['D_TOV%']:.1%}"
    )

with col3:
    st.metric(
        "ORB% Allowed",
        f"{team['D_ORB%']:.1%}"
    )

with col4:
    st.metric(
        "FTR Allowed",
        f"{team['D_FTR']:.1%}"
    )


st.divider()


# =========================================================
# DEFENSIVE PROCESS
# =========================================================

st.header("Defensive Process")

st.caption(
    "How frequently our defensive behaviors occurred across defensive possessions."
)


# ---------------------------------------------------------
# POSSESSION OCCURRENCE
# ---------------------------------------------------------

st.subheader("Defensive Possession Occurrence")

col1, col2, col3, col4, col5 = st.columns(5)

with col1:
    st.metric(
        "Defensive Possessions",
        f"{team['Completed Def Poss']:.0f}"
    )
with col2:
    st.metric(
        "Middle",
        f"{team['Middle Possession Occurrence']:.1%}"
    )

with col3:
    st.metric(
        "Uncontested 3",
        f"{team['UC3 Possession Occurrence']:.1%}"
    )

with col4:
    st.metric(
        "Paint Touch",
        f"{team['Paint Touch Possession Occurrence']:.1%}"
    )

with col5:
    st.metric(
        "Deflection",
        f"{team['Deflection Possession Occurrence']:.1%}"
    )


# ---------------------------------------------------------
# RAW DEFENSIVE EVENTS
# ---------------------------------------------------------

st.subheader("Defensive Events")

col1, col2, col3, col4,col5 = st.columns(5)

with col2:
    st.metric(
        "Middle",
        f"{team['Middle']:.0f}"
    )

with col3:
    st.metric(
        "UC3",
        f"{team['UC3']:.0f}"
    )

with col4:
    st.metric(
        "Paint Touch",
        f"{team['Paint Touch']:.0f}"
    )

with col5:
    st.metric(
        "Deflections",
        f"{team['Deflection']:.0f}"
    )


st.divider()


# =========================================================
# DEFENSIVE OUTCOMES
# =========================================================

#st.header("Defensive Outcomes")
st.header("Turnover Margin and Stop vs Score Rate")

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric(
        "TOV Forced",
        f"{team['TOV Forced']:.0f}"
    )

with col2:
    st.metric(
        "LMU Turnovers",
        f"{team['TOV']:.0f}"
    )

with col3:
    oppscorerate = 1 - team["Stop Rate"]
    st.metric(
        "Opponent Score Rate",
        f"{oppscorerate:.0%}"
    )

with col4:
    st.metric(
        "LMU Score Rate",
        f"{team['Score Rate']:.0%}"
    )



#### =========================================================# =========================================================# =========================================================
#### =========================================================# =========================================================# =========================================================
# =========================================================
# FILTER DCM MASTER
# =========================================================

dcm_week = dcm_master[
    dcm_master["Week"] == selected_week
].copy()

# =========================================================
# DCM COMPONENT PROFILE
# =========================================================

st.divider()

st.header("DCM Component Profile")

st.caption(
    f"Defensive activity by player — Week {int(selected_week)}"
)

# ---------------------------------------------------------
# DISPLAY WEEKLY DCM MASTER
# ---------------------------------------------------------

display_columns = [
    "Player",
    "Defensive Possessions",
    "On-Ball Opportunities",
    "Boxout Opportunities",
    "Middle Drives",
    "Uncontested 3s",
    "Paint Touches",
    "Fouls",
    "Deflections",
    "Charges Taken",
    "Loose Balls Recovered",
    "Successful Boxouts",
    "O-Boards Allowed",
    "Missed Boxouts",
]

# Only use columns that actually exist
display_columns = [
    col for col in display_columns
    if col in dcm_week.columns
]

dcm_display = dcm_week[display_columns].copy()

st.dataframe(
    dcm_display,
    use_container_width=True,
    hide_index=True,
)


# =========================================================
# PLAYER SELECTOR
# =========================================================

st.subheader("Player Detail")

players = dcm_week["Player"].dropna().tolist()

selected_player = st.selectbox(
    "Select Player",
    players,
)

player_data = dcm_week[
    dcm_week["Player"] == selected_player
].iloc[0]


player_name = player_data["Player"]

# Extract jersey number if the name begins with #number
if isinstance(player_name, str) and player_name.startswith("#"):
    parts = player_name.split(" ", 1)
    jersey_number = parts[0]
    display_name = parts[1] if len(parts) > 1 else player_name
else:
    jersey_number = ""
    display_name = player_name


st.divider()


player_image = (
    PROJECT_ROOT
    / "yDashboard"
    / "assets"
    / f"{display_name}.webp"
)

header_col1, header_col2, header_col3 = st.columns(
    [2.3, 1.8, 2.3],
    gap="small"
)


# ---------------------------------------------------------
# LEFT — PLAYER PHOTO
# ---------------------------------------------------------

with header_col2:

    if player_image.exists():
        st.image(
            player_image,
            use_container_width=True
        )


# =========================================================
# OPPORTUNITY CONTEXT
# =========================================================

st.header("Defensive Opportunity Context")

st.caption(
    "DCM uses different opportunity denominators depending "
    "on the defensive behavior being measured."
)

col1, col2, col3 = st.columns(3)


with col1:

    st.subheader("Defensive Possessions")

    st.metric(
        "Possessions",
        f"{player_data['Defensive Possessions']:.0f}",
    )

    st.write(
        """
        All opponent possessions while the player was
        on the court.
        """
    )

    with col2:

        st.subheader("On-Ball Opportunities")

        st.metric(
            "Opportunities",
            f"{player_data['On-Ball Opportunities']:.0f}",
        )

        st.write(
            """
            Times the player was the primary defender on the
            ball or was in a closeout opportunity or help-side rotation.
            """
        )


with col3:

    st.subheader("Boxout Attempts")

    st.metric(
        "Opportunities",
        f"{player_data['Boxout Opportunities']:.0f}"
    )

    st.write(
        """
        Times the player tried to boxout the nearest opponent.
        """
    )


st.divider()

# =========================================================
# TIER 1 DCM  BREAKDOWN
# =========================================================

st.header("Tier 1 DCM  Breakdown")

st.caption(
    "Events the defense is trying to prevent."
)

col1, col2, col3 = st.columns(3)


with col1:

    st.subheader("Middle Drives")

    st.metric(
        "Middle Drives",
        f"{player_data['Middle Drives']:.0f}",
    )


with col2:

    st.subheader("Paint Touches")

    st.metric(
        "Paint Touches",
        f"{player_data['Paint Touches']:.0f}",
    )


with col3:

    st.subheader("Uncontested 3s")

    st.metric(
        "Uncontested 3s",
        f"{player_data['Uncontested 3s']:.0f}",
    )


st.divider()

# =========================================================
# DEFENSIVE ACTIVITY
# =========================================================

st.header("Defensive Activity")

st.caption(
    "Defensive actions involving discipline and disruption."
)

col1, col2, col3, col4 = st.columns(4)


with col1:

    st.subheader("Fouls")

    st.metric(
        "Fouls",
        f"{player_data['Fouls']:.0f}",
    )


with col2:

    st.subheader("Deflections")

    st.metric(
        "Deflections",
        f"{player_data['Deflections']:.0f}",
    )


with col3:

    st.subheader("Charges Taken")

    st.metric(
        "Charges",
        f"{player_data['Charges Taken']:.0f}",
    )

with col4:

    st.subheader("Loose Balls")

    st.metric(
        "Recovered",
        f"{player_data['Loose Balls Recovered']:.0f}",
    )


st.divider()


# =========================================================
# BOXOUT DETAIL
# =========================================================

st.header("Boxout Detail")

col1, col2, col3 = st.columns(3)


with col1:

    st.metric(
        "Successful Boxouts",
        f"{player_data['Successful Boxouts']:.0f}",
    )


with col2:

    st.metric(
        "Missed Boxouts",
        f"{player_data['Missed Boxouts']:.0f}",
    )


with col3:

    st.metric(
        "O-Boards Allowed",
        f"{player_data['O-Boards Allowed']:.0f}",
    )

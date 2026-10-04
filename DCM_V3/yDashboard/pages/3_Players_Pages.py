import streamlit as st
import pandas as pd
from pathlib import Path


# =========================================================
# PAGE CONFIG
# =========================================================

st.set_page_config(
    page_title="Individual DCM",
    page_icon="🏀",
    layout="wide",
)


# =========================================================
# PATHS
# =========================================================

PROJECT_ROOT = Path(__file__).resolve().parents[2]

DATA_PATH = (
    PROJECT_ROOT
    / "data"
    / "dcm"
    / "master"
    / "dcm_metric.csv"
)

DCMSEASON = (
    PROJECT_ROOT
    / "data"
    / "dcm"
    / "master"
    / "season_dcm.csv"
)

ASSETS_PATH = (
    PROJECT_ROOT
    / "yDashboard"
    / "assets"
    / "players"
)


# =========================================================
# LOAD DATA
# =========================================================

df = pd.read_csv(DATA_PATH)

# Remove leading "*" from column names.
# This keeps the dashboard terminology clean while allowing
# the existing CSV to retain its current schema.
df.columns = df.columns.str.lstrip("*")

dcm_season = pd.read_csv(DCMSEASON)

# =========================================================
# METRIC DEFINITIONS
# =========================================================

metrics = [
    {
        
        "name": "Middle Drive Frequency",
        "count": "Middle Drives",
        "frequency": "Middle Drive Frequency",
        "z": "Middle Drive Frequency Z-Score",
        "percentile": "Middle Drive Frequency Percentile",
        "direction": "↓ better",
        "description": "Limits dribble penetration into the middle.",
    },
    {
        
        "name": "Uncontested 3 Frequency",
        "count": "Uncontested 3s",
        "frequency": "UC3 Frequency",
        "z": "UC3 Frequency Z-Score",
        "percentile": "UC3 Frequency Percentile",
        "direction": "↓ better",
        "description": "Limits open threes off the closeout.",
    },
    {
        
        "name": "Paint Touches per Poss.",
        "count": "Paint Touches",
        "frequency": "Paint Touch Per Poss.",
        "z": "Paint Touch Per Poss. Z-Score",
        "percentile": "Paint Touch Per Poss. Percentile",
        "direction": "↓ better",
        "description": "Limits touches in the paint.",
    },
    {
        
        "name": "Foul Frequency",
        "count": "Fouls",
        "frequency": "Foul Frequency",
        "z": "Foul Frequency Z-Score",
        "percentile": "Foul Frequency Percentile",
        "direction": "↓ better",
        "description": "Limits free throws and keeps the defense on the floor.",
    },
    {
        
        "name": "Deflections per Poss.",
        "count": "Deflections",
        "frequency": "Deflection Per Poss.",
        "z": "Deflection Per Poss. Z-Score",
        "percentile": "Deflection Per Poss. Percentile",
        "direction": "↑ better",
        "description": "Disrupts passes and creates turnovers.",
    },
    {
        
        "name": "Charge Frequency",
        "count": "Charges Taken",
        "frequency": "Charge Frequency",
        "z": "Charge Frequency Z-Score",
        "percentile": "Charge Frequency Percentile",
        "direction": "↑ better",
        "description": "Takes charges and stops drives.",
    },
    {
        
        "name": "Loose Ball Frequency",
        "count": "Loose Balls Recovered",
        "frequency": "Loose Ball Recovered Frequency",
        "z": "Loose Ball Recovered Frequency Z-Score",
        "percentile": "Loose Ball Recovered Frequency Percentile",
        "direction": "↑ better",
        "description": "Creates extra possessions by securing loose balls.",
    },
    {
        
        "name": "Successful Boxout %",
        "count": "Successful Boxouts",
        "frequency": "Successful Boxout Frequency",
        "z": "Successful Boxout Frequency Z-Score",
        "percentile": "Successful Boxout Frequency Percentile",
        "direction": "↑ better",
        "description": "Executes boxouts to prevent second chances.",
    },
    {
        
        "name": "O-Board Allowed Frequency",
        "count": "O-Boards Allowed",
        "frequency": "OBoard Allowed Frequency",
        "z": "OBoard Allowed Frequency Z-Score",
        "percentile": "OBoard Allowed Frequency Percentile",
        "direction": "↓ better",
        "description": "Limits offensive rebounds given up.",
    },
]

# =========================================================
# PLAYER SELECTOR
# =========================================================

st.title("Individual Defensive Completeness")

st.caption(
    "L3 — Individual DCM profile"
)

player_names = df["Player"].tolist()

selected_player = st.selectbox(
    "Player",
    player_names,
)

player = df[
    df["Player"] == selected_player
].iloc[0]




# =========================================================
# BUILD METRIC TABLE
# =========================================================

metric_rows = []

for metric in metrics:

    frequency_value = player[metric["frequency"]]
    z_value = player[metric["z"]]
    percentile_value = player[metric["percentile"]]

    # Format frequency based on the type of metric
    if metric["name"] == "Successful Boxout %":
        frequency_display = f"{frequency_value:.1%}"
    else:
        frequency_display = f"{frequency_value:.2f}"

    metric_rows.append(
        {
            "DCM Metric": metric["name"],
            #"Count": int(player[metric["count"]]),
            "Frequency": frequency_display,
            "Z-Score": f"{z_value:+.2f}",
            "Percentile": f"{percentile_value:.0f}",
            "Direction": metric["direction"],
        }
    )

metric_table = pd.DataFrame(metric_rows)



def get_display_name(player_name):

    if isinstance(player_name, str) and player_name.startswith("#"):
        parts = player_name.split(" ", 1)
        return parts[1] if len(parts) > 1 else player_name


    return player_name
# =========================================================
# PLAYER NAME
# =========================================================


player_name = player["Player"]

display_name = get_display_name(player_name)

if isinstance(player_name, str) and player_name.startswith("#"):
    jersey_number = player_name.split(" ", 1)[0]
else:
    jersey_number = ""

display_name = get_display_name(player_name)
st.divider()


player_image = (
    PROJECT_ROOT
    / "yDashboard"
    / "assets"
    / f"{display_name}.webp"
)
# =========================================================







# =========================================================
# PLAYER HEADER
# =========================================================

scale_img_path = (
    PROJECT_ROOT
    / "yDashboard"
    / "assets"
    / "dcm_rating_scale.png"
)

header_col1, header_col2, header_col3 = st.columns(
    [1.1, 2.2, 1.1],
    gap="large"
)


# ---------------------------------------------------------
# LEFT — PLAYER PHOTO
# ---------------------------------------------------------

with header_col1:

    if player_image.exists():
        st.image(
            player_image,
            use_container_width=True
        )


# ---------------------------------------------------------
# CENTER — PLAYER INFO
# ---------------------------------------------------------

with header_col2:

   
    st.markdown(
        f"""
        <h1 style="
            margin-bottom:0px;
            font-size:42px;
        ">
            {display_name.upper()}
        </h1>
        """,
        unsafe_allow_html=True,
    )

    if jersey_number:
        st.markdown(
            f"""
            <div style="
                font-size:20px;
                margin-bottom:20px;
            ">
                {jersey_number}
            </div>
            """,
            unsafe_allow_html=True,
        )

    st.markdown("### Defensive Profile")

    st.write(
        f"""
        **Defensive Possessions:** 
        {player["Defensive Possessions"]:.0f}
        """
    )

    st.divider()

    score_col, rating_col = st.columns(2)

    with score_col:

        st.markdown(
            """
            <div style="
                font-size:16px;
                font-weight:600;
            ">
                DCM SCORE
            </div>
            """,
            unsafe_allow_html=True,
        )

        st.markdown(
            f"""
            <div style="
                font-size:64px;
                font-weight:800;
                line-height:1;
            ">
                {player["DCM"]:.2f}
            </div>
            """,
            unsafe_allow_html=True,
        )

        st.caption("OUT OF 7")


    with rating_col:

        dcm_rating = round(player["DCM"])

        # Keep rating inside the 1–7 scale
        dcm_rating = max(1, min(7, dcm_rating))

        st.markdown(
            """
            <div style="
                font-size:16px;
                font-weight:600;
            ">
                DCM RATING
            </div>
            """,
            unsafe_allow_html=True,
        )

        st.markdown(
            f"""
            <div style="
                font-size:64px;
                font-weight:800;
                line-height:1;
            ">
                {dcm_rating}
            </div>
            """,
            unsafe_allow_html=True,
        )

        st.caption("1–7 SCALE")




# ---------------------------------------------------------
# RIGHT — DCM RATING SCALE
# ---------------------------------------------------------

with header_col3:

    if scale_img_path.exists():
        st.markdown(
            "<div style='height:80px;'></div>",
            unsafe_allow_html=True
        )

        st.image(
            scale_img_path,
            use_container_width=True
        )



# =========================================================
# OPPORTUNITY CONTEXT
# =========================================================

st.header("Defensive Opportunity Context")

st.caption(
    "DCM uses different opportunity denominators depending on the defensive behavior being measured."
)


col1, col2, col3 = st.columns(3)


with col2:

    st.subheader("On-Ball Opportunities")

    st.metric(
        "Opportunities",
        f"{player['On-Ball Opportunities']:.0f}",
    )

    st.write(
        """
        Times the player was the primary defender on the
        ball or was in a closeout opportunity or help-side rotation.
        """
    )


with col1:

    st.subheader("Defensive Possessions")

    st.metric(
        "Possessions",
        f"{player['Defensive Possessions']:.0f}",
    )

    st.write(
        """
        All opponent possessions while the player was
        on the court.
        """
    )


with col3:

    st.subheader("Boxout Opportunities")

    st.metric(
        "Opportunities",
        f"{player['Boxout Opportunities']:.0f}",
    )

    st.write(
        """
        Times the player had a true opportunity to boxout the nearest opponent.
        """
    )


st.divider()


# =========================================================
# Tier 1 DCM BREAKDOWN
# =========================================================

st.header("Tier 1 DCM Breakdown")

st.caption(
    "Events the defense is trying to prevent."
)

col1, col2, col3 = st.columns(3)


with col1:

    st.subheader("Middle Drives")

    st.metric(
        "Middle Drives",
        f"{player['Middle Drives']:.0f}",
    )


with col2:

    st.subheader("Paint Touches")

    st.metric(
        "Paint Touches",
        f"{player['Paint Touches']:.0f}",
    )


with col3:

    st.subheader("Uncontested 3s")

    st.metric(
        "Uncontested 3s",
        f"{player['Uncontested 3s']:.0f}",
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
        f"{player['Fouls']:.0f}",
    )


with col2:

    st.subheader("Deflections")

    st.metric(
        "Deflections",
        f"{player['Deflections']:.0f}",
    )


with col3:

    st.subheader("Charges Taken")

    st.metric(
        "Charges",
        f"{player['Charges Taken']:.0f}",
    )

with col4:

    st.subheader("Loose Balls")

    st.metric(
        "Recovered",
        f"{player['Loose Balls Recovered']:.0f}",
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
        f"{player['Successful Boxouts']:.0f}",
    )

with col2:
    st.metric(
        "Missed Boxouts",
        f"{player['Missed Boxouts']:.0f}",
    )

with col3:
    st.metric(
        "O-Boards Allowed",
        f"{player['O-Boards Allowed']:.0f}",
    )


       
# =========================================================
# NINE DCM METRICS
# =========================================================

st.header("The 9 DCM Process Metrics")


st.caption(
    "Each metric evaluates a specific defensive behavior relative "
    "to the opportunity available to the player."
)
st.caption(
    "Z-score measures how far a player's performance is from the team "
    "average in standard deviation units. Percentile shows the player's "
    "relative standing within the team. A z-score of 0 represents the "
    "team average, while a percentile of 50 represents the team median. "
    "Higher values indicate better defensive performance. When dealing with small sample sizes, " \
    "z-scores are more reliable than percentiles, which can be skewed by outliers."
)





# =========================================================
# BUILD METRIC TABLE
# =========================================================
metric_rows = []

for metric in metrics:

    frequency_value = player[metric["frequency"]]
    z_value = player[metric["z"]]
    percentile_value = player[metric["percentile"]]

    # Format frequency based on the type of metric
    if metric["name"] == "Successful Boxout %":
        frequency_display = f"{frequency_value:.1%}"
    else:
        frequency_display = f"{frequency_value:.2f}"

    metric_rows.append(
        {
            "DCM Metric": metric["name"],
            #"Count": int(player[metric["count"]]),
            "Frequency": frequency_display,
            "Z-Score": f"{z_value:+.2f}",
            "Percentile": f"{percentile_value:.0f}",
            "Direction": metric["direction"],
        }
    )

metric_table = pd.DataFrame(metric_rows)


# =========================================================
# DISPLAY TABLE
# =========================================================

st.dataframe(
    metric_table,
    use_container_width=True,
    hide_index=True,
    column_config={

        "DCM Metric": st.column_config.TextColumn(
            width="large"
        ),
        "Count": st.column_config.NumberColumn(
            width="small"
        ),
        "Frequency": st.column_config.TextColumn(
            width="medium"
        ),
        "Z-Score": st.column_config.TextColumn(
            width="small"
        ),
        "Percentile": st.column_config.ProgressColumn(
            min_value=0,
            max_value=100,
            format="%d",
        ),
        "Direction": st.column_config.TextColumn(
            width="small"
        ),
    },
)


st.divider()


# =========================================================
# TEAM DCM BASELINE
# =========================================================

team_dcm_metrics = [
    {
        "Metric": "Middle Drive Frequency",
        "Numerator": "Middle Drives",
        "Denominator": "On-Ball Opportunities",
    },
    {
        "Metric": "Uncontested 3 Frequency",
        "Numerator": "Uncontested 3s",
        "Denominator": "On-Ball Opportunities",
    },
    {
        "Metric": "Paint Touches per Poss.",
        "Numerator": "Paint Touches",
        "Denominator": "Defensive Possessions",
    },
    {
        "Metric": "Foul Frequency",
        "Numerator": "Fouls",
        "Denominator": "Defensive Possessions",
    },
    {
        "Metric": "Deflections per Poss.",
        "Numerator": "Deflections",
        "Denominator": "Defensive Possessions",
    },
    {
        "Metric": "Charge Frequency",
        "Numerator": "Charges Taken",
        "Denominator": "Defensive Possessions",
    },
    {
        "Metric": "Loose Ball Frequency",
        "Numerator": "Loose Balls Recovered",
        "Denominator": "Defensive Possessions",
    },
    {
        "Metric": "Successful Boxout %",
        "Numerator": "Successful Boxouts",
        "Denominator": "Boxout Opportunities",
    },
    {
        "Metric": "O-Board Allowed Frequency",
        "Numerator": "O-Boards Allowed",
        "Denominator": "Boxout Opportunities",
    },
]


team_baseline = []

for metric in team_dcm_metrics:

    numerator = dcm_season[metric["Numerator"]].sum()
    denominator = dcm_season[metric["Denominator"]].sum()

    frequency = numerator / denominator if denominator > 0 else 0

    team_baseline.append({
        "DCM Metric": metric["Metric"],
        "Frequency": frequency,
    })

team_baseline_df = pd.DataFrame(team_baseline)

team_baseline_display = team_baseline_df.copy()

def format_frequency(row):
    if row["DCM Metric"] in  ["Paint Touches per Poss.","Deflection per Poss."]:
        return f'{row["Frequency"]:.2f}'
    else:
        return f'{row["Frequency"] * 100:.1f}%'

team_baseline_display["Frequency"] = team_baseline_display.apply(
    format_frequency,
    axis=1
)
st.subheader("Team DCM Baseline")

st.dataframe(
    team_baseline_display,
    hide_index=True,
    use_container_width=True,
)


st.divider()
# =========================================================
# TEAM DCM LEADERS
# =========================================================

leader_config = [
    ("Middle Drive Frequency", "lower"),
    ("UC3 Frequency", "lower"),
    ("Paint Touch Per Poss.", "lower"),
    ("Foul Frequency", "lower"),
    ("Deflection Per Poss.", "higher"),
    ("Charge Frequency", "higher"),
    ("Loose Ball Recovered Frequency", "higher"),
    ("Successful Boxout Frequency", "higher"),
    ("OBoard Allowed Frequency", "lower"),
]

denominator_map = {
    "Middle Drive Frequency": "On-Ball Opportunities",
    "UC3 Frequency": "On-Ball Opportunities",
    "Paint Touch Per Poss.": "Defensive Possessions",
    "Foul Frequency": "Defensive Possessions",
    "Deflection Per Poss.": "Defensive Possessions",
    "Charge Frequency": "Defensive Possessions",
    "Loose Ball Recovered Frequency": "Defensive Possessions",
    "Successful Boxout Frequency": "Boxout Opportunities",
    "OBoard Allowed Frequency": "Boxout Opportunities",
}


leaders = []

for metric, direction in leader_config:

    # -----------------------------------------------------
    # Only include players who have actual opportunities
    # -----------------------------------------------------

    denominator = denominator_map[metric]

    eligible = dcm_season[
        dcm_season[denominator] > 0
    ].copy()

    # Remove missing metric values
    eligible = eligible.dropna(subset=[metric])

    # -----------------------------------------------------
    # Rank players
    # -----------------------------------------------------

    eligible = eligible.sort_values(
        metric,
        ascending=(direction == "lower")
    )

    top_3 = eligible.head(3)

    # -----------------------------------------------------
    # Store the three leaders
    # -----------------------------------------------------

    for rank, (_, player) in enumerate(top_3.iterrows(), start=1):

        
        player_name = player["Player"]

        display_name = get_display_name(player_name)
        

        player_image = (
            PROJECT_ROOT
            / "yDashboard"
            / "assets"
            / f"{display_name}.webp"
        )

        leaders.append({
            "DCM Metric": metric,
            "Rank": rank,
            "Player": display_name,
            "Frequency": player[metric],
            "Image": player_image,
        })


leaders_df = pd.DataFrame(leaders)


def format_dcm_frequency(metric, value):

    if pd.isna(value):
        return "-"

    if metric in ["Paint Touch Per Poss.","Deflection Per Poss."]:
        return f"{value:.2f}"

    return f"{value * 100:.1f}%"

# =========================================================
# TEAM DCM LEADERS DISPLAY
# =========================================================

st.markdown("### Team DCM Leaders")

st.caption(
    "Top 3 players for each DCM process metric based on frequency."
)

for metric, direction in leader_config:

    metric_rows = (
        leaders_df[
            leaders_df["DCM Metric"] == metric
        ]
        .sort_values("Rank")
    )

    # -----------------------------------------------------
    # Metric title
    # -----------------------------------------------------

    st.markdown(
        f"""
        <div style="
            font-size:16px;
            font-weight:700;
            margin-top:18px;
            margin-bottom:8px;
        ">
            {metric}
        </div>
        """,
        unsafe_allow_html=True,
    )

    # -----------------------------------------------------
    # Three leaders
    # -----------------------------------------------------

    leader_cols = st.columns(3)

    for col, (_, leader) in zip(
        leader_cols,
        metric_rows.iterrows()
    ):

        with col:

            # Rank
            st.markdown(
                f"""
                <div style="
                    font-size:12px;
                    font-weight:600;
                    color:#666;
                    margin-bottom:4px;
                ">
                    {int(leader["Rank"])}{"ST" if leader["Rank"] == 1 else "ND" if leader["Rank"] == 2 else "RD"}
                </div>
                """,
                unsafe_allow_html=True,
            )

            # Headshot
            if leader["Image"].exists():
                st.image(
                    leader["Image"],
                    width=70,
                )

            # Player name
            st.markdown(
                f"""
                <div style="
                    font-size:15px;
                    font-weight:700;
                    margin-top:-4px;
                ">
                    {leader["Player"]}
                </div>
                """,
                unsafe_allow_html=True,
            )

            # Frequency
            st.markdown(
                f"""
                <div style="
                    font-size:13px;
                    color:#666;
                ">
                    {format_dcm_frequency(
                        metric,
                        leader["Frequency"]
                    )}
                </div>
                """,
                unsafe_allow_html=True,
            )



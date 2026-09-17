import pandas as pd


# ============================================================
# RAW MATRIX COLUMN MAPPING
# ============================================================

# Maps the raw DCM matrix columns to the standardized
# DCM V3 parser schema.
#
# Defensive Possessions are NOT mapped here.
# They are determined by the intersection of each player's
# row with that player's own column in the raw matrix.
#
# The parser stops at:
#     - defensive events
#     - defensive opportunities
#
# It does NOT calculate:
#     - frequencies
#     - per-possession values
#     - z-scores
#     - percentiles
#     - DCM scores


RAW_COLUMNS = {
    "On-Ball Opportunities": "On-Ball Opp",

    "Middle Drives": "Allow Middle",

    "Paint Touches": "Allow Paint Touch",

    "Uncontested 3s": "Allow Uncontested Three",

    "O-Boards Allowed": "Allow OBoard",

    "Loose Balls Recovered": "Loose Ball Recovered",

    "Fouls": "Foul",

    "Deflections": "Deflection",

    "Charges Taken": "Charge",

    "Successful Boxouts": "Successful Boxout",

    "Missed Boxouts": "Missed Box Out",
}


# ============================================================
# PARSER
# ============================================================

def parse_dcm_matrix(
    input_file,
    output_file
):
    """
    Convert a raw weekly DCM matrix into a clean weekly
    DCM player dataset.

    Defensive Possessions are determined by the diagonal
    of the player-by-player matrix:

        player's row × player's own column

    Example:
        #04 Allison Clarke → 26 Defensive Possessions
        #06 Shawnee Nordstrom → 62 Defensive Possessions

    The parser produces:
        - defensive possessions
        - on-ball opportunities
        - boxout opportunities
        - nine DCM event counts

    The parser does NOT calculate:
        - frequencies
        - per-possession values
        - z-scores
        - percentiles
        - DCM ratings

    Those calculations belong to later layers of the DCM
    pipeline.
    """

    # --------------------------------------------------------
    # READ RAW MATRIX
    # --------------------------------------------------------

    df = pd.read_csv(input_file)

    # The first column of the raw matrix contains player names.
    player_column = df.columns[0]

    df = df.rename(
        columns={
            player_column: "Player"
        }
    )

    # --------------------------------------------------------
    # PLAYER DATA
    # --------------------------------------------------------

    # Every row is now an individual player.
    # There is no longer a team summary row.
    players = df.copy()

    output = pd.DataFrame()

    output["Player"] = players["Player"]

    # --------------------------------------------------------
    # DEFENSIVE POSSESSIONS
    # --------------------------------------------------------
    #
    # Defensive Possessions are the intersection of:
    #
    #     player's row
    #              ×
    #     player's own column
    #
    # Example:
    #
    #     row = #04 Allison Clarke
    #     column = #04 Allison Clarke
    #     value = 26
    #
    # Therefore:
    #
    #     Allison Clarke → 26 defensive possessions
    #
    # --------------------------------------------------------

    def get_defensive_possessions(row):

        player = row["Player"]

        # Make sure the player's name is actually one of
        # the matrix columns.
        if player not in players.columns:
            return 0

        return pd.to_numeric(
            row[player],
            errors="coerce"
        )

    output["Defensive Possessions"] = (
        players.apply(
            get_defensive_possessions,
            axis=1
        )
        .fillna(0)
    )

    # --------------------------------------------------------
    # ON-BALL OPPORTUNITIES
    # --------------------------------------------------------

    output["On-Ball Opportunities"] = pd.to_numeric(
        players[RAW_COLUMNS["On-Ball Opportunities"]],
        errors="coerce"
    ).fillna(0)

    # --------------------------------------------------------
    # DCM EVENT COUNTS
    # --------------------------------------------------------

    output["Middle Drives"] = pd.to_numeric(
        players[RAW_COLUMNS["Middle Drives"]],
        errors="coerce"
    ).fillna(0)

    output["Paint Touches"] = pd.to_numeric(
        players[RAW_COLUMNS["Paint Touches"]],
        errors="coerce"
    ).fillna(0)

    output["Uncontested 3s"] = pd.to_numeric(
        players[RAW_COLUMNS["Uncontested 3s"]],
        errors="coerce"
    ).fillna(0)

    output["O-Boards Allowed"] = pd.to_numeric(
        players[RAW_COLUMNS["O-Boards Allowed"]],
        errors="coerce"
    ).fillna(0)

    output["Loose Balls Recovered"] = pd.to_numeric(
        players[RAW_COLUMNS["Loose Balls Recovered"]],
        errors="coerce"
    ).fillna(0)

    output["Fouls"] = pd.to_numeric(
        players[RAW_COLUMNS["Fouls"]],
        errors="coerce"
    ).fillna(0)

    output["Deflections"] = pd.to_numeric(
        players[RAW_COLUMNS["Deflections"]],
        errors="coerce"
    ).fillna(0)

    output["Charges Taken"] = pd.to_numeric(
        players[RAW_COLUMNS["Charges Taken"]],
        errors="coerce"
    ).fillna(0)

    output["Successful Boxouts"] = pd.to_numeric(
        players[RAW_COLUMNS["Successful Boxouts"]],
        errors="coerce"
    ).fillna(0)

    output["Missed Boxouts"] = pd.to_numeric(
        players[RAW_COLUMNS["Missed Boxouts"]],
        errors="coerce"
    ).fillna(0)

    # --------------------------------------------------------
    # BOXOUT OPPORTUNITIES
    # --------------------------------------------------------
    #
    # Boxout Opportunities are defined as:
    #
    #     Successful Boxouts + Missed Boxouts
    #
    # This is an opportunity count, not a frequency.
    # --------------------------------------------------------

    missed_boxouts = pd.to_numeric(
        players[RAW_COLUMNS["Missed Boxouts"]],
        errors="coerce"
    ).fillna(0)

    output["Boxout Opportunities"] = (
        output["Successful Boxouts"]
        + missed_boxouts
    )

    # --------------------------------------------------------
    # FINAL COLUMN ORDER
    # --------------------------------------------------------

    columns = [
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

    output = output[columns]

    # --------------------------------------------------------
    # CLEAN NUMERIC COLUMNS
    # --------------------------------------------------------

    numeric_columns = [
        column
        for column in output.columns
        if column != "Player"
    ]

    output[numeric_columns] = output[numeric_columns].apply(
        pd.to_numeric,
        errors="coerce"
    )

    # Counts/opportunities should be integers.
    output[numeric_columns] = (
        output[numeric_columns]
        .fillna(0)
        .astype(int)
    )

    # --------------------------------------------------------
    # SAVE
    # --------------------------------------------------------

    output.to_csv(
        output_file,
        index=False
    )

    print(
        f"DCM boxscore saved to {output_file}"
    )

    return output


# ============================================================
# RUN
# ============================================================

if __name__ == "__main__":

    # Change the week number in the function definition.

    dcm_boxscore = parse_dcm_matrix(
        input_file="/Users/rrodr102/Desktop/Python/DCM_V3/Data/dcm/raw/DCM_week02.csv",
        output_file="/Users/rrodr102/Desktop/Python/DCM_V3/Data/dcm/parsed/DCM_boxscore_week02.csv",
    )

    print(dcm_boxscore)
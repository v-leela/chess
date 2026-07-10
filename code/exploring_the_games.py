# import pandas as pd
# import matplotlib.pyplot as plt
# import numpy as np
import os
import glob

all_files = glob.glob(os.path.join("csv_by_month", "games_20*.csv"))
all_files = sorted(all_files)
print(all_files)

####################################
""" carlsen_games = []
for month_file in all_files:
    df_month = pd.read_csv(month_file)

    if "White" in df_month.columns and "Black" in df_month.columns:
        df_month["White"] = df_month["White"].fillna("")
        df_month["Black"] = df_month["Black"].fillna("")

        condition = df_month["White"].str.contains("Carlsen,M", case=False) | df_month[
            "Black"
        ].str.contains("Carlsen,M", case=False)
        carlsen_month = df_month[condition]
        if not carlsen_month.empty:
            carlsen_games.append(carlsen_month)

# print([len(each) for each in carlsen_games])

if carlsen_games:
    carlsen_df = pd.concat(carlsen_games, ignore_index=True)
    carlsen_df["Date"] = pd.to_datetime(
        carlsen_df["Date"], format="%Y.%m.%d", errors="coerce"
    )

    # Sort by date and reassign (sort_values doesn't sort in-place by default)
    carlsen_df = carlsen_df.sort_values(by="Date").reset_index(drop=True)

    # Optional: convert back to string format for cleaner CSV output
    # carlsen_df["Date"] = carlsen_df["Date"].dt.strftime("%Y.%m.%d")

    carlsen_df.to_csv("magnus_carlsen_games.csv", index=False) """

############################

""" def get_player_elo(games, pre, player):
    is_white = games["White"].str.contains(player, case=False, na=False)
    is_black = games["Black"].str.contains(player, case=False, na=False)

    white_rows = games.loc[is_white, ["WhiteElo"]].rename(columns={"WhiteElo": "Elo"})
    black_rows = games.loc[is_black, ["BlackElo"]].rename(columns={"BlackElo": "Elo"})

    player_elo_df = pd.concat([white_rows, black_rows], ignore_index=True).dropna()
    player_elo = player_elo_df["Elo"].unique()

    if player_elo.size:
        return np.mean(player_elo)
    else:
        return pre


def elo_plot(players):
    for player in players:
        pre = 0
        elos = []
        for file in all_files:
            game = pd.read_csv(file)
            pre = get_player_elo(game, pre, player)
            elos.append(pre)
        player_elo_df = pd.DataFrame(elos, columns=["Elo"])

        plt.plot(player_elo_df, label=player)
    plt.legend()
    plt.xlabel("Timeline")
    plt.ylabel("Elo Rating")
    plt.title("Players Elo Rating Progression")
    plt.show()


elo_plot(["Carlsen,M", "Nakamura,Hi", "Anand,V", "Praggnanandhaa", "gukesh"]) """

#####################################

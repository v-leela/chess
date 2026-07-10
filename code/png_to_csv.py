"""import chess.pgn
import pandas as pd

# Path to your PGN file
pgn_path = "/Users/vallurileelasaikrishna/Documents/chess/data/twic.pgn"

games = []
rows = 0

# Use a single 'with' block to safely open and read the file
with open(pgn_path, encoding="latin-1") as pgn_file:
    while True:
        game = chess.pgn.read_game(pgn_file)

        # Break the loop if we reach the end of the file
        if game is None:
            break

        # 1. Grab ALL headers automatically as a dictionary
        game_data = dict(game.headers)

        # 2. Grab the actual moves (mainline notation) and add it to the data
        game_data["Moves"] = str(game.mainline_moves())

        # Append the game's data to our list
        games.append(game_data)
        rows += 1
        print(rows)

# Convert the list of dictionaries to a pandas DataFrame
df = pd.DataFrame(games)

# Shift the index to start from 1 instead of 0
df.index = df.index + 1

# Label the index column so it looks clean in your CSV viewer
#df.index.name = "Game_Number"

# Save to CSV with the 1-based index included
df.to_csv("games.csv", index=True)

# Quick peek at the data structure
print(f"Successfully processed {len(df)} games.")
print(df.head())

"""

import chess.pgn
import pandas as pd
import os

pgn_folder = "/Users/vallurileelasaikrishna/Documents/chess/data/"
output_folder = "/Users/vallurileelasaikrishna/Documents/chess/data/raw_data"

os.makedirs(output_folder, exist_ok=True)

headers_written = {}
totals = {}
batches = {}

for filename in sorted(os.listdir(pgn_folder)):
    if not filename.endswith(".pgn"):
        continue

    print(f"Processing {filename}...")

    with open(os.path.join(pgn_folder, filename), encoding="latin-1") as pgn_file:
        while True:
            game = chess.pgn.read_game(pgn_file)
            if game is None:
                break

            h = game.headers
            date = h.get("Date", "????.??.??")
            parts = date.split(".")

            # Extract year and month
            year = parts[0] if len(parts) > 0 and parts[0].isdigit() else "Unknown"
            month = parts[1] if len(parts) > 1 and parts[1].isdigit() else "Unknown"

            key = f"{year}_{month}"  # e.g. "2020_05"

            if key not in batches:
                batches[key] = []
                totals[key] = 0

            batches[key].append(
                {
                    "Event": h.get("Event"),
                    "Site": h.get("Site"),
                    "Date": h.get("Date"),
                    "White": h.get("White"),
                    "Black": h.get("Black"),
                    "Result": h.get("Result"),
                    "WhiteElo": h.get("WhiteElo"),
                    "BlackElo": h.get("BlackElo"),
                    "ECO": h.get("ECO"),
                    "Opening": h.get("Opening"),
                    "Moves": str(game.mainline_moves()),
                }
            )

            if len(batches[key]) >= 1000:
                csv_path = os.path.join(output_folder, f"games_{key}.csv")
                df = pd.DataFrame(batches[key])
                df.to_csv(
                    csv_path, mode="a", header=key not in headers_written, index=False
                )
                headers_written[key] = True
                totals[key] += len(batches[key])
                batches[key] = []

# Flush remaining
for key, batch in batches.items():
    if batch:
        csv_path = os.path.join(output_folder, f"games_{key}.csv")
        df = pd.DataFrame(batch)
        df.to_csv(csv_path, mode="a", header=key not in headers_written, index=False)
        totals[key] = totals.get(key, 0) + len(batch)

print("\nDone! Games per month:")
for key in sorted(totals):
    print(f"  {key}: {totals[key]} games")

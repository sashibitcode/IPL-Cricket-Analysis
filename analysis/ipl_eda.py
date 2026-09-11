from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns

BASE_DIR = Path(__file__).resolve().parents[1]
DATA_DIR = BASE_DIR / "data"
OUTPUT_DIR = BASE_DIR / "outputs"
PLOTS_DIR = OUTPUT_DIR / "plots"
PLOTS_DIR.mkdir(parents=True, exist_ok=True)


def clean_matches(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()
    for col in df.columns:
        if df[col].dtype == object:
            df[col] = df[col].astype(str).str.strip()
            df[col] = df[col].replace({"nan": np.nan, "NaN": np.nan, "NA": np.nan})

    df["date"] = pd.to_datetime(df["date"], errors="coerce")
    df["result_margin"] = pd.to_numeric(df["result_margin"], errors="coerce")
    df["target_runs"] = pd.to_numeric(df["target_runs"], errors="coerce")
    df["target_overs"] = pd.to_numeric(df["target_overs"], errors="coerce")
    return df


def clean_deliveries(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()
    for col in df.columns:
        if df[col].dtype == object:
            df[col] = df[col].astype(str).str.strip()
            df[col] = df[col].replace({"nan": np.nan, "NaN": np.nan, "NA": np.nan})

    numeric_cols = [
        "match_id",
        "inning",
        "over",
        "ball",
        "batsman_runs",
        "extra_runs",
        "total_runs",
        "is_wicket",
    ]
    for col in numeric_cols:
        df[col] = pd.to_numeric(df[col], errors="coerce")

    df["is_wicket"] = df["is_wicket"].fillna(0).astype(int)
    return df


def plot_team_wins(matches: pd.DataFrame) -> None:
    team_wins = matches["winner"].value_counts().reset_index()
    team_wins.columns = ["team", "wins"]
    team_wins = team_wins.sort_values("wins", ascending=False)

    plt.figure(figsize=(12, 6))
    sns.barplot(data=team_wins, x="wins", y="team", palette="viridis")
    plt.title("IPL team wins")
    plt.xlabel("Matches won")
    plt.ylabel("Team")
    plt.tight_layout()
    plt.savefig(PLOTS_DIR / "team_wins.png", dpi=300)
    plt.close()


def plot_season_trend(matches: pd.DataFrame) -> None:
    season_summary = (
        matches.groupby("season")
        .agg(matches_played=("id", "count"), total_winners=("winner", "nunique"))
        .reset_index()
    )

    plt.figure(figsize=(12, 6))
    sns.lineplot(data=season_summary, x="season", y="matches_played", marker="o", color="royalblue")
    plt.title("IPL match count by season")
    plt.xlabel("Season")
    plt.ylabel("Matches")
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.savefig(PLOTS_DIR / "season_match_count.png", dpi=300)
    plt.close()


def plot_toss_impact(matches: pd.DataFrame) -> None:
    toss_impact = matches.assign(toss_win_matches=(matches["toss_winner"] == matches["winner"]))
    toss_summary = (
        toss_impact.groupby("toss_decision")
        .agg(matches=("id", "count"), toss_winner_then_winner=("toss_win_matches", "sum"))
        .reset_index()
    )

    plt.figure(figsize=(10, 6))
    sns.barplot(data=toss_summary, x="toss_decision", y="toss_winner_then_winner", palette="Set2")
    plt.title("Toss decision vs match win")
    plt.xlabel("Toss decision")
    plt.ylabel("Matches won after winning toss")
    plt.tight_layout()
    plt.savefig(PLOTS_DIR / "toss_impact.png", dpi=300)
    plt.close()


def plot_top_players_of_match(matches: pd.DataFrame) -> None:
    player_counts = matches["player_of_match"].value_counts().head(10).reset_index()
    player_counts.columns = ["player", "awards"]

    plt.figure(figsize=(12, 7))
    sns.barplot(data=player_counts, x="awards", y="player", palette="magma")
    plt.title("Top player-of-the-match award winners")
    plt.xlabel("Awards")
    plt.ylabel("Player")
    plt.tight_layout()
    plt.savefig(PLOTS_DIR / "top_players_of_match.png", dpi=300)
    plt.close()


def plot_result_distribution(matches: pd.DataFrame) -> None:
    result_counts = matches["result"].value_counts().reset_index()
    result_counts.columns = ["result", "count"]

    plt.figure(figsize=(8, 6))
    sns.barplot(data=result_counts, x="result", y="count", palette="pastel")
    plt.title("Match result distribution")
    plt.xlabel("Result")
    plt.ylabel("Count")
    plt.tight_layout()
    plt.savefig(PLOTS_DIR / "result_distribution.png", dpi=300)
    plt.close()


def create_summary_files(matches: pd.DataFrame, deliveries: pd.DataFrame) -> None:
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    matches.to_csv(DATA_DIR / "matches_clean.csv", index=False)
    deliveries.to_csv(DATA_DIR / "deliveries_clean.csv", index=False)

    summary = {
        "total_matches": int(matches.shape[0]),
        "total_deliveries": int(deliveries.shape[0]),
        "seasons": sorted(matches["season"].dropna().unique().tolist()),
        "teams": sorted(set(matches["team1"].dropna().tolist()) | set(matches["team2"].dropna().tolist())),
        "most_successful_team": matches["winner"].value_counts().idxmax(),
        "top_player_of_match": matches["player_of_match"].value_counts().idxmax(),
    }

    pd.DataFrame([summary]).to_csv(OUTPUT_DIR / "ipl_summary.csv", index=False)


def main() -> None:
    matches = clean_matches(pd.read_csv(DATA_DIR / "matches.csv"))
    deliveries = clean_deliveries(pd.read_csv(DATA_DIR / "deliveries.csv"))

    create_summary_files(matches, deliveries)
    plot_team_wins(matches)
    plot_season_trend(matches)
    plot_toss_impact(matches)
    plot_top_players_of_match(matches)
    plot_result_distribution(matches)

    print("Matches shape:", matches.shape)
    print("Deliveries shape:", deliveries.shape)
    print("Missing values in matches:", matches.isna().sum().sum())
    print("Missing values in deliveries:", deliveries.isna().sum().sum())
    print("Most successful team:", matches["winner"].value_counts().idxmax())
    print("Top player of match:", matches["player_of_match"].value_counts().idxmax())
    print("Outputs saved in:", OUTPUT_DIR)


if __name__ == "__main__":
    sns.set_style("whitegrid")
    main()

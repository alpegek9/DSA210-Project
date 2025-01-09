#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jan  5 18:46:53 2025

@author: alp
"""

import pandas as pd
import matplotlib.pyplot as plt


def parse_chess_data(file_path):
    games = []
    current_game = {}

    with open(file_path, 'r', encoding='utf-8') as file:
        for line in file:
            line = line.strip()

            if not line:
                if len(current_game) >= 5:
                    games.append({
                        'Date': current_game.get('Date', ''),
                        'White': current_game.get('White', ''),
                        'Black': current_game.get('Black', ''),
                        'Result': current_game.get('Result', ''),
                        'Termination': current_game.get('Termination', ''),
                    })
                current_game = {}
                continue

            if line.startswith('[Date "'):
                current_game['Date'] = line.split('"')[1]
            elif line.startswith('[White "'):
                current_game['White'] = line.split('"')[1]
            elif line.startswith('[Black "'):
                current_game['Black'] = line.split('"')[1]
            elif line.startswith('[Result "'):
                current_game['Result'] = line.split('"')[1]
            elif line.startswith('[Termination "'):
                current_game['Termination'] = line.split('"')[1]

        if len(current_game) >= 5:
            games.append({
                'Date': current_game.get('Date', ''),
                'White': current_game.get('White', ''),
                'Black': current_game.get('Black', ''),
                'Result': current_game.get('Result', ''),
                'Termination': current_game.get('Termination', ''),
            })

    return games


def prepare_dataframe(games, player_name):
    df = pd.DataFrame(games)
    df["Date"] = pd.to_datetime(df["Date"], errors="coerce")

 
    df["White"] = df["White"].apply(lambda x: x if x == player_name else "****")
    df["Black"] = df["Black"].apply(lambda x: x if x == player_name else "****")


    df["PlayerColor"] = df.apply(
        lambda row: "White" if row["White"] == player_name else "Black", axis=1
    )

    
    def get_outcome(row):
        if (row["Result"] == "1-0" and row["White"] == player_name) or \
           (row["Result"] == "0-1" and row["Black"] == player_name):
            return "Win"
        elif (row["Result"] == "0-1" and row["White"] == player_name) or \
             (row["Result"] == "1-0" and row["Black"] == player_name):
            return "Loss"
        else:
            return "Draw"

    df["Outcome"] = df.apply(get_outcome, axis=1)

    return df


def analyze_and_print_stats(df):
    total_games = len(df)
    wins = len(df[df["Outcome"] == "Win"])
    losses = len(df[df["Outcome"] == "Loss"])
    win_rate = (wins / total_games * 100) if total_games > 0 else 0
    lose_rate = (losses / total_games * 100) if total_games > 0 else 0

    white_games = df[df["PlayerColor"] == "White"]
    white_wins = len(white_games[white_games["Outcome"] == "Win"])
    white_losses = len(white_games[white_games["Outcome"] == "Loss"])
    white_win_rate = (white_wins / len(white_games) * 100) if len(white_games) > 0 else 0
    white_lose_rate = (white_losses / len(white_games) * 100) if len(white_games) > 0 else 0

    print(f"Win rate: {win_rate:.2f}%")
    print(f"Lose rate: {lose_rate:.2f}%")
    print(f"White win rate: {white_win_rate:.2f}%")
    print(f"White lose rate: {white_lose_rate:.2f}%")


def plot_monthly_rates(df):
    df["Month"] = df["Date"].dt.to_period("M")
    
  
    monthly_outcomes = df.groupby("Month")["Outcome"].value_counts().unstack(fill_value=0)
    monthly_outcomes = monthly_outcomes.divide(monthly_outcomes.sum(axis=1), axis=0) * 100

    monthly_outcomes.plot(kind="line", marker="o", title="Monthly Win, Lose, Draw Rates (%)")
    plt.xlabel("Month")
    plt.ylabel("Percentage (%)")
    plt.legend(title="Outcome")
    plt.grid()
    plt.show()


def plot_monthly_white_rates(df):
    df_white = df[df["PlayerColor"] == "White"].copy()
    df_white["Month"] = df_white["Date"].dt.to_period("M")

    white_outcomes = df_white.groupby("Month")["Outcome"].value_counts().unstack(fill_value=0)
    white_outcomes = white_outcomes.divide(white_outcomes.sum(axis=1), axis=0) * 100

    white_outcomes.plot(kind="line", marker="o", title="Monthly White Win, Lose, Draw Rates (%)")
    plt.xlabel("Month")
    plt.ylabel("Percentage (%)")
    plt.legend(title="Outcome")
    plt.grid()
    plt.show()


file_path = "DSA210Merged.txt" 
player_name = "alpegek9"        
games = parse_chess_data(file_path)
df = prepare_dataframe(games, player_name)
analyze_and_print_stats(df)
plot_monthly_rates(df)
plot_monthly_white_rates(df)

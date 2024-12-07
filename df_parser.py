import re

import numpy as np
import pandas as pd


def parse_from_file(file_path: str):
    """
    Parses a .phh file to extract hand data and initializes a Hand object.
    """
    with open(file_path, "r") as file:
        lines = file.readlines()

    # Extract data line by line
    actions = re.findall(r"'([^']+)'", lines[6])
    hand = int(re.search(r"hand\s*=\s*(\d+)", lines[7]).group(1))
    players = re.findall(r"'([^']+)'", lines[8])
    profits = list(map(int, re.findall(r"\d+", lines[9])))
    for i, profit in enumerate(profits):
        profits[i] = profit - 10000

    pot = 0
    current_bet = 150

    for action in actions:
        parts = action.split()

        # Skip invalid actions
        if len(parts) < 2:
            continue

        # Parse the action
        player = parts[0]  # e.g., p3, p2, d
        action_type = parts[1]  # e.g., cbr, cc, db, f, sm

        # Handle betting actions
        if action_type == "cbr":  # Raise or bet
            bet_amount = int(parts[2])
            pot += bet_amount  # Add the bet to the pot
            current_bet = bet_amount  # Update the current bet size
        elif action_type == "cc":  # Call
            pot += current_bet
        elif action_type == "db":  # Deal board
            current_bet = 0
            continue
        elif action_type == "dh":  # Deal hand
            continue
        elif action_type == "f":
            continue
        elif action_type == "sm":
            continue

    hole_cards = {f"p{i+1}": None for i in range(6)}

    # Hole cards
    for action in actions[:6]:
        parts = action.split()
        player = parts[2]
        cards = parts[3]
        hole_cards[player] = cards

    preflop = {f"p{i+1}": [] for i in range(6)}
    flop = {f"p{i+1}": [] for i in range(6)}
    turn = {f"p{i+1}": [] for i in range(6)}
    river = {f"p{i+1}": [] for i in range(6)}
    flop_cards = ""
    turn_cards = ""
    river_cards = ""
    next_street = False
    index = 0
    for action in actions[6:]:
        if action.startswith("d db"):
            next_street = True
            flop_cards = action.split()[2]
            index += 1
            break
        elif action.startswith("p"):
            player = action.split()[0]
            choice = action.split()[1:]
            moves = " ".join(choice)
            preflop[player].append(moves)
        index += 1

    # ['p3 cbr 200', 'p4 f', 'p5 f', 'p6 f', 'p1 f', 'p2 cc', 'd db 2s8h2c', 'p2 cc', 'p3 cbr 150', 'p2 cc', 'd db Qc', 'p2 cc', 'p3 cc', 'd db 4d', 'p2 cc', 'p3 cc', 'p2 sm AhTs', 'p3 sm AcJh']

    if next_street:
        next_street = False
        for action in actions[6 + index :]:
            if action.startswith("d db"):
                next_street = True
                turn_cards = action.split()[2]
                index += 1
                break
            elif action.startswith("p"):
                player = action.split()[0]
                choice = action.split()[1:]
                moves = " ".join(choice)
                flop[player].append(moves)
            index += 1

    if next_street:
        next_street = False
        for action in actions[6 + index :]:
            if action.startswith("d db"):
                next_street = True
                river_cards = action.split()[2]
                index += 1
                break
            elif action.startswith("p"):
                player = action.split()[0]
                choice = action.split()[1:]
                moves = " ".join(choice)
                turn[player].append(moves)
            index += 1

    if next_street:
        for action in actions[6 + index :]:
            player = action.split()[0]
            choice = action.split()[1:]
            moves = " ".join(choice)
            river[player].append(moves)
            index += 1
    df_data = {
        "Player": players,
        "Hole Cards": [hole_cards[f"p{i+1}"] for i in range(6)],
        "Preflop": [", ".join(preflop[f"p{i+1}"]) for i in range(6)],
        flop_cards: [", ".join(flop[f"p{i+1}"]) for i in range(6)],
        turn_cards: [", ".join(turn[f"p{i+1}"]) for i in range(6)],
        river_cards: [", ".join(river[f"p{i+1}"]) for i in range(6)],
        "Pot Size": pot,
        "Profits": profits,
    }

    df = pd.DataFrame(df_data)

    return df

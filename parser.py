import os
import re
from dataclasses import dataclass, field
from typing import List

# 1. Model classify whether a given hand is a bluff or not
# 2. Analyze Pluribus's bluff success rate
# 3. If it is a good success rate, we learn and try and implement on our own, model distillation
# 4. Model distillation gives us a simpler model

# Analyze by streets
# River: easy to determine whether or not they are bluffing

# Consider the river


@dataclass
class Hand:
    actions: List[str]
    hand: int
    players: List[str]
    profits: List[int]

    @staticmethod
    def parse_from_file(file_path: str) -> "Hand":
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

        return Hand(actions=actions, hand=hand, players=players, profits=profits)


# Example usage
# Assuming the .phh file content shown in the image is saved as 'hand_data.phh'
# file_path = 'hand_data.phh'
# hand = Hand.parse_from_file(file_path)
# print(hand)

if __name__ == "__main__":
    # Path to the .phh file
    file_path = "0.phh"

    # Parse the file and create a Hand object
    try:
        hand = Hand.parse_from_file(file_path)
        print(hand)
    except Exception as e:
        print(f"Error occurred: {e}")

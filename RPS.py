import random
import numpy as np
import matplotlib.pyplot as plt
from enum import Enum

class Action(Enum):
    ROCK = 0
    PAPER = 1
    SCISSORS = 2

def get_payoff(action_1: Action, action_2: Action) -> int:
    mod3_val = (action_1.value - action_2.value) % 3
    if mod3_val == 2:
        return -1
    else:
        return mod3_val

def get_strategy(cumulative_regrets: np.ndarray) -> np.ndarray:
    pos = np.maximum(0, cumulative_regrets)
    total = pos.sum()
    if total > 0:
        return pos / total
    else:
        return np.full(shape=len(Action), fill_value=1/len(Action))

def get_regrets(payoff: int, opp_action: Action) -> np.ndarray:
    """Return regrets for each possible action."""
    return np.array([
        get_payoff(a, opp_action) - payoff
        for a in Action
    ])

# Parameters
num_iterations = 10000
opp_strategy = [0.2, 0.2, 0.6]

cumulative_regrets = np.zeros(len(Action), dtype=int)
strategy_sum = np.zeros(len(Action), dtype=float)

rock_probs = []
paper_probs = []
scissors_probs = []

for i in range(num_iterations):
    strategy = get_strategy(cumulative_regrets)
    strategy_sum += strategy
    avg_strategy = strategy_sum / (i + 1)
    
    rock_probs.append(avg_strategy[Action.ROCK.value])
    paper_probs.append(avg_strategy[Action.PAPER.value])
    scissors_probs.append(avg_strategy[Action.SCISSORS.value])
    
    our_action = random.choices(list(Action), weights=strategy)[0]
    opp_action = random.choices(list(Action), weights=strategy)[0]
    
    our_payoff = get_payoff(our_action, opp_action)
    regrets = get_regrets(our_payoff, opp_action)
    
    cumulative_regrets += regrets

plt.plot(rock_probs, label="Rock")
plt.plot(paper_probs, label="Paper")
plt.plot(scissors_probs, label="Scissors")

plt.xlabel("Iteration")
plt.ylabel("Probability")
plt.title("Regret vs Regret")
plt.legend()
plt.show()


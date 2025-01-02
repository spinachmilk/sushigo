from agent import Agent
from state import SushiGoState
import random

class RandomAgent(Agent):
    """
    An agent that selects actions randomly from the available cards.
    """

    def __init__(self):
        pass

    def select_action(self, state: SushiGoState):
        """
        Select a random card from the player's hand.

        Args:
            state: The current game state.
        
        Returns:
            A list with one randomly selected card.
        """
        return [random.choice(state.cur_hand)]

from abc import ABC, abstractmethod
from state import SushiGoState
from typing import List


class Agent(ABC):
    """
    Abstract base class for agents in the Sushi Go game.
    Each agent should implement the select_action method to decide their move.
    """

    @abstractmethod
    def select_action(self, state: SushiGoState) -> List[int]:
        """
        Given a state, selects the best action for the agent.

        Args:
            state: The current game state.
        
        Returns:
            List of card(s) to be played.
        """
        pass

from agent import Agent
from heuristic_agent import HeuristicAgent
from state import SushiGoState
from typing import Union, Dict, Tuple


class ExpectimaxAgent(Agent):
    """
    An agent that uses the Expectimax algorithm to make decisions, optionally playing against another agent.
    """

    def __init__(self, opponent: Union[Agent, None] = None, max_depth: int = 3):
        """
        Initialize the agent with the option to play against another agent.

        Args:
            opponent: Another agent to play against, or None for a random opponent.
        """
        self.opponent = opponent
        self.max_depth = max_depth
        self.dp: Dict[int, Tuple[int, int]] = {}
        self.heuristic = HeuristicAgent()

    def select_action(self, state: SushiGoState):
        """
        Select an action based on the current state.

        Args:
            state: The current game state.
        
        Returns:
            A list containing the selected card.
        """
        _, action = (
            self.search_against_random(state)
            if self.opponent is None
            else self.search_against_opponent(state)
        )
        return [action]

    def search_against_opponent(self, state: SushiGoState, depth=0) -> Tuple[int, int]:
        """
        Recursively searches for the best action against an opponent using Expectimax.

        Args:
            state: The current game state.
            depth: The current depth of the search.

        Returns:
            A tuple with the best score and the chosen action.
        """
        key = hash(state)
        if key in self.dp:
            return self.dp[key]

        if state.is_terminal():
            p1_score, p2_score = state.calculate_scores()
            self.dp[key] = p1_score - p2_score, -1
            return p1_score - p2_score, -1

        opp_state = state.deep_flip()
        opp_card = self.opponent.select_action(opp_state)[0]
        opp_state.cur_collection.append(opp_card)
        opp_state.cur_hand.remove(opp_card)

        if depth >= self.max_depth:
            card = self.heuristic.select_action(state)[0]
            next_state = opp_state.deep_flip()
            next_state.cur_collection.append(card)
            next_state.cur_hand.remove(card)
            next_state.swap_hands()
            score, _ = self.search_against_opponent(next_state, depth + 1)
            return score, card

        best_score = float("-infinity")
        best_card = -1

        for card in state.cur_hand:
            next_state = opp_state.deep_flip()
            next_state.cur_collection.append(card)
            next_state.cur_hand.remove(card)
            next_state.swap_hands()
            score, _ = self.search_against_opponent(next_state, depth + 1)
            if score > best_score:
                best_score = score
                best_card = card

        self.dp[key] = best_score, best_card
        return best_score, best_card

    def search_against_random(self, state: SushiGoState, depth=0):
        """
        Recursively searches for the best action against a random opponent using Expectimax.

        Args:
            state: The current game state.
            depth: The current depth of the search.

        Returns:
            A tuple with the best score and the chosen action.
        """
        key = hash(state)
        if key in self.dp:
            return self.dp[key]

        if state.is_terminal():
            p1_score, p2_score = state.calculate_scores()
            score = 1 if p1_score > p2_score else -1 if p1_score < p2_score else 0
            return score, None

        if depth >= self.max_depth:
            card = self.heuristic.select_action(state)[0]
            opp_card = self.heuristic.select_action(state.flip())[0]
            state.cur_collection.append(card)
            state.cur_hand.remove(card)
            state.opp_collection.append(opp_card)
            state.opp_hand.remove(opp_card)
            state.swap_hands()
            score, _ = self.search_against_random(state, depth + 1)
            return score, card

        n = len(state.cur_hand)
        best_score = float("-infinity")
        best_card = -1

        for card in state.cur_hand:
            avg_score = 0
            for opp_card in state.opp_hand:
                next_state = state.deep_copy()
                next_state.cur_collection.append(card)
                next_state.cur_hand.remove(card)
                next_state.opp_collection.append(opp_card)
                next_state.opp_hand.remove(opp_card)
                next_state.swap_hands()

                score, _ = self.search_against_random(next_state, depth + 1)
                avg_score += score

            avg_score /= n
            if avg_score > best_score:
                best_score = avg_score
                best_card = card

        self.dp[key] = best_score, best_card
        return best_score, best_card

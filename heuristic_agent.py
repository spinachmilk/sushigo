from agent import Agent
from state import SushiGoState, card_names
from typing import List
import random

class HeuristicAgent(Agent):
    """
    An agent that uses a heuristic approach to select actions based on card values.
    """

    def __init__(self):
        pass

    def get_cnts(self, sushi_go_list: List[int]):
        """
        Returns the count of various types of cards in the given list.

        Args:
            sushi_go_list: List of cards in the player's hand or collection.
        
        Returns:
            A tuple with counts of different card types.
        """
        counts = [0] * 6  # Initialize counts for each card type (Tempura, Sashimi, etc.)
        for card in sushi_go_list:
            if card == 0:  # Tempura
                counts[0] += 1
            elif card == 1:  # Sashimi
                counts[1] += 1
            elif card == 2:  # Dumpling
                counts[2] += 1
            elif card in [3, 4, 5]:  # Maki rolls
                counts[3] += card - 2
            elif card in [6, 7, 8]:  # Nigiri
                counts[4] += 1
            elif card == 9:  # Wasabi
                counts[5] += 1
        return counts

    def select_action(self, state: SushiGoState):
        """
        Select the best card to play based on the current state and heuristic evaluation.

        Args:
            state: The current game state.
        
        Returns:
            The selected card(s) to play.
        """
        card_values = [0] * len(card_names)  # Initialize card values for each card type
        cur_hand_cnts = self.get_cnts(state.cur_hand)
        opp_hand_cnts = self.get_cnts(state.opp_hand)
        cur_collection_cnts = self.get_cnts(state.cur_collection)
        opp_collection_cnts = self.get_cnts(state.opp_collection)

        # Evaluate the expected value (EV) for different cards in the game
        has_wasabi = cur_collection_cnts[0] < cur_collection_cnts[1]  # Check if the player has Wasabi

        # Calculate expected value for Nigiri cards
        if has_wasabi:
            card_values[6] += 6
            card_values[7] += 9
            card_values[8] += 3
        else:
            card_values[6] += 2
            card_values[7] += 3
            card_values[8] += 1

        # Evaluate expected value for Tempura
        if len(state.cur_collection) > 1:
            if cur_collection_cnts[2] % 2 == 1:
                card_values[0] += 5
            elif opp_collection_cnts[2] % 2 == 1 and (
                opp_hand_cnts[2] == 0 and cur_hand_cnts[2] == 1
            ):
                card_values[0] += 5
            elif (len(state.cur_collection) < 4) and (cur_hand_cnts[2] + opp_hand_cnts[2] > 1):
                card_values[0] += 2.5 / (
                    4 - min(3, cur_hand_cnts[2] + opp_hand_cnts[2])
                )
            else:
                card_values[0] += 0.1

        # Evaluate expected value for Sashimi (only check for blocking)
        if len(state.cur_collection) > 1:
            if opp_collection_cnts[5] % 3 == 2 and (
                opp_hand_cnts[5] == 0 and cur_hand_cnts[5] == 1
            ):
                card_values[1] += 10

        # Evaluate expected value for Wasabi (if not already used)
        if not has_wasabi:
            if len(state.cur_collection) < 5:
                if opp_hand_cnts[0] > 1:
                    card_values[9] += 2.5

        # Evaluate expected value for Dumplings
        card_values[2] += 1 + cur_collection_cnts[4]
        if len(state.cur_collection) > 1:
            if len(state.cur_collection) < 4:
                card_values[2] += (cur_hand_cnts[4] + opp_hand_cnts[4]) * 0.1

        # Evaluate expected value for Maki rolls
        if len(state.cur_collection) > 1:
            total_maki_left = cur_hand_cnts[3] + opp_hand_cnts[3]
            if cur_collection_cnts[3] <= opp_collection_cnts[3] + total_maki_left:
                if (
                    cur_collection_cnts[3] + 1
                    > opp_collection_cnts[3] + total_maki_left - 1
                ):
                    card_values[3] += 3
                    card_values[4] += 3
                    card_values[5] += 3
                elif (
                    cur_collection_cnts[3] + 2
                    > opp_collection_cnts[3] + total_maki_left - 2
                ):
                    card_values[4] += 3
                    card_values[5] += 3
                elif (
                    cur_collection_cnts[3] + 3
                    > opp_collection_cnts[3] + total_maki_left - 3
                ):
                    card_values[5] += 3
                elif cur_collection_cnts[3] + 1 > opp_collection_cnts[3]:
                    card_values[3] += 0.15
                    card_values[4] += 0.6
                    card_values[5] += 1.35
                elif cur_collection_cnts[3] + 2 > opp_collection_cnts[3]:
                    card_values[4] += 0.15
                    card_values[5] += 0.6
                elif cur_collection_cnts[3] + 3 > opp_collection_cnts[3]:
                    card_values[5] += 0.15
        else:
            card_values[3] += 0.15
            card_values[4] += 0.6
            card_values[5] += 1.35

        # Sort the cards by their expected value (highest to lowest)
        sorted_card_values = sorted(
            enumerate(card_values), key=lambda x: x[1], reverse=True
        )
        
        # Select the card with the highest expected value that is available in hand
        for card, _ in sorted_card_values:
            if state.cur_hand.count(card) > 0:
                return [card]

        # If no cards are found, pick a random card from the hand
        return [random.choice(state.cur_hand)]

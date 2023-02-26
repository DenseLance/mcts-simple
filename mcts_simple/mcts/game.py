from typing import Any, List

class Game:
    def __init__(self):
        raise NotImplementedError

    def render(self) -> None:
        """
        RETURNS:
            Visual representation of the current state of the game which is to be output as text or other means
        """
        raise NotImplementedError

    def get_state(self) -> Any:
        """
        RETURNS:
            Current state of the game
        """
        raise NotImplementedError

    def number_of_players(self) -> int:
        """
        RETURNS:
            Number of players
        """
        raise NotImplementedError

    def current_player(self) -> int:
        """
        Note that players are labelled from 0 to number of players - 1

        RETURNS:
            Player that is taking an action this turn
        """
        raise NotImplementedError
    
    def possible_actions(self) -> List[int]:
        """
        RETURNS:
            Possible actions that can be taken by current player this turn
        """
        raise NotImplementedError

    def take_action(self, action: int) -> None:
        """
        Note that next player should be chosen even after end of game
        """
        raise NotImplementedError

    def has_outcome(self) -> bool:
        """
        RETURNS:
            True if game has ended
            OR
            False if game is still ongoing
        """
        raise NotImplementedError

    def winner(self) -> List[int]:
        """
        RETURNS:
            Empty list if all players lose
            OR
            List of players if game ends in a draw
            OR
            List of winners if at least 1 player wins
        """
        raise NotImplementedError

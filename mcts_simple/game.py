class Game:
    def __init__(self):
        raise NotImplementedError

    def render(self):
        """
        RETURNS:
            visual representation of the current state of the game
        """
        raise NotImplementedError

    def get_state(self):
        """
        Note:
        1. Provide a hashable state.
        2. Ensure that the state provided during the game does not coincide with the state provided
           at the start of the game.
        3. Best to include the player who is taking their action this turn within the state.
                
        RETURNS:
            current state of the game
        """
        raise NotImplementedError

    def number_of_players(self):
        """
        RETURNS:
            number of players
        """
        raise NotImplementedError

    def current_player(self):
        """
        RETURNS:
            player that is taking an action this turn
        """
        raise NotImplementedError

    def possible_actions(self):
        """
        RETURNS:
            actions that can be taken this turn
        """
        raise NotImplementedError

    def take_action(self, action):
        """
        action should be string type to support the play_with_human() method from MCTS
        """
        raise NotImplementedError
        if action not in self.possible_actions():
            raise RuntimeError("Action taken is invalid.")

    def delete_last_action(self):
        raise NotImplementedError

    def has_outcome(self):
        """
        RETURNS:
            True if game has ended
            False if game is still ongoing
        """
        raise NotImplementedError

    def winner(self):
        """
        RETURNS:
            None if game is a draw
            winner if one of the players won
        """
        raise NotImplementedError
        if not self.has_outcome():
            raise RuntimeError("winner() cannot be called when outcome is undefined.")

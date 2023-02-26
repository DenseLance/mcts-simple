from __future__ import annotations
from .mcts import *
import math
from copy import deepcopy
from typing import List, Dict, Optional

class UCTNode(Node):
    # Note that exploration term is only included in choose_best_action() method and not in eval()
    def __init__(self, player: int, state: str, prev_node: Optional[UCTNode] = None, transposition_table: Optional[Dict[tuple, str]] = None, c: float = 2 ** 0.5):
        super().__init__(player, state, prev_node, transposition_table)
        self.c = c

    def add_child(self, next_player: int, next_state: str, action: int) -> None:
        if action not in self.children:
            if self.transposition_table is not None:
                key = (next_player, next_state)
                if key in self.transposition_table:
                    self.children[action] = self.transposition_table[key]
                else:
                    self.children[action] = self.transposition_table[key] = UCTNode(next_player, next_state, transposition_table = self.transposition_table, c = self.c)
            else:
                self.children[action] = UCTNode(next_player, next_state, prev_node = self, c = self.c)

    def choose_best_action(self, training: bool) -> int:
        return max(self.children, key = lambda action: ((self.children[action].eval(training) + self.c * (math.log(self.n) / self.children[action].n) ** 0.5) if self.children[action].n > 0 else float("inf"))) if training is True else super().choose_best_action(training)

class UCT(MCTS):
    def __init__(self, game: Game, allow_transpositions: bool = True, training: bool = True, c: float = 2 ** 0.5):
        self.game = game
        self.copied_game = deepcopy(self.game)

        self.transposition_table = dict() if allow_transpositions is True else None
        self.c = c
        self.root = UCTNode(self.game.current_player(), str(self.game.get_state()), transposition_table = self.transposition_table, c = self.c)
        if self.transposition_table is not None:
            self.transposition_table[(self.game.current_player(), str(self.game.get_state()))] = self.root
        self.training = training

    def selection(self, node: UCTNode) -> List[UCTNode]:
        return super().selection(node)

    def expansion(self, path: List[UCTNode]) -> List[UCTNode]:
        return super().expansion(path)

    def simulation(self, path: List[UCTNode]) -> List[UCTNode]:
        return super().simulation(path)

    def backpropagation(self, path: List[UCTNode]) -> None:
        return super().backpropagation(path)

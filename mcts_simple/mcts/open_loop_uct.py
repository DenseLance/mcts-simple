from __future__ import annotations
from .open_loop_mcts import *
import math
from copy import deepcopy
from typing import List, Optional

class OpenLoopUCTNode(OpenLoopNode):
    def __init__(self, player: int, action: Optional[int] = None, prev_node: Optional[OpenLoopNode] = None, c: float = 2 ** 0.5):
        super().__init__(player, action, prev_node)
        self.c = c

    def add_child(self, next_player: int, action: int) -> None:
        if action not in self.children:
            self.children[action] = OpenLoopUCTNode(next_player, action, prev_node = self, c = self.c)

    def choose_best_action(self, training: bool) -> int:
        return max(self.children, key = lambda action: ((self.children[action].eval(training) + self.c * (math.log(self.n) / self.children[action].n) ** 0.5) if self.children[action].n > 0 else float("inf"))) if training is True else super().choose_best_action(training)

class OpenLoopUCT(OpenLoopMCTS):
    def __init__(self, game: Game, training: bool = True, c: float = 2 ** 0.5):
        self.game = game
        self.copied_game = deepcopy(self.game)

        self.c = c
        self.root = OpenLoopUCTNode(self.game.current_player(), None, c = self.c)
        self.training = training

    def selection(self, node: OpenLoopUCTNode) -> List[OpenLoopUCTNode]:
        return super().selection(node)

    def expansion(self, path: List[OpenLoopUCTNode]) -> List[OpenLoopUCTNode]:
        return super().expansion(path)

    def simulation(self, path: List[OpenLoopUCTNode]) -> List[OpenLoopUCTNode]:
        return super().simulation(path)

    def backpropagation(self, path: List[OpenLoopUCTNode]) -> None:
        return super().backpropagation(path)

from __future__ import annotations
from .mcts import *
import os
import random
from copy import deepcopy
from typing import Any, List, Union, Optional

class OpenLoopNode(Node):
    def __init__(self, player: int, action: Optional[int] = None, prev_node: Optional[OpenLoopNode] = None, rng: random.Random = random.Random()):
        self.player = player # player that makes a move which leads to one of the child nodes
        self.action = action
        
        self.prev_node = prev_node
        self.children = dict() # {action: Node}

        self.is_expanded = False
        self.has_outcome = False

        self.w = 0. # number of games won by previous player where node was traversed
        self.n = 0 # number of games played where node was traversed

        self.rng = rng

    def add_child(self, next_player: int, action: int) -> None:
        if action not in self.children:
            self.children[action] = OpenLoopNode(next_player, action, prev_node = self, rng = self.rng)

class OpenLoopMCTS(MCTS):
    def __init__(self, game: Game, training: bool = True, seed: Optional[int] = None):
        self.game = game
        self.copied_game = deepcopy(self.game)

        self.seed = seed
        self.rng = random.Random(seed)

        self.root = OpenLoopNode(self.game.current_player(), None, rng = self.rng)
        self.training = training

    def selection(self, node: OpenLoopNode) -> List[OpenLoopNode]:
        return super().selection(node)

    def expansion(self, path: List[OpenLoopNode]) -> List[OpenLoopNode]:
        if self.copied_game.has_outcome() is True:
            path[-1].has_outcome = True
            return path

        if path[-1].is_expanded is False:
            for action in self.copied_game.possible_actions():
                expanded_game = deepcopy(self.copied_game)
                expanded_game.take_action(action)
                path[-1].add_child(expanded_game.current_player(), action)

            assert len(path[-1].children) > 0
            
            path[-1].is_expanded = True
            action = path[-1].choose_random_action()
            path.append(path[-1].children[action])
            self.copied_game.take_action(action)
        return path

    def simulation(self, path: List[OpenLoopNode]) -> List[OpenLoopNode]:
        while self.copied_game.has_outcome() is False:
            action = self.rng.choice(self.copied_game.possible_actions())
            self.copied_game.take_action(action)
            path[-1].add_child(self.copied_game.current_player(), action)
            path.append(path[-1].children[action])
        return path

    def backpropagation(self, path: List[OpenLoopNode]) -> None:
        return super().backpropagation(path)

    def partially_load_node(self, node_dict: Dict[str, Any]) -> OpenLoopNode:
        node = OpenLoopNode(None, rng = self.rng)
        node.__dict__.update(node_dict)
        return node

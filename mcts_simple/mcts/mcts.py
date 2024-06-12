from __future__ import annotations
import gc
import os
import pickle
import random
from copy import deepcopy
from tqdm.auto import tqdm
from typing import List, Dict, Union, Optional

class Node:
    def __init__(self, player: int, state: str, prev_node: Optional[Node] = None, transposition_table: Optional[Dict[tuple, str]] = None):
        self.player = player # player that makes a move which leads to one of the child nodes
        self.state = state
        
        self.prev_node = prev_node
        self.transposition_table = transposition_table # {(player, state): Node}
        self.children = dict() # {action: Node}

        self.is_expanded = False
        self.has_outcome = False

        self.w = 0. # number of games won by previous player where node was traversed
        self.n = 0 # number of games played where node was traversed

    def eval(self, training: bool) -> float:
        return self.w / self.n if self.n > 0 else float("inf") if training else 0.

    def add_child(self, next_player: int, next_state: str, action: int) -> None:
        if action not in self.children:
            if self.transposition_table is not None:
                key = (next_player, next_state)
                if key in self.transposition_table:
                    self.children[action] = self.transposition_table[key]
                else:
                    self.children[action] = self.transposition_table[key] = Node(next_player, next_state, transposition_table = self.transposition_table)
            else:
                self.children[action] = Node(next_player, next_state, prev_node = self)

    def choose_best_action(self, training: bool) -> int:
        return max(self.children, key = lambda action: self.children[action].eval(training))

    def choose_random_action(self) -> int:
        return random.sample(list(self.children), 1)[0]

class MCTS:
    def __init__(self, game: Game, allow_transpositions: bool = True, training: bool = True):
        self.game = game
        self.copied_game = deepcopy(self.game)

        self.transposition_table = dict() if allow_transpositions is True else None
        self.root = Node(self.game.current_player(), str(self.game.get_state()), transposition_table = self.transposition_table)
        if self.transposition_table is not None:
            self.transposition_table[(self.game.current_player(), str(self.game.get_state()))] = self.root
        self.training = training
        
    def selection(self, node: Node) -> List[Node]:
        path = [node]
        while path[-1].is_expanded is True and path[-1].has_outcome is False: # loop if not leaf node
            action = path[-1].choose_best_action(self.training)
            path.append(path[-1].children[action])
            self.copied_game.take_action(action)
        return path

    def expansion(self, path: List[Node]) -> List[Node]:
        if self.copied_game.has_outcome() is True:
            path[-1].has_outcome = True
            return path
        if path[-1].is_expanded is False:
            for action in self.copied_game.possible_actions():
                expanded_game = deepcopy(self.copied_game)
                expanded_game.take_action(action)
                path[-1].add_child(expanded_game.current_player(), str(expanded_game.get_state()), action)

            assert len(path[-1].children) > 0
            
            path[-1].is_expanded = True
            action = path[-1].choose_random_action()
            path.append(path[-1].children[action])
            self.copied_game.take_action(action)
        return path

    def simulation(self, path: List[Node]) -> List[Node]:
        while self.copied_game.has_outcome() is False:
            action = random.choice(self.copied_game.possible_actions())
            self.copied_game.take_action(action)
            path[-1].add_child(self.copied_game.current_player(), str(self.copied_game.get_state()), action)
            path.append(path[-1].children[action])
        return path

    def backpropagation(self, path: List[Node]) -> None:
        if self.copied_game.has_outcome() is True:
            winners = self.copied_game.winner()
            number_of_winners = len(winners)
            path[0].n += 1
            for i in range(1, len(path)):
                if number_of_winners > 0:
                    path[i].w += (path[i - 1].player in winners) / number_of_winners
                path[i].n += 1
            path[-1].has_outcome = True

    def step(self) -> None:
        if self.training is True:
            self.backpropagation(self.simulation(self.expansion(self.selection(self.root))))
        else:
            node = self.root
            while not self.copied_game.has_outcome():
                self.copied_game.render()
                if len(node.children) > 0:
                    action = node.choose_best_action(self.training)
                    node = node.children[action]
                else:
                    action = random.choice(self.copied_game.possible_actions())
                self.copied_game.take_action(action)
            self.copied_game.render()
            
        self.copied_game = deepcopy(self.game)
        gc.collect()

    def self_play(self, iterations: int = 1) -> None:
        desc = "Training" if self.training is True else "Evaluating"
        for _ in tqdm(range(iterations), desc = desc):
            self.step()

    def save(self, file_path: Union[str, os.PathLike]) -> None:
        game, copied_game, training = self.game, self.copied_game, self.training
        del self.game, self.copied_game, self.training
        with open(file_path, "wb") as handle:
            pickle.dump(self, handle, protocol = -1)
            handle.close()
        self.game, self.copied_game, self.training = game, copied_game, training

    def load(self, file_path: Union[str, os.PathLike]) -> None:
        with open(file_path, "rb") as handle:
            self.__dict__.update(pickle.load(handle).__dict__)
            handle.close()
        if self.transposition_table is not None:
            self.root = self.transposition_table[(self.game.current_player(), str(self.game.get_state()))]
        assert self.game.current_player() == self.root.player and str(self.game.get_state()) == self.root.state

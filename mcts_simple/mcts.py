import jsonpickle
from copy import deepcopy
from tqdm.notebook import tqdm
import math
import random
from .game import Game

class Node:
    def __init__(self, prev_state = None, state = None, action = None, player = None):
        self.state = state
        if prev_state is None and action is None:
            self.transposed_from = {}
        elif prev_state is None or action is None:
            raise RuntimeError("Previous state and action taken has to be both None or neither of them are None.")
        else:
            self.transposed_from = {prev_state: action} 
        self.children = []

        self.player = player # refers to player that is making a move during self.state to transpose into one of the nodes in self.children
        self.is_expanded = False
        self.outcome = False # Ongoing: False, Outcome present: True

        self.w = 0.
        self.n = 0

    def get_action(self, prev_state = None):
        return self.transposed_from[prev_state]

    def add_child_node(self, action, node: "Node") -> "Node":
        children_states = [child.state for child in self.children]
        if node.state not in children_states:
            self.children.append(node)
            node.transposed_from[self.state] = action
        else:
            node = self.children[children_states.index(node.state)]
        return node

    def add_child(self, state = None, action = None, player = None) -> "Node":
        children_states = [child.state for child in self.children]
        if state not in children_states:
            node = Node(self.state, state, action, player)
            self.children.append(node)
        else:
            node = self.children[children_states.index(state)]
        return node

    def expand(self, states: list, actions: list, players: list) -> list:
        self.is_expanded = True
        return [self.add_child(states[i], actions[i], players[i]) for i in range(len(states))]

    def has_children(self) -> bool:
        return bool(self.children)

    def has_outcome(self) -> bool:
        return self.outcome

    def is_leaf_node(self) -> bool:
        return not self.is_expanded or self.outcome

    def choose_random_child_node(self) -> "Node":
        if not self.is_leaf_node():
            return random.choice(self.children)

    def choose_best_child_node(self) -> "Node":
        if not self.is_leaf_node():
            return max(self.children, key = lambda node: node.evaluate_node())

    def get_child_by_state(self, next_state) -> "Node":
        return [node for node in self.children if node.state == next_state][0]

    def get_children_evaluations(self) -> list:
        return [node.evaluate_node() if node.evaluate_node() != math.inf else 0. for node in self.children]

    def get_children_actions(self) -> list:
        return [node.get_action(self.state) for node in self.children]

    def evaluate_node(self) -> float:
        if self.n != 0:
            return self.w / self.n
        else:
            return math.inf

class UCTNode(Node):
    def __init__(self, prev_state = None, state = None, action = None, player = None, c = math.sqrt(2)):
        super().__init__(prev_state, state, action, player)
        
        self.c = c

    def add_child_node(self, action, node: "UCTNode") -> "UCTNode":
        children_states = [child.state for child in self.children]
        if node.state not in children_states:
            self.children.append(node)
            node.transposed_from[self.state] = action
        else:
            node = self.children[children_states.index(node.state)]
        return node

    def add_child(self, state = None, action = None, player = None) -> "UCTNode":
        children_states = [child.state for child in self.children]
        if state not in children_states:
            node = UCTNode(self.state, state, action, player, self.c)
            self.children.append(node)
        else:
            node = self.children[children_states.index(state)]
        return node

    def choose_best_child_node(self) -> "UCTNode":
        if not self.is_leaf_node():
            return max(self.children, key = lambda node: node.evaluate_node(self))

    def get_child_by_state(self, next_state) -> "UCTNode":
        return [node for node in self.children if node.state == next_state][0]

    def get_children_evaluations(self) -> list:
        # We avoid the UCB1 formula as this method is only called after exploration is completed
        # We can exploit and utilise a greedy policy instead
        return [super(type(node), node).evaluate_node() if super(type(node), node).evaluate_node() != math.inf else 0. for node in self.children]
##        return [node.evaluate_node(self) if node.evaluate_node(self) != math.inf else 0. for node in self.children]
    
    def evaluate_node(self, parent: "UCTNode") -> float:
        # UCB1 formula
        if self.n != 0:
            return self.w / self.n + self.c * math.sqrt(math.log(parent.n) / self.n)
        else:
            return math.inf

class OpenLoopNode(Node):
    def __init__(self, action = None, player = None):
        self.action = action
        self.children = []

        self.player = player # refers to player that is making the move this turn
        self.is_expanded = False
        self.outcome = False # Ongoing: False, Outcome present: True

        self.w = 0.
        self.n = 0

    def get_action(self):
        return self.action

    def add_child_node(self, node: "OpenLoopNode") -> "OpenLoopNode":
        children_actions = [child.action for child in self.children]
        if node.action not in children_actions:
            self.children.append(node)
        else:
            node = self.children[children_actions.index(node.action)]
        return node

    def add_child(self, action = None, player = None) -> "OpenLoopNode":
        children_actions = [child.action for child in self.children]
        if action not in children_actions:
            node = OpenLoopNode(action, player)
            self.children.append(node)
        else:
            node = self.children[children_actions.index(action)]
        return node

    def expand(self, actions: list, players: list) -> list:
        self.is_expanded = True
        return [self.add_child(actions[i], players[i]) for i in range(len(actions))]

    def choose_random_child_node(self) -> "OpenLoopNode":
        if not self.is_leaf_node():
            return random.choice(self.children)

    def choose_best_child_node(self) -> "OpenLoopNode":
        if not self.is_leaf_node():
            return max(self.children, key = lambda node: node.evaluate_node())

    def get_child_by_state(self, next_state) -> "OpenLoopNode":
        raise NotImplementedError("This method does not exist for OpenLoopNode.")

    def get_child_by_action(self, next_action) -> "OpenLoopNode":
        return [node for node in self.children if node.action == next_action][0]

    def get_children_actions(self) -> list:
        return [node.get_action() for node in self.children]

class OpenLoopUCTNode(OpenLoopNode):
    def __init__(self, action = None, player = None, c = math.sqrt(2)):
        super().__init__(action, player)
        
        self.c = c

    def add_child_node(self, node: "OpenLoopUCTNode") -> "OpenLoopUCTNode":
        children_actions = [child.action for child in self.children]
        if node.action not in children_actions:
            self.children.append(node)
        else:
            node = self.children[children_actions.index(node.action)]
        return node

    def add_child(self, action = None, player = None) -> "OpenLoopUCTNode":
        children_actions = [child.action for child in self.children]
        if action not in children_actions:
            node = OpenLoopUCTNode(action, player, self.c)
            self.children.append(node)
        else:
            node = self.children[children_actions.index(action)]
        return node

    def choose_best_child_node(self) -> "OpenLoopUCTNode":
        if not self.is_leaf_node():
            return max(self.children, key = lambda node: node.evaluate_node(self))

    def get_child_by_state(self, next_state) -> "OpenLoopUCTNode":
        raise NotImplementedError("This method does not exist for OpenLoopUCTNode.")

    def get_child_by_action(self, next_action) -> "OpenLoopUCTNode":
        return [node for node in self.children if node.action == next_action][0]

    def get_children_evaluations(self) -> list:
        # We avoid the UCB1 formula as this method is only called after exploration is completed
        # We can exploit and utilise a greedy policy instead
        return [super(type(node), node).evaluate_node() if super(type(node), node).evaluate_node() != math.inf else 0. for node in self.children]
##        return [node.evaluate_node(self) if node.evaluate_node(self) != math.inf else 0. for node in self.children]
    
    def evaluate_node(self, parent: "OpenLoopUCTNode") -> float:
        # UCB1 formula
        if self.n != 0:
            return self.w / self.n + self.c * math.sqrt(math.log(parent.n) / self.n)
        else:
            return math.inf

class MCTS:
    def __init__(self, game: "Game"):
        """
        Monte Carlo Tree Search (MCTS) attempts to identify the most promising moves
        at each state by choosing random actions at that state for every episode
        (playouts/rollouts). The final game result of each episode is then used to
        determine the weight of all nodes traversed during that episode so that the
        probability of choosing an action that yields higher current and potential
        rewards is increased.

        There are 4 stages to the MCTS:
        1. Selection
            Traverse through the search tree from the root node to a leaf node, while 
            only selecting the most promising child nodes. Leaf node in this case refers to
            a node that has not yet gone through the expansion stage, rather than its
            traditional definition which is "a node without child nodes".
        2. Expansion
            If the leaf node does not lead to an outcome to the episode (e.g. win/lose/
            draw), create at least one child node for that leaf node and choose one child
            node from those created. In mcts-simple's implementation, the child node is only
            chosen during simulation.
        3. Simulation
            Complete one episode starting from the chosen child node, where random actions
            are chosen for future states. An episode is only completed when an outcome can
            be yielded from it.
        4. Backpropagation
            The outcome yielded from the simulated episode in stage 3 should be used to
            update information in traversed nodes.

        * We assume that states are unique.
        * Root node's score is almost never evaluated, and at most only the number of visits
        "n" is used.
        * We assume the node with the highest q-value/win rate/reward is the most visited node.
        """
        if not isinstance(game, Game):
            raise TypeError("Parameter 'game' does not belong to Game class.")
        
        self.game = game
        self.root = Node(None, self.game.get_state(), None, self.game.current_player())

        # Accounts for nodes that have been traversed due to expansion and simulation
        # Transposition table is used for states that have been reached via different action orders
        # Arithmetic mean is used to evaluate a state
        self.nodes = {self.root.state: self.root}

    @staticmethod
    def best(actions: list, scores: list):
        return actions[scores.index(max(scores))]

    @staticmethod
    def linear(actions: list, scores: list):
        return random.choices(actions, weights = scores)[0]

    @staticmethod
    def tanh(actions: list, scores: list):
        return random.choices(actions, weights = [math.tanh(score) for score in scores])[0]

    @staticmethod
    def softmax(actions: list, scores: list):
        return random.choices(actions, weights = [math.exp(score) for score in scores])[0]

    def self_play(self, activation: str):
        activation_functions = {"best": lambda actions, scores: self.best(actions, scores),
                                "linear": lambda actions, scores: self.linear(actions, scores),
                                "tanh": lambda actions, scores: self.tanh(actions, scores),
                                "softmax": lambda actions, scores: self.softmax(actions, scores)}
        
        if activation not in activation_functions:
            raise ValueError("Could not interpret activation function identifier.")
        
        game = deepcopy(self.game)
        curr_node = self.root
        game.render()
        while not game.has_outcome():
            if curr_node is not None and curr_node.has_children(): # ignores actions that are possible but are unexplored if child nodes are present
                action = activation_functions[activation](curr_node.get_children_actions(), curr_node.get_children_evaluations())
                game.take_action(action)
                curr_node = curr_node.get_child_by_state(game.get_state())
            else:
                action = random.choice(game.possible_actions())
                game.take_action(action)
                curr_node = None
            game.render()

        del game

    def play_with_human(self, activation: str):
        activation_functions = {"best": lambda actions, scores: self.best(actions, scores),
                                "linear": lambda actions, scores: self.linear(actions, scores),
                                "tanh": lambda actions, scores: self.tanh(actions, scores),
                                "softmax": lambda actions, scores: self.softmax(actions, scores)}
        
        if activation not in activation_functions:
            raise ValueError("Could not interpret activation function identifier.")
        if self.game.number_of_players() <= 1:
            raise ValueError("At least 2 players are needed to support human play.")
        
        game = deepcopy(self.game)
        player_number = random.randint(1, game.number_of_players())
        players = set()
        player = None
        curr_node = self.root
        game.render()
        while not game.has_outcome():
            if player is None:
                players.add(curr_node.player)
                if len(players) == player_number:
                    player = curr_node.player
                    del players
            if player is not None and game.current_player() == player:
                action = input("Input user action: ")
                while action not in game.possible_actions():
                    action = input("Input user action: ")
                game.take_action(action)
                if curr_node is not None and curr_node.has_children():
                    try:
                        curr_node = curr_node.get_child_by_state(game.get_state())
                    except:
                        curr_node = None
                else:
                    curr_node = None
            else:
                if curr_node is not None and curr_node.has_children(): # ignores actions that are possible but are unexplored if child nodes are present
                    action = activation_functions[activation](curr_node.get_children_actions(), curr_node.get_children_evaluations())
                    game.take_action(action)
                    curr_node = curr_node.get_child_by_state(game.get_state())
                else:
                    action = random.choice(game.possible_actions())
                    game.take_action(action)
                    curr_node = None
            game.render()

        del game

    def step(self):
        game = deepcopy(self.game)
        path, game = self.selection(self.root, game)
        self.expansion(path[-1], game)
        extended_path, game = self.simulation(path[-1], game)
        self.backpropagation(path + extended_path, game)
        
        del path, extended_path, game

    def run(self, iterations: int):
        if not isinstance(iterations, int):
            raise TypeError("Parameter 'iterations' does not belong to int class.")
        assert iterations > 0
        
        for _ in tqdm(range(iterations), desc = "Simulating"):
            self.step()

    def selection(self, node: "Node", game: "Game") -> (list, "Game"):
        path = [node]
        while not path[-1].is_leaf_node():
            path.append(path[-1].choose_best_child_node())
            game.take_action(path[-1].get_action(game.get_state()))
        return path, game

    def expansion(self, node: "Node", game: "Game"):
        if not game.has_outcome(): # leaf node but does not have outcome
            states, actions, players = [], [], []
            for action in game.possible_actions():
                game.take_action(action)
                state = game.get_state()
                player = game.current_player()
                if state not in self.nodes:
                    states.append(state)
                    actions.append(action)
                    players.append(player)
                else:
                    node.add_child_node(action, self.nodes[state]) # since state has been seen before, use node from transposition table
                game.delete_last_action()
            nodes = node.expand(states, actions, players)
            self.nodes = {**self.nodes, **dict(zip([node.state for node in nodes], nodes))}

    def simulation(self, node: "Node", game: "Game") -> (list, "Game"):
        extended_path = [node]
        while not game.has_outcome():
            action = random.choice(game.possible_actions())
            game.take_action(action)
            state = game.get_state()
            player = game.current_player()
            if state not in self.nodes:
                extended_path.append(extended_path[-1].add_child(state, action, player))
                self.nodes[state] = extended_path[-1]
            else:
                extended_path.append(extended_path[-1].add_child_node(action, self.nodes[state])) # since state has been seen before, use node from transposition table
        return extended_path[1:], game

    def backpropagation(self, path: list, game: "Game"):
        result = game.winner()
        for index in range(len(path) - 1, 0, -1):
            path[index].n += 1
            path[index].w += 0.5 if result is None else 1. if result == path[index - 1].player else 0.
        path[0].n += 1
        path[-1].outcome = True

    def _export(self, file: str):
        with open(file, "w") as f:
            f.write(jsonpickle.encode(self, keys = True))
            f.close()

    def _import(self, file: str):
        with open(file, "r") as f:
            game = self.game
            self.__dict__.update(jsonpickle.decode(f.read(), keys = True).__dict__)
            self.game = game
            self.root = self.nodes[self.game.get_state()]
            f.close()

class UCT(MCTS):
    def __init__(self, game: "Game", c = math.sqrt(2)):
        """
        Upper Confidence bounds applied to Trees (UCT), a variation of MCTS, is often used
        instead of vanilla MCTS for a few reasons, mainly:
        1. MCTS emphasizes entirely on exploitation. On the other hand, UCT is able to balance
        exploration and exploitation.
        2. MCTS may favour a losing move despite the presence of one or few forced refutations.
        UCT attempts to deal with this limitation of the original MCTS.

        UCT uses the UCB1 formula to evaluate actions at each state.
        The exploration parameter c in the UCB1 formula is theoretically equal to sqrt(2),
        but it can be changed to fit your needs.
        """
        if not isinstance(game, Game):
            raise TypeError("Parameter 'game' does not belong to Game class.")

        self.c = c

        self.game = game
        self.root = UCTNode(None, self.game.get_state(), None, self.game.current_player(), self.c)

        # Accounts for nodes that have been traversed due to expansion and simulation
        # Transposition table is used for states that have been reached via different action orders
        # Arithmetic mean is used to evaluate a state
        self.nodes = {self.root.state: self.root}

class OpenLoopMCTS(MCTS):
    def __init__(self, game: "Game"):
        """
        Most of the time, a closed loop MCTS is sufficient in dealing with reinforcement learning
        problems. However, when it comes to games that have non-deterministic or non-discrete
        states, an open loop MCTS is required. Open loop MCTS would completely eliminate the need
        for chance nodes. Transpositions will also not be considered since we would ignore the game
        state entirely. Since the tree is now significantly smaller in an open loop MCTS, the
        branching factor is also a lot smaller and evaluations may be less accurate. This also
        means that results can converge at a faster rate.

        This variant of MCTS can be used for deterministic games as well.

        * Since there is no transposition table in an open loop MCTS, we generally cannot use it to
        play from another state that is not the starting state.
        """
        if not isinstance(game, Game):
            raise TypeError("Parameter 'game' does not belong to Game class.")

        self.game = game
        self.root = OpenLoopNode(None, self.game.current_player())

    def self_play(self, activation: str):
        activation_functions = {"best": lambda actions, scores: self.best(actions, scores),
                                "linear": lambda actions, scores: self.linear(actions, scores),
                                "tanh": lambda actions, scores: self.tanh(actions, scores),
                                "softmax": lambda actions, scores: self.softmax(actions, scores)}
        
        if activation not in activation_functions:
            raise ValueError("Could not interpret activation function identifier.")
        
        game = deepcopy(self.game)
        curr_node = self.root
        game.render()
        while not game.has_outcome():
            if curr_node is not None and curr_node.has_children(): # ignores actions that are possible but are unexplored if child nodes are present
                action = activation_functions[activation](curr_node.get_children_actions(), curr_node.get_children_evaluations())
                game.take_action(action)
                curr_node = curr_node.get_child_by_action(action)
            else:
                action = random.choice(game.possible_actions())
                game.take_action(action)
                curr_node = None
            game.render()

        del game

    def play_with_human(self, activation: str):
        activation_functions = {"best": lambda actions, scores: self.best(actions, scores),
                                "linear": lambda actions, scores: self.linear(actions, scores),
                                "tanh": lambda actions, scores: self.tanh(actions, scores),
                                "softmax": lambda actions, scores: self.softmax(actions, scores)}
        
        if activation not in activation_functions:
            raise ValueError("Could not interpret activation function identifier.")
        if self.game.number_of_players() <= 1:
            raise ValueError("At least 2 players are needed to support human play.")
        
        game = deepcopy(self.game)
        player_number = random.randint(1, game.number_of_players())
        players = set()
        player = None
        curr_node = self.root
        game.render()
        while not game.has_outcome():
            if player is None:
                if curr_node.player is not None:
                    players.add(curr_node.player)
                if len(players) == player_number:
                    player = curr_node.player
                    del players
            if player is not None and game.current_player() == player:
                action = input("Input user action: ")
                while action not in game.possible_actions():
                    action = input("Input user action: ")
                game.take_action(action)
                if curr_node is not None and curr_node.has_children():
                    try:
                        curr_node = curr_node.get_child_by_action(action)
                    except:
                        curr_node = None
                else:
                    curr_node = None
            else:
                if curr_node is not None and curr_node.has_children(): # ignores actions that are possible but are unexplored if child nodes are present
                    action = activation_functions[activation](curr_node.get_children_actions(), curr_node.get_children_evaluations())
                    game.take_action(action)
                    curr_node = curr_node.get_child_by_action(action)
                else:
                    action = random.choice(game.possible_actions())
                    game.take_action(action)
                    curr_node = None
            game.render()

        del game

    def selection(self, node: "Node", game: "Game") -> (list, "Game"):
        path = [node]
        while not path[-1].is_leaf_node():
            path.append(path[-1].choose_best_child_node())
            game.take_action(path[-1].get_action())
        return path, game

    def expansion(self, node: "Node", game: "Game"):
        if not game.has_outcome(): # leaf node but does not have outcome
            actions, players = [], []
            for action in game.possible_actions():
                game.take_action(action)
                actions.append(action)
                players.append(game.current_player())
                game.delete_last_action()
            node.expand(actions, players)

    def simulation(self, node: "Node", game: "Game") -> (list, "Game"):
        extended_path = [node]
        while not game.has_outcome():
            action = random.choice(game.possible_actions())
            game.take_action(action)
            player = game.current_player()
            extended_path.append(extended_path[-1].add_child(action, player))
        return extended_path[1:], game

    def _import(self, file: str):
        with open(file, "r") as f:
            game = self.game
            self.__dict__.update(jsonpickle.decode(f.read(), keys = True).__dict__)
            self.game = game
            f.close()    

class OpenLoopUCT(OpenLoopMCTS):
    def __init__(self, game: "Game", c = math.sqrt(2)):
        if not isinstance(game, Game):
            raise TypeError("Parameter 'game' does not belong to Game class.")

        self.c = c

        self.game = game
        self.root = OpenLoopUCTNode(None, self.game.current_player(), self.c)

def get_action_space(): # required if PUCT is used
    raise NotImplementedError

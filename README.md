# mcts-simple

*mcts-simple* is a Python3 library that allows reinforcement learning problems to be solved easily with its implementations of Monte Carlo Tree Search.

### Monte Carlo Tree Search (MCTS)

MCTS attempts to identify the most promising moves at each state by choosing random actions at that state for every episode (playouts/rollouts). The final game result of each episode is then used to determine the weight of all nodes traversed during that episode so that the probability of choosing an action that yields higher current and potential rewards is increased.

**There are 4 stages to the MCTS:**

1. Selection
    - Traverse through the search tree from the root node to a leaf node, while only selecting the most promising child nodes. Leaf node in this case refers to a node that has not yet gone through the expansion stage, rather than its traditional definition which is "a node without child nodes".
2. Expansion
    - If the leaf node does not lead to an outcome to the episode (e.g. win/lose/draw), create at least one child node for that leaf node and choose one child node from those created.
3. Simulation
    - Complete one episode starting from the chosen child node, where random actions are chosen for future states. An episode is only completed when an outcome can be yielded from it.
4. Backpropagation
    - The outcome yielded from the simulated episode in stage 3 should be used to update information in traversed nodes.

**Note:**

* We assume that states are unique.
* Root node's score is almost never evaluated, and at most only the number of visits "n" is used.

### Upper Confidence bounds applied to Trees (UCT)

UCT, a variation of MCTS, is often used instead of vanilla MCTS for a few reasons, mainly:
1. MCTS emphasizes entirely on exploitation. On the other hand, UCT is able to balance exploration and exploitation.
2. MCTS may favour a losing move despite the presence of one or few forced refutations. UCT attempts to deal with this limitation of the original MCTS.

UCT uses the UCB1 formula to evaluate actions at each state. The exploration parameter c in the UCB1 formula is theoretically equal to sqrt(2), but it can be changed to fit your needs.

### How to use mcts-simple

*mcts-simple* only supports python 3.7 and above.

#### Dependencies

*mcts-simple* requires the following libraries:

* json-pickle
* tqdm

#### User installation

In cmd,

```cmd
pip install mcts-simple
```

In your python file,

```python
from mcts_simple import *
```

#### Creating your own game environment

For the progress bar to work best, use Jupyter Notebook or another platform that supports carriage return "/r". 

Create a class for your game by inheriting the Game class from *mcts-simple*, and define the following methods for your class:

|          Method           |                         What it does                         |
| :-----------------------: | :----------------------------------------------------------: |
|    \_\_init\_\_(self)     |                   Initialises the object.                    |
|       render(self)        | Returns a visual representation of the current state of the game. |
|      get_state(self)      | Returns current state of the game.<br>Note:<br><ol><li>Provide a hashable state.</li><li>Ensure that the state provided during the game does not coincide with the state provided at the start of the game</li><li>Best to include the player that is taking an action this turn within the state.</li></ol> |
|  number_of_players(self)  |                  Returns number of players.                  |
|   current_player(self)    |    Returns the player that is taking an action this turn.    |
|  possible_actions(self)   |       Returns the actions that can be taken this turn.       |
| take_action(self, action) | Player takes action. It is best to check if action is in possible actions (see source code). Action should be string type to support the play_with_human() method from MCTS. Note that even if action leads to the game ending, next player should still be chosen. |
| delete_last_action(self)  | Last action is removed. Current state is reverted back to previous state. |
|     has_outcome(self)     | Returns True if game has ended. Returns False if game is still ongoing. |
|       winner(self)        | Returns None if game is a draw. Returns the winner if one of the players won. It is best to check if outcome is defined. |

After creating your environment, you're basically done! You can train and export your MCTS with just 3 lines of code (assuming your game environment class is named *"YourGame"*:

```python
mcts = MCTS(YourGame())
mcts.run(iterations = 50000)
mcts._export("mcts.json")
```

You can import your trained MCTS, with another 3 lines of code:

```python
mcts = MCTS(TicTacToe())
mcts._import("mcts.json")
mcts.self_play(activation = "best")
```

If you have any issues in creating your environment, you can browse the source code or check out the examples provided here.

### Contributions

I appreciate if you are able to contribute to this project, since currently I am the only one maintaining this module. This is also the first public Python package that I have written, so if you think that something is wrong with my code, you can open an issue and I'll try my best to resolve it!

There are also other variants of MCTS, so feel free to give some pointers to how they should be implemented.

### To Do

- [ ] Resolve issue with numpy arrays as state: https://stackoverflow.com/questions/66847901/python-array-issue-with-jsonpickle
- [ ] Implement tree for MC-RAVE (Rapid Action Value Estimation for MCTS).
- [ ] Implement example with DNN + MCTS (using a specialised evaluation formula) for chess.
- [ ] Implement conversion from OpenAI-Gym environment to Game class in *mcts-simple*.
- [ ] Implement alpha-beta pruning.
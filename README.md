# mcts-simple

[![Python](https://img.shields.io/pypi/pyversions/mcts-simple.svg?style=plastic)](https://badge.fury.io/py/mcts-simple) [![Version](https://img.shields.io/pypi/v/mcts-simple.svg?logo=pypi)](https://badge.fury.io/py/mcts-simple) [![GitHub license](https://img.shields.io/github/license/denselance/mcts-simple.svg)](https://github.com/DenseLance/mcts-simple/blob/main/LICENSE) [![PyPI downloads](https://img.shields.io/pypi/dm/mcts-simple.svg)](https://pypistats.org/packages/mcts-simple)

*mcts-simple* is a Python3 library that allows reinforcement learning problems to be solved easily with its implementations of Monte Carlo Tree Search.

### Version Updates (v1.0.0)

* Implementing a more lightweight, faster, and memory efficient version of MCTS.
  * More than 10x reduction in space and time complexity.
  * Linear instead of exponential time complexity.
* Automatic hashing of state using `str()` which can be reverted using Python's in-built `eval()`.
  * Now your game state can be returned as a list! However, do ensure that typings of both state and action remain constant throughout.
* Type hints are now supported for better documentation of code.
* Different variants of MCTS are split into different files for improved readability of code.
* cPickle is now used in place of JSONPickle to speed up the exporting and importing process of MCTS.
* tqdm now automatically detects the IDE that is used and outputs the progress bar accordingly.
* Removed `delete_last_action()` method from game environment class.
* `_import()` and `_export()` methods are now referred to as `save()` and `load()` respectively.
* Player name is automatically paired with state and used as key when searching through transposition table.

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
* Root node's score is almost never evaluated, and at most only the number of visits, *n*, is used.
* We assume the node with the highest average returns is the most visited node.

### Upper Confidence bounds applied to Trees (UCT)

UCT, a variation of MCTS, is often used instead of vanilla MCTS for a few reasons, mainly:
1. MCTS emphasizes entirely on exploitation. On the other hand, UCT is able to balance exploration and exploitation.
2. MCTS may favour a losing move despite the presence of one or few forced refutations. UCT attempts to deal with this limitation of the original MCTS.

UCT uses the UCB1 formula to evaluate actions at each state. The exploration parameter c in the UCB1 formula is theoretically equal to $\sqrt{2}$, but it can be changed depending on each situation.

### Open Loop MCTS

Most of the time, a closed loop MCTS is sufficient in dealing with reinforcement learning problems. However, when it comes to games that have non-deterministic or non-discrete states, an open loop MCTS is required. Open loop MCTS would completely eliminate the need for chance nodes. Transpositions will also not be considered since we would ignore the game state entirely. Since the tree is now significantly smaller in an open loop MCTS, the branching factor is also a lot smaller and evaluations may be less accurate. This would also mean that results are more likely to converge at a faster rate. This variant of MCTS can be used for deterministic games as well.

**Note:**

* Since there is no transposition table in an open loop MCTS, we cannot change the initial starting state.

### How to use mcts-simple

*mcts-simple* only supports python 3.7 and above. If you want to use *mcts-simple* for other versions of Python, do note that it may not function as intended.

Module is tested only on Windows. Issues when setting up on Linux and macOS are still relatively unknown.

#### Dependencies

*mcts-simple* requires the following libraries, which is automatically installed together with it unless otherwise specified:

* tqdm
* gymnasium (for CartPole example only)

#### User installation

In command prompt on Windows,

```cmd
pip install mcts-simple
```

In your python file,

```python
from mcts_simple import *
```

#### Creating your own game environment

Create a class for your game by inheriting the `Game` class from *mcts-simple*, and define the following methods for your class:

|           Method           |                         What it does                         |
| :------------------------: | :----------------------------------------------------------: |
|        `__init__()`        |                   Initialises the object.                    |
|         `render()`         | Returns a visual representation of the current state of the game. |
|       `get_state()`        |              Returns current state of the game.              |
|   `number_of_players()`    |                  Returns number of players.                  |
|     `current_player()`     | Returns the player that is taking an action this turn.<br>**Note:** Players are labelled from `0` to `number of players - 1`. |
|    `possible_actions()`    | Returns the possible actions that can be taken by current player this turn. |
| `take_action(action: int)` | Player takes action.<br>**Note:** Even if action leads to the end of the game, next player should still be chosen. |
|      `has_outcome()`       | Returns True if game has ended. Returns False if game is still ongoing. |
|         `winner()`         | Returns empty list if all players lose. Returns list of players if game ends in a draw. Returns list of winners if at least 1 player wins. |

After creating your game environment, you're basically done! You can train and export your MCTS with just 3 lines of code, noting that `YourGame()` should be the game environment class you have created based on the above:

```python
mcts = MCTS(YourGame(), training = True)
mcts.self_play(iterations = 50000)
mcts.save("game.mcts")
```

You can import your trained MCTS and see how it performs with another 3 lines of code:

```python
mcts = MCTS(YourGame(), training = False)
mcts.load("game.mcts")
mcts.self_play()
```

If you have any issues in creating your environment, you can browse the source code or check out the examples provided <a href = "https://github.com/DenseLance/mcts-simple/tree/main/examples">here</a>.

### Contributions

I appreciate if you are able to contribute to this project as I am the only contributor for now. This is also the first public Python package that I have written, so if you think that something is wrong with my code, you can open an issue and I'll try my best to resolve it!

### Work in Progress

- [ ] Implement PUCT.
- [ ] Implement MC-RAVE.
# Python Snake Game

Welcome to the Python Snake Game, a fun and engaging project where you can pit different types of AI-controlled snakes against each other. This game includes different types of snakes and is open to support even more algorithms. The `ManualSnake` has to be operated by the user. The `RandomSnake` moves randomly across the game grid, which shows major flaws as a strategy. The `AutoSnake`while the `AISnake` uses advanced reinforcement learning to make its moves.

## Table of Contents

- [Python Snake Game](#python-snake-game)
  - [Table of Contents](#table-of-contents)
  - [Installation](#installation)
  - [Usage](#usage)
  - [Snake Modules](#snake-modules)
    - [RandomSnake](#randomsnake)
    - [AISnake](#aisnake)
  - [Contributing](#contributing)

## Installation

Before you begin, ensure you have met the following requirements:

- You have installed the latest version of Python (Python 3.8 or later is recommended)
- You have a Windows/Linux/Mac machine.

To install the Python Snake Game, follow these steps:

```bash
git clone https://github.com/ExperTeach/Snake.git
cd python-snake-game
pip install -r requirements.txt
```

## Usage

To play the Python Snake Game, follow these steps:

```bash
python main.py
```

To specify which snake implementation should be used start the game with one of the following arguments:

```bash
python main.py --gamestyle="ai-snake"
python main.py --gamestyle="auto-snake"
python main.py --gamestyle="random-snake"
python main.py --gamestyle="snake"
```

## Snake Modules

### RandomSnake

The `RandomSnake` class defines a snake that moves randomly across the game grid. It uses a simple algorithm to choose a random direction for each move.

### AISnake

The `AISnake` class uses reinforcement learning to control the snake's movements. It uses a trained model to predict the best move based on the current state of the game. This snake tends to perform better than the `RandomSnake`, but it's not perfect. It's an excellent opportunity to see reinforcement learning in action!

## Contributing

If you want to contribute to the Python Snake Game, follow these steps:

1. Fork this repository.
2. Make Changes and commit them to your fork
3. Push to the fork Github repository
4. Create the pull request with the ExperTeach/Snake repository

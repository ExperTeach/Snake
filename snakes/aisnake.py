from helper.model_parser import ModelParser
from helper.style import BLOCK_SIZE
from ai.actions import Action
from snakes.snake import *
from ai.states import State
import numpy as np

class AISnake(Snake):
    
    alpha = 0.5 # Learning Rate
    gamma = 0.85 # Discount Factor
    epsilon = 0.9
    is_danger = 0
    action_space = Action.actions()
    try:
        with open("ai/model/q_table.json","r") as file:
            q_table = ModelParser.load_q_table(file)
    except FileNotFoundError as err:
        # Initial State of the Q-Table as Fallback if file is empty    
        q_table = {}
        for state in State.states():
            q_table[state] = {}
            for action in Action.actions():
                q_table[state][action] = 0
          
    
    def __init__(self, start_x, start_y, block_size):
        super().__init__(start_x, start_y, block_size)
        # A list of all possible states, saved as tuples
        state_space = []
        
        for x in range(0, 22*BLOCK_SIZE, BLOCK_SIZE):
            for y in range(0, 18*BLOCK_SIZE, BLOCK_SIZE):
                for direction in Direction:
                    for danger in [0, 1]:
                        state_space.append((x, y, direction, danger))
        

        
    def update_q_table(q_table, state, action, reward, new_state, alpha, gamma):
        max_future_q = np.max(list(q_table[new_state].values()))
        current_q = q_table[state][action]

        new_q = current_q + alpha * (reward + gamma * max_future_q - current_q)
        #new_q = reward
        if state[2] is not Direction.NONE:    # initial state ignored
            AISnake.q_table[state][action] = new_q

    def choose_action(state, epsilon):
        if random.uniform(0, 1) < epsilon:
            # Take a random action
            choices = AISnake.action_space.copy()
            if state[2] in choices:
                choices.remove(state[2])
            return random.choice(choices)
        else:
            # Take the best known action for this state
            q_table_entry = AISnake.q_table[state]
            index = np.argmax(AISnake.q_table[state])
            
            values = np.array(list(AISnake.q_table[state].values()))
            keys = np.array(list(AISnake.q_table[state].keys()))

            max_value_key = keys[np.argmax(values)]
            return max_value_key

    def move(self):
        # The current state of the snake
        head_x, head_y = self.body[0]
        current_state = (head_x, head_y, self.direction, self.is_danger)

        # Get action based on the current state and epsilon
        action = AISnake.choose_action(current_state, self.epsilon)
        
        # Update the direction based on the action
        self.direction = action

        # Move the snake in the new direction
        if self.direction == Direction.UP:
            head_y -= BLOCK_SIZE
        elif self.direction == Direction.DOWN:
            head_y += BLOCK_SIZE
        elif self.direction == Direction.LEFT:
            head_x -= BLOCK_SIZE
        elif self.direction == Direction.RIGHT:
            head_x += BLOCK_SIZE
            
        self.body.insert(0, [head_x, head_y])  # add new position to the head of the snake
        self.body.pop()  # remove the tail of the snake
            
        new_state = (head_x, head_y, self.direction, self.is_danger)
        # Decrease epsilon
        #self.epsilon = max(self.epsilon * self.epsilon_decay, self.min_epsilon)
        return current_state, action, new_state
    
    def handle_event(self,event):
        pass
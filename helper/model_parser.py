import json
from game.directions import Direction
from ai.states import State
from ai.actions import Action

class ModelParser():
    
    @staticmethod
    def load_q_table(file):
        # load the stringified dictionary as a basic data type dictionary
        q_table_raw = json.loads(file.read())

        # reconstruct the keys and values with enum types
        q_table = {}

        items = q_table_raw.items()

        for k, v in items:
            # parse the key string back into a tuple
            # strip the parentheses, split by commas, and parse each item
            x, y, direction, danger = k.strip("()").split(", ")

            x = int(x)
            y = int(y)
            # strip the Direction enum string to get the name
            direction = Direction[direction.split(".")[1].split(":")[0]]
            danger = int(danger)

            # for the values, map the Direction string to the enum
            actions = {Direction[action.split(".")[1]]: value for action, value in v.items()}
            q_table[(x, y, direction, danger)] = actions
        
        # Initial State of the Q-Table as Fallback if file is empty    
        if len(q_table) == 0:
            for state in State.states():
                q_table[state] = {}
                for action in Action.actions():
                    q_table[state][action] = 0
        
        return q_table
    
    @staticmethod
    def store_q_table(file, q_table):
        # we need to convert the keys and values to basic data types so JSON can handle them
        json.dump({str(k): {str(ka): va for ka, va in v.items()} for k, v in q_table.items()}, file)

from game.directions import Direction

class Action():
    action_space = [Direction.UP, Direction.DOWN, Direction.LEFT, Direction.RIGHT]
    
    @staticmethod
    def actions():
        return Action.action_space
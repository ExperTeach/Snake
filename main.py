import argparse
import game.game

if __name__ == "__main__":
    parser = argparse.ArgumentParser()

    # Add the gamestyle argument.
    # Default is "ai-snake", and the type is str.
    parser.add_argument('--gamestyle', default="snake", type=str, help="Set the game style")

    args = parser.parse_args()
    
    print(args.gamestyle)
    game.game.main(args.gamestyle)

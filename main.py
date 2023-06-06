import argparse
import game.game

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    # Add the autoplay argument.
    # Store true if --autoplay is given, else store false.
    parser.add_argument('--autoplay', action='store_true', help="Enable autoplay")

    # Add the gamestyle argument.
    # Default is "ai-snake", and the type is str.
    parser.add_argument('--gamestyle', default="snake", type=str, help="Set the game style")

    args = parser.parse_args()
    game.game.main(args.autoplay, args.gamestyle)

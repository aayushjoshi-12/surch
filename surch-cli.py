import argparse
import time

from engine import SurchEngine
from utils import retrieve_history

ascii_art = """
███████╗██╗   ██╗██████╗  ██████╗██╗  ██╗
██╔════╝██║   ██║██╔══██╗██╔════╝██║  ██║
███████╗██║   ██║██████╔╝██║     ███████║
╚════██║██║   ██║██╔══██╗██║     ██╔══██║
███████║╚██████╔╝██║  ██║╚██████╗██║  ██║
╚══════╝ ╚═════╝ ╚═╝  ╚═╝ ╚═════╝╚═╝  ╚═╝                 
"""


def main():
    parser = argparse.ArgumentParser(
        description="Surch: A conversational search engine"
    )
    parser.add_argument("-u", "--user_id", help="User id", required=True)
    parser.add_argument("-n", "--new", action="store_true", help="Ask a new question")
    parser.add_argument(
        "-H", "--history", action="store_true", help="See previous conversations"
    )

    args = parser.parse_args()

    if args.new:
        conversation_id = time.strftime("%Y%m%d%H%M%S")
        engine = SurchEngine(args.user_id, conversation_id)
        print(ascii_art)
        print("Welcome to Surch! Ask me something. (press ctri+c to exit)")
        query = input(">>> ")
        print(engine.first_question(query), "\n")
        while True:
            query = input(">>> ")
            print(engine.follow_up_question(query), "\n")

    elif args.history:
        retrieve_history()


if __name__ == "__main__":
    main()

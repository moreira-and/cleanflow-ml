from bootstrap import initialize_app
from src.application import usecases
import argparse

def parse_args():
    parser = argparse.ArgumentParser(description="cleanflow-ml")
    parser.add_argument("--input", type=str, required=True, help="Input file path")
    return parser.parse_args()

def main():
    initialize_app()

    args = parse_args()
    print(f"Processing input: {args.input}")    


    # keepcoding

if __name__ == "__main__":
    main()









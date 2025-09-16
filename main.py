import argparse
from functions.notebook_processor import process_all_notebooks
from functions.config_reader import read_config

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Notebook Migration Script")
    parser.add_argument(
        "--config",
        type=str,
        required=True,
        help="Path to the configuration JSON file"
    )
    args = parser.parse_args()

    # Load config
    config = read_config(args.config)

    # Pass config into processor
    process_all_notebooks(config)

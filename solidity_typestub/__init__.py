import os.path

from .printer import process_folder, PrintConfig, print_file
import argparse


def main() -> None:

    parser = argparse.ArgumentParser(
        description="Generate python stub files from solidity abi"
    )

    parser.add_argument("files", nargs="+")

    parser.add_argument(
        "-nf", "--no-format", default=False, dest="no_format", action="store_true"
    )
    parser.add_argument("--output", dest="output_folder", type=str, default="artifacts")
    args = parser.parse_args()

    config = PrintConfig(output_folder=args.output_folder, format=not args.no_format)

    for file in args.files:
        if not os.path.exists(file):
            continue
        if os.path.isdir(file):
            process_folder(file, config)
        else:
            print_file(file, config)


if __name__ == "__main__":
    main()

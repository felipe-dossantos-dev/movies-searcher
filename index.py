import argparse
import gc
import sys
from pathlib import Path

from src.indexers import FileIndexer, NGramIndexer


def main():
    parser = argparse.ArgumentParser(
        description="Build and manage search index for text files."
    )
    parser.add_argument(
        "--data-dir",
        type=Path,
        default="./data",
        help="Directory containing text files to be indexed",
    )
    parser.add_argument(
        "--index-dir",
        type=Path,
        default=Path("./index"),
        help="Directory where the index file will be saved (default: ./index)",
    )

    args = parser.parse_args()

    indexer = NGramIndexer(index_dir=args.index_dir, rebuild=True)
    try:
        indexer.build_index(args.data_dir)
        print(f"Index successfully built and saved to {args.index_path}")
        print(f"Total unique words indexed: {len(indexer.get_all_words())}")
    except Exception as e:
        print(f"Error building index: {str(e)}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    gc.disable()
    main()
    gc.enable()

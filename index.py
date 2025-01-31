import argparse
import sys
from pathlib import Path

from src.indexers import FileIndexer


def main():
    parser = argparse.ArgumentParser(
        description="Build and manage search index for text files."
    )
    parser.add_argument(
        "--data-dir",
        type=Path,
        required=True,
        help="Directory containing text files to be indexed",
    )
    parser.add_argument(
        "--index-path",
        type=Path,
        default=Path("index.json"),
        help="Path where the index file will be saved (default: index.json)",
    )
    parser.add_argument(
        "--rebuild",
        action="store_true",
        help="Force rebuild the index even if it already exists",
    )

    args = parser.parse_args()

    if not args.data_dir.exists():
        print(
            f"Error: Data directory '{args.data_dir}' does not exist", file=sys.stderr
        )
        sys.exit(1)

    if not args.data_dir.is_dir():
        print(f"Error: '{args.data_dir}' is not a directory", file=sys.stderr)
        sys.exit(1)

    indexer = FileIndexer(index_path=args.index_path, rebuild=args.rebuild)
    try:
        indexer.build_index(args.data_dir)
        print(f"Index successfully built and saved to {args.index_path}")
        print(f"Total unique words indexed: {len(indexer.get_all_words())}")
    except Exception as e:
        print(f"Error building index: {str(e)}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()

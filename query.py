import argparse
import gc
import sys
from pathlib import Path

from src.indexers import FileIndexer, MemoryIndexer, Indexer
from src.searcher import Searcher


def main():
    parser = argparse.ArgumentParser(description="search for words in text files")
    parser.add_argument("query", help="Search query", nargs="+")
    parser.add_argument(
        "--data-dir", type=Path, default="./data", help="Data directory"
    )
    parser.add_argument(
        "--index-path", type=Path, default="./index/index.json", help="Index Path"
    )
    parser.add_argument(
        "--indexer", 
        choices=["file", "memory"],
        default="file",
        help="Type of indexer to use (file or memory)"
    )

    args = parser.parse_args()

    if not args.data_dir.exists():
        print(f"Error: Directory '{args.data_dir}' does not exist", file=sys.stderr)
        sys.exit(1)

    indexer = build_indexer(args)
    indexer.build_index(args.data_dir)

    searcher = Searcher(indexer)

    query = " ".join(args.query)

    results = searcher.search(query)

    if not results:
        print("No matches found.")
    else:
        print(f"Found {len(results)} matches:")
        for path in results:
            print(f"- {path.name}")

def build_indexer(args) -> Indexer:
    if args.indexer == "file":
        indexer = FileIndexer(args.index_path, False)
    else:
        indexer = MemoryIndexer()
    return indexer


if __name__ == "__main__":
    gc.disable()
    main()
    gc.enable()

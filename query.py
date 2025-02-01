import argparse
import gc
import sys
from pathlib import Path

from src.consts import (
    CLI_ARG_DATA_DIR,
    CLI_ARG_INDEX_DIR,
    CLI_ARG_INDEXER,
    CLI_HELP_DATA_DIR,
    CLI_HELP_DESCRIPTION,
    CLI_HELP_INDEX_DIR,
    CLI_HELP_INDEXER,
    CLI_HELP_QUERY,
    FILES_DEFAULT_DATA_DIR,
    FILES_DEFAULT_INDEX_DIR,
    INDEXER_TYPE_FILE,
    INDEXER_TYPE_MEMORY,
    INDEXER_TYPE_NGRAM,
    MSG_DIR_NOT_EXISTS,
    MSG_FOUND_MATCHES,
    MSG_MATCH_PREFIX,
    MSG_NO_MATCHES,
)
from src.indexers import (
    FileIndexer,
    Indexer,
    MemoryIndexer,
    NGramIndexer,
)
from src.searcher import Searcher


def main():
    parser = argparse.ArgumentParser(description=CLI_HELP_DESCRIPTION)
    parser.add_argument("query", help=CLI_HELP_QUERY, nargs="+")
    parser.add_argument(
        CLI_ARG_DATA_DIR,
        type=Path,
        default=FILES_DEFAULT_DATA_DIR,
        help=CLI_HELP_DATA_DIR,
    )
    parser.add_argument(
        CLI_ARG_INDEXER,
        choices=[
            INDEXER_TYPE_FILE,
            INDEXER_TYPE_MEMORY,
            INDEXER_TYPE_NGRAM,
        ],
        default=INDEXER_TYPE_NGRAM,
        help=CLI_HELP_INDEXER,
    )
    parser.add_argument(
        CLI_ARG_INDEX_DIR,
        type=Path,
        default=FILES_DEFAULT_INDEX_DIR,
        help=CLI_HELP_INDEX_DIR,
    )

    args = parser.parse_args()

    if not args.data_dir.exists():
        print(MSG_DIR_NOT_EXISTS.format(args.data_dir), file=sys.stderr)
        sys.exit(1)

    indexer = build_indexer(args)
    indexer.build_index(args.data_dir)

    searcher = Searcher(indexer)

    query = " ".join(args.query)

    results = searcher.search(query)

    if not results:
        print(MSG_NO_MATCHES)
    else:
        print(MSG_FOUND_MATCHES.format(len(results)))
        for path in results:
            print(MSG_MATCH_PREFIX.format(path.name))


def build_indexer(args) -> Indexer:
    if args.indexer == INDEXER_TYPE_FILE:
        indexer = FileIndexer(args.index_dir, False)
    elif args.indexer == INDEXER_TYPE_NGRAM:
        indexer = NGramIndexer(args.index_dir, False)
    else:
        indexer = MemoryIndexer()
    return indexer


if __name__ == "__main__":
    gc.disable()
    main()
    gc.enable()

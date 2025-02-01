import argparse
import gc
import sys
from pathlib import Path

from src.consts import (
    CLI_ARG_DATA_DIR,
    CLI_ARG_INDEX_DIR,
    FILES_DEFAULT_DATA_DIR,
    FILES_DEFAULT_INDEX_DIR,
    MSG_DATA_DIR_HELP,
    MSG_DESCRIPTION,
    MSG_ERROR,
    MSG_INDEX_DIR_HELP,
    MSG_SUCCESS,
    MSG_TOTAL_WORDS,
)
from src.indexers import FileIndexer, NGramIndexer


def main():
    parser = argparse.ArgumentParser(description=MSG_DESCRIPTION)
    parser.add_argument(
        CLI_ARG_DATA_DIR,
        type=Path,
        default=FILES_DEFAULT_DATA_DIR,
        help=MSG_DATA_DIR_HELP,
    )
    parser.add_argument(
        CLI_ARG_INDEX_DIR,
        type=Path,
        default=Path(FILES_DEFAULT_INDEX_DIR),
        help=MSG_INDEX_DIR_HELP,
    )

    args = parser.parse_args()

    indexer = NGramIndexer(index_dir=args.index_dir, rebuild=True)
    try:
        # TODO - clean all files in folder - files.py
        indexer.build_index(args.data_dir)
        print(MSG_SUCCESS.format(args.index_dir))
        print(MSG_TOTAL_WORDS.format(len(indexer.get_all_words())))
    except Exception as e:
        print(MSG_ERROR.format(str(e)), file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    gc.disable()
    main()
    gc.enable()

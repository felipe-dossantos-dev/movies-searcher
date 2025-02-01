import argparse
import gc
import sys
from pathlib import Path

from src.consts import (
    CLI_ARG_DATA_DIR,
    CLI_ARG_INDEX_DIR,
    CLI_ARG_INDEXER,
    CLI_HELP_INDEXER,
    FILES_DEFAULT_DATA_DIR,
    FILES_DEFAULT_INDEX_DIR,
    INDEXER_TYPE_FILE,
    INDEXER_TYPE_NGRAM,
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
        default=Path(FILES_DEFAULT_DATA_DIR),
        help=MSG_DATA_DIR_HELP,
    )
    parser.add_argument(
        CLI_ARG_INDEX_DIR,
        type=Path,
        default=Path(FILES_DEFAULT_INDEX_DIR),
        help=MSG_INDEX_DIR_HELP,
    )
    parser.add_argument(
        CLI_ARG_INDEXER,
        choices=[INDEXER_TYPE_FILE, INDEXER_TYPE_NGRAM],
        default=INDEXER_TYPE_NGRAM,
        help=CLI_HELP_INDEXER,
    )

    args = parser.parse_args()

    indexer = build_indexer(args)
    try:
        indexer.build_index(args.data_dir)
        print(MSG_SUCCESS.format(args.index_dir))
        print(MSG_TOTAL_WORDS.format(len(indexer.get_all_words())))
    except Exception as e:
        print(MSG_ERROR.format(str(e)), file=sys.stderr)
        sys.exit(1)


def build_indexer(args):
    if args.indexer == INDEXER_TYPE_FILE:
        return FileIndexer(index_dir=args.index_dir, rebuild=True)
    elif args.indexer == INDEXER_TYPE_NGRAM:
        return NGramIndexer(index_dir=args.index_dir, rebuild=True)
    else:
        raise NotImplementedError()


if __name__ == "__main__":
    gc.disable()
    main()
    gc.enable()

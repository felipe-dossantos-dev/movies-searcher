# Files
FILES_DEFAULT_DATA_DIR = "./data"
FILES_DEFAULT_INDEX_DIR = "./index"
FILES_DATA_GLOB_PATTERN = "*.txt"

# Cli
CLI_ARG_INDEX_DIR = "--index-dir"
CLI_ARG_DATA_DIR = "--data-dir"
CLI_ARG_INDEXER = "--indexer"

# Indexer Types
INDEXER_TYPE_FILE = "file"
INDEXER_TYPE_MEMORY = "memory"

# Messages
MSG_NO_MATCHES = "No matches found."
MSG_FOUND_MATCHES = "Found {} matches:"
MSG_DIR_NOT_EXISTS = "Error: Directory '{}' does not exist"
MSG_MATCH_PREFIX = "- {}"
MSG_DESCRIPTION = "Build and manage search index for text files."
MSG_DATA_DIR_HELP = "Directory containing text files to be indexed"
MSG_INDEX_DIR_HELP = "Directory where the index file will be saved (default: ./index)"
MSG_SUCCESS = "Index successfully built and saved to {}"
MSG_TOTAL_WORDS = "Total unique words indexed: {}"
MSG_ERROR = "Error building index: {}"

# CLI Help Messages
CLI_HELP_DESCRIPTION = "search for words in text files"
CLI_HELP_QUERY = "Search query"
CLI_HELP_DATA_DIR = "Data directory"
CLI_HELP_INDEX_DIR = "Index Directory"
CLI_HELP_INDEXER = "Type of indexer to use (file or memory)"

# NGram
NGRAM_DEFAULT_SIZE = 3
NGRAM_FILE_EXTENSION = ".ngram.pickle"
NGRAM_FILE_PATTERN = f"*{NGRAM_FILE_EXTENSION}"

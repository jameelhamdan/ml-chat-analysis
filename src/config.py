import os

DATA_FILE = './data/dataset.jsonl'
OUT_DIR = './out'
OPENAI_API_KEY = os.getenv('OPENAI_API_KEY', '')
OPENAI_API_MODEL = 'gpt-4o-mini'
# Read output data from file instead of analysing it everytime
ANALYTICS_FILENAME = os.getenv('ANALYTICS_FILENAME', '')

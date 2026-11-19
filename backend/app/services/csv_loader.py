# ---------------------------------------utils--------------------
import os
import psutil


def log_memory(label):
    process = psutil.Process(os.getpid())
    memory = process.memory_info()

    print(f"[{label}] RSS: {memory.rss / 1024**2:.2f} MB")


# ---------------------------------------utils--------------------

log_memory("Application startup csv_loader.py")


import pandas as pd
from pathlib import Path


BASE_DIR = Path(__file__).resolve().parents[3]
CSV_PATH = BASE_DIR / "data" / "movies(stemd).csv"

movies_df = pd.read_csv(CSV_PATH, index_col="tmdb_id")
log_memory("After movies.csv")

# print(movies_df.info(memory_usage="deep"))
# print(movies_df.memory_usage(deep=True).sort_values(ascending=False))

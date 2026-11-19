import os
import psutil
import sys

process = psutil.Process(os.getpid())


def report(label):
    mem = process.memory_full_info()

    print(f"\n{'=' * 45}")
    print(label)
    print(f"RSS : {mem.rss / 1024**2:.2f} MB")
    print(f"USS : {mem.uss / 1024**2:.2f} MB")
    print(f"PSS : {mem.pss / 1024**2:.2f} MB")
    print("=" * 45)


report("Python startup")

# Import your actual application modules
from app.services.csv_loader import movies_df

report("After CSV loader")

from app.services.recommender import X, TMDB_IDS, tmdb_to_index

report("After recommender")


# DataFrame memory
print("\n--- PANDAS ---")
print(
    movies_df
    .memory_usage(deep=True)
    .sort_values(ascending=False)
    .map(lambda x: f"{x / 1024**2:.2f} MB")
)

print("DataFrame total:", f"{movies_df.memory_usage(deep=True).sum() / 1024**2:.2f} MB")


# CSR matrix memory
print("\n--- CSR MATRIX ---")
print("Shape:", X.shape)
print("Non-zero elements:", X.nnz)
print("Data:", X.data.nbytes / 1024**2, "MB")
print("Indices:", X.indices.nbytes / 1024**2, "MB")
print("Indptr:", X.indptr.nbytes / 1024**2, "MB")

csr_total = X.data.nbytes + X.indices.nbytes + X.indptr.nbytes

print("CSR total:", csr_total / 1024**2, "MB")


# NumPy
print("\n--- NUMPY ---")
print("TMDB IDs:", TMDB_IDS.nbytes / 1024**2, "MB")


# Python dictionary
print("\n--- PYTHON DICTIONARY ---")
print("Entries:", len(tmdb_to_index))
print("Shallow size:", sys.getsizeof(tmdb_to_index) / 1024**2, "MB")

report("Final memory")

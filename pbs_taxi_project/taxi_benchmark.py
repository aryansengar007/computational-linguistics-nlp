import pandas as pd
import time
import os

DATASET = "yellow_tripdata_2024-01.parquet"

print("=" * 60)
print("NYC YELLOW TAXI DATA CLEANING BENCHMARK")
print("=" * 60)

# ---------------------------------------------------------
# 1. TOTAL START TIME
# ---------------------------------------------------------
total_start = time.perf_counter()

# ---------------------------------------------------------
# 2. LOAD DATASET
# ---------------------------------------------------------
start = time.perf_counter()

df = pd.read_parquet(DATASET)

load_time = time.perf_counter() - start

print("\nDataset loaded successfully.")
print(f"Rows    : {len(df):,}")
print(f"Columns : {len(df.columns)}")
print(f"Load Time: {load_time:.4f} seconds")


# ---------------------------------------------------------
# 3. BASIC DATA INFORMATION
# ---------------------------------------------------------
start = time.perf_counter()

print("\n--- Dataset Information ---")

print("\nColumns:")
print(df.columns.tolist())

print("\nMissing values:")
print(df.isnull().sum())

missing_time = time.perf_counter() - start

print(f"\nMissing-value analysis time: {missing_time:.4f} seconds")


# ---------------------------------------------------------
# 4. REMOVE DUPLICATES
# ---------------------------------------------------------
start = time.perf_counter()

before_duplicates = len(df)

df = df.drop_duplicates()

after_duplicates = len(df)

duplicate_time = time.perf_counter() - start

print("\n--- Duplicate Removal ---")
print(f"Rows before : {before_duplicates:,}")
print(f"Rows after  : {after_duplicates:,}")
print(f"Duplicates removed: {before_duplicates - after_duplicates:,}")
print(f"Duplicate removal time: {duplicate_time:.4f} seconds")


# ---------------------------------------------------------
# 5. HANDLE MISSING VALUES
# ---------------------------------------------------------
start = time.perf_counter()

numeric_columns = df.select_dtypes(
    include=["number"]
).columns

for column in numeric_columns:
    df[column] = df[column].fillna(df[column].median())

categorical_columns = df.select_dtypes(
    include=["object", "string"]
).columns

for column in categorical_columns:
    df[column] = df[column].fillna("Unknown")

missing_clean_time = time.perf_counter() - start

print("\n--- Missing Value Handling ---")
print(f"Numeric columns processed    : {len(numeric_columns)}")
print(f"Categorical columns processed: {len(categorical_columns)}")
print(
    f"Missing-value cleaning time: "
    f"{missing_clean_time:.4f} seconds"
)


# ---------------------------------------------------------
# 6. CONVERT DATE/TIME COLUMNS
# ---------------------------------------------------------
start = time.perf_counter()

datetime_columns = [
    "tpep_pickup_datetime",
    "tpep_dropoff_datetime"
]

for column in datetime_columns:
    if column in df.columns:
        df[column] = pd.to_datetime(
            df[column],
            errors="coerce"
        )

datetime_time = time.perf_counter() - start

print("\n--- Date/Time Conversion ---")
print(f"Date/time conversion time: {datetime_time:.4f} seconds")


# ---------------------------------------------------------
# 7. REMOVE INVALID VALUES
# ---------------------------------------------------------
start = time.perf_counter()

if "trip_distance" in df.columns:
    df = df[df["trip_distance"] > 0]

if "fare_amount" in df.columns:
    df = df[df["fare_amount"] >= 0]

if "passenger_count" in df.columns:
    df = df[
        (df["passenger_count"] > 0) &
        (df["passenger_count"] <= 10)
    ]

invalid_time = time.perf_counter() - start

print("\n--- Invalid Value Removal ---")
print(f"Rows after validation: {len(df):,}")
print(f"Invalid-value cleaning time: {invalid_time:.4f} seconds")


# ---------------------------------------------------------
# 8. CREATE TRIP DURATION
# ---------------------------------------------------------
start = time.perf_counter()

if (
    "tpep_pickup_datetime" in df.columns
    and "tpep_dropoff_datetime" in df.columns
):
    df["trip_duration_minutes"] = (
        df["tpep_dropoff_datetime"]
        - df["tpep_pickup_datetime"]
    ).dt.total_seconds() / 60

    df = df[
        (df["trip_duration_minutes"] > 0) &
        (df["trip_duration_minutes"] <= 24 * 60)
    ]

duration_time = time.perf_counter() - start

print("\n--- Trip Duration Processing ---")
print(f"Rows after duration filtering: {len(df):,}")
print(f"Duration processing time: {duration_time:.4f} seconds")


# ---------------------------------------------------------
# 9. SAVE CLEAN DATASET
# ---------------------------------------------------------
start = time.perf_counter()

output_file = "yellow_taxi_cleaned.parquet"

df.to_parquet(
    output_file,
    index=False
)

save_time = time.perf_counter() - start

print("\n--- Output ---")
print(f"Cleaned dataset: {output_file}")
print(f"Save time: {save_time:.4f} seconds")


# ---------------------------------------------------------
# 10. TOTAL EXECUTION TIME
# ---------------------------------------------------------
total_time = time.perf_counter() - total_start

print("\n" + "=" * 60)
print("FINAL BENCHMARK RESULTS")
print("=" * 60)

print(f"Load Time                  : {load_time:.4f} sec")
print(f"Missing Analysis Time      : {missing_time:.4f} sec")
print(f"Duplicate Removal Time     : {duplicate_time:.4f} sec")
print(f"Missing Value Cleaning     : {missing_clean_time:.4f} sec")
print(f"Date/Time Conversion       : {datetime_time:.4f} sec")
print(f"Invalid Value Cleaning     : {invalid_time:.4f} sec")
print(f"Trip Duration Processing   : {duration_time:.4f} sec")
print(f"Save Time                  : {save_time:.4f} sec")
print("-" * 60)
print(f"TOTAL EXECUTION TIME       : {total_time:.4f} sec")
print("=" * 60)

# Save timing results
with open("benchmark_results.txt", "w") as f:
    f.write("NYC Yellow Taxi Benchmark\n")
    f.write("=========================\n")
    f.write(f"Rows processed: {len(df):,}\n")
    f.write(f"Load Time: {load_time:.4f} sec\n")
    f.write(f"Missing Analysis Time: {missing_time:.4f} sec\n")
    f.write(f"Duplicate Removal Time: {duplicate_time:.4f} sec\n")
    f.write(f"Missing Value Cleaning: {missing_clean_time:.4f} sec\n")
    f.write(f"Date/Time Conversion: {datetime_time:.4f} sec\n")
    f.write(f"Invalid Value Cleaning: {invalid_time:.4f} sec\n")
    f.write(f"Trip Duration Processing: {duration_time:.4f} sec\n")
    f.write(f"Save Time: {save_time:.4f} sec\n")
    f.write(f"TOTAL TIME: {total_time:.4f} sec\n")

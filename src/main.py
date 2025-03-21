import math
import concurrent.futures
from collections import defaultdict

def process_chunk(lines):
    stats = defaultdict(lambda: {"min": float("inf"), "max": float("-inf"), "sum": 0.0, "count": 0})
    for line in lines:
        parts = line.rstrip("\n").split(";")
        if len(parts) < 2:
            continue
        key = parts[0]
        try:
            value = float(parts[1])
        except ValueError:
            continue
        stats[key]["min"] = min(stats[key]["min"], value)
        stats[key]["max"] = max(stats[key]["max"], value)
        stats[key]["sum"] += value
        stats[key]["count"] += 1
    return stats

def merge_stats(stats1, stats2):
    for key, data in stats2.items():
        if key in stats1:
            stats1[key]["min"] = min(stats1[key]["min"], data["min"])
            stats1[key]["max"] = max(stats1[key]["max"], data["max"])
            stats1[key]["sum"] += data["sum"]
            stats1[key]["count"] += data["count"]
        else:
            stats1[key] = data
    return stats1

def main(input_file_name="testcase.txt", output_file_name="output.txt", num_workers=4, chunk_size=10000):
    with open(input_file_name, "r") as infile:
        lines = infile.readlines()
    chunks = [lines[i:i+chunk_size] for i in range(0, len(lines), chunk_size)]
    stats = defaultdict(lambda: {"min": float("inf"), "max": float("-inf"), "sum": 0.0, "count": 0})
    with concurrent.futures.ThreadPoolExecutor(max_workers=num_workers) as executor:
        for partial_stats in executor.map(process_chunk, chunks):
            stats = merge_stats(stats, partial_stats)
    with open(output_file_name, "w") as outfile:
        for key in sorted(stats.keys()):
            if stats[key]["count"] > 0:
                mean_value = stats[key]["sum"] / stats[key]["count"]
                min_temp = math.ceil(stats[key]["min"] * 10) / 10
                mean_temp = math.ceil(mean_value * 10) / 10
                max_temp = math.ceil(stats[key]["max"] * 10) / 10
                outfile.write(f"{key}={min_temp}/{mean_temp}/{max_temp}\n")

if __name__ == "__main__":
    main()

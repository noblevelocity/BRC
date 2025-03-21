import math
from collections import defaultdict

def main(input_file_name="testcase.txt", output_file_name="output.txt"):
    stats = defaultdict(lambda: {"min": float("inf"), "max": float("-inf"), "sum": 0.0, "count": 0})
    
    with open(input_file_name, "r") as infile:
        for line in infile:
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

    with open(output_file_name, "w") as outfile:
        for key in sorted(stats.keys()):
            mean_value = stats[key]["sum"] / stats[key]["count"]
            min_temp = math.ceil(stats[key]["min"] * 10) / 10
            mean_temp = math.ceil(mean_value * 10) / 10
            max_temp = math.ceil(stats[key]["max"] * 10) / 10
            outfile.write(f"{key}={min_temp}/{mean_temp}/{max_temp}\n")

if __name__ == "__main__":
    main()

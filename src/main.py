from collections import defaultdict

def process_file(input_file="testcase.txt", output_file="output.txt"):
    city_data = defaultdict(lambda: [float('inf'), 0, float('-inf'), 0])  # min, sum, max, count
    
    with open(input_file, "r") as f:
        for line in f:
            city, score = line.strip().split(";")
            score = float(score)
            
            city_stats = city_data[city]
            city_stats[0] = min(city_stats[0], score)  # min
            city_stats[1] += score                     # sum
            city_stats[2] = max(city_stats[2], score)  # max
            city_stats[3] += 1                         # count
    
    with open(output_file, "w") as f:
        for city in sorted(city_data.keys()):
            min_val, total, max_val, count = city_data[city]
            mean_val = total / count
            f.write(f"{city}={min_val:.1f}/{mean_val:.1f}/{max_val:.1f}\n")

if __name__ == "__main__":
    process_file()

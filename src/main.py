import math

def main(input_file_name="testcase.txt", output_file_name="output.txt"):
    min_values = {}
    max_values = {}
    sums = {}
    counts = {}
    
    with open(input_file_name, "r") as f:
        lines = f.readlines()
    
    for line in lines:
        parts = line.strip().split(';', 1)
        key = parts[0]
        value = float(parts[1])
        
        try:
            if value < min_values[key]: min_values[key] = value
        except: min_values[key] = value
        
        try:
            if value > max_values[key]: max_values[key] = value
        except: max_values[key] = value
        
        try:
            sums[key] += value
            counts[key] += 1
        except:
            sums[key] = value
            counts[key] = 1
    
    results = []
    for key in sorted(min_values):
        min_t = math.ceil(min_values[key] * 10) / 10
        mean_t = math.ceil((sums[key] / counts[key]) * 10) / 10
        max_t = math.ceil(max_values[key] * 10) / 10
        results.append(f"{key}={min_t}/{mean_t}/{max_t}\n")
    
    with open(output_file_name, "w") as f:
        f.writelines(results)

if __name__ == "__main__":
    main()
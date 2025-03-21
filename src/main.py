import math

def main(input_file_name="testcase.txt", output_file_name="output.txt"):
    min_values = {}
    max_values = {}
    sums = {}
    counts = {}
    
    with open(input_file_name, "r") as input_file:
        for line in input_file:
            key, value_str = line.strip().split(';', 1)
            value = float(value_str)
            
            try:
                if value < min_values[key]:
                    min_values[key] = value
            except KeyError:
                min_values[key] = value
                
            try:
                if value > max_values[key]:
                    max_values[key] = value
            except KeyError:
                max_values[key] = value
                
            try:
                sums[key] += value
                counts[key] += 1
            except KeyError:
                sums[key] = value
                counts[key] = 1
    
    sorted_keys = sorted(min_values.keys())
    
    results = []
    for key in sorted_keys:
        min_temp = math.ceil(min_values[key] * 10) / 10
        mean_temp = math.ceil((sums[key] / counts[key]) * 10) / 10
        max_temp = math.ceil(max_values[key] * 10) / 10
        results.append(f"{key}={min_temp}/{mean_temp}/{max_temp}\n")
    
    with open(output_file_name, "w") as output_file:
        output_file.writelines(results)

if __name__ == "__main__":
    main()
import math
import concurrent.futures
import os

def process_chunk(chunk_lines):
    local_min = {}
    local_max = {}
    local_sums = {}
    local_counts = {}
    
    for line in chunk_lines:
        parts = line.strip().split(';', 1)
        if len(parts) != 2:
            continue
            
        key = parts[0]
        try:
            value = float(parts[1])
        except ValueError:
            continue
            
        try:
            if value < local_min[key]: local_min[key] = value
        except KeyError:
            local_min[key] = value
        
        try:
            if value > local_max[key]: local_max[key] = value
        except KeyError:
            local_max[key] = value
        
        try:
            local_sums[key] += value
            local_counts[key] += 1
        except KeyError:
            local_sums[key] = value
            local_counts[key] = 1
            
    return local_min, local_max, local_sums, local_counts

def merge_results(results):
    final_min = {}
    final_max = {}
    final_sums = {}
    final_counts = {}
    
    for min_dict, max_dict, sums_dict, counts_dict in results:
        for key, value in min_dict.items():
            if key in final_min:
                final_min[key] = min(final_min[key], value)
            else:
                final_min[key] = value
                
        for key, value in max_dict.items():
            if key in final_max:
                final_max[key] = max(final_max[key], value)
            else:
                final_max[key] = value
                
        for key, value in sums_dict.items():
            final_sums[key] = final_sums.get(key, 0) + value
            final_counts[key] = final_counts.get(key, 0) + counts_dict[key]
            
    return final_min, final_max, final_sums, final_counts

def main(input_file_name="testcase.txt", output_file_name="output.txt", num_workers=4):
    with open(input_file_name, "r") as f:
        all_lines = f.readlines()
    
    total_lines = len(all_lines)
    chunk_size = max(1, total_lines // num_workers)
    
    chunks = [all_lines[i:i + chunk_size] for i in range(0, total_lines, chunk_size)]
    
    results = []
    with concurrent.futures.ThreadPoolExecutor(max_workers=num_workers) as executor:
        futures = [executor.submit(process_chunk, chunk) for chunk in chunks]
        for future in concurrent.futures.as_completed(futures):
            results.append(future.result())
    
    min_values, max_values, sums, counts = merge_results(results)
    
    output_lines = []
    for key in sorted(min_values.keys()):
        min_temp = math.ceil(min_values[key] * 10) / 10
        mean_temp = math.ceil((sums[key] / counts[key]) * 10) / 10
        max_temp = math.ceil(max_values[key] * 10) / 10
        output_lines.append(f"{key}={min_temp}/{mean_temp}/{max_temp}\n")
    
    with open(output_file_name, "w") as f:
        f.writelines(output_lines)

if __name__ == "__main__":
    main(num_workers=4)
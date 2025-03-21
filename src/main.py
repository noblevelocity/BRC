import math
import concurrent.futures
from concurrent.futures import ThreadPoolExecutor

def process_chunk(lines_chunk):
    local_min = {}
    local_max = {}
    local_sum = {}  # key: (sum, count)
    for line in lines_chunk:
        li = line.strip().split(';')
        if len(li) != 2:
            continue
        key, value_str = li
        try:
            value = float(value_str)
        except ValueError:
            continue
        # Update local_min
        if key in local_min:
            if value < local_min[key]:
                local_min[key] = value
        else:
            local_min[key] = value
        # Update local_max
        if key in local_max:
            if value > local_max[key]:
                local_max[key] = value
        else:
            local_max[key] = value
        # Update local_sum
        if key in local_sum:
            local_sum[key] = (local_sum[key][0] + value, local_sum[key][1] + 1)
        else:
            local_sum[key] = (value, 1)
    return (local_min, local_max, local_sum)

def main(input_file_name="testcase.txt", output_file_name="output.txt"):
    # Read all lines from the input file
    with open(input_file_name, "r") as input_file:
        lines = input_file.readlines()
    
    # Determine the number of chunks (adjust based on system capabilities)
    num_threads = 4  # This can be adjusted to the number of available CPU cores
    chunk_size = (len(lines) + num_threads - 1) // num_threads
    chunks = [lines[i:i + chunk_size] for i in range(0, len(lines), chunk_size)]
    
    # Process each chunk in parallel using ThreadPoolExecutor
    with ThreadPoolExecutor(max_workers=num_threads) as executor:
        futures = [executor.submit(process_chunk, chunk) for chunk in chunks]
        results = [future.result() for future in concurrent.futures.as_completed(futures)]
    
    # Merge results from all chunks
    global_min = {}
    global_max = {}
    global_sum = {}
    
    for local_min, local_max, local_sum in results:
        # Merge minimum values
        for key, val in local_min.items():
            if key in global_min:
                if val < global_min[key]:
                    global_min[key] = val
            else:
                global_min[key] = val
        # Merge maximum values
        for key, val in local_max.items():
            if key in global_max:
                if val > global_max[key]:
                    global_max[key] = val
            else:
                global_max[key] = val
        # Merge sum and count values
        for key, (sum_val, count) in local_sum.items():
            if key in global_sum:
                global_sum[key] = (global_sum[key][0] + sum_val, global_sum[key][1] + count)
            else:
                global_sum[key] = (sum_val, count)
    
    # Calculate the mean values
    global_mean = {key: (sum_val / count) for key, (sum_val, count) in global_sum.items()}
    
    # Write the results to the output file
    with open(output_file_name, "w") as output_file:
        for key in sorted(global_min.keys()):
            min_temp = math.ceil(global_min[key] * 10) / 10
            mean_temp = math.ceil(global_mean[key] * 10) / 10
            max_temp = math.ceil(global_max[key] * 10) / 10
            output_file.write(f"{key}={min_temp}/{mean_temp}/{max_temp}\n")

if __name__ == "__main__":
    main()
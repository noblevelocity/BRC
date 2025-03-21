import math
import concurrent.futures
import multiprocessing
import os
import mmap

def process_chunk(file_path, start_pos, end_pos):
    local_min = {}
    local_max = {}
    local_sums = {}
    local_counts = {}
    
    with open(file_path, 'r') as f:
        with mmap.mmap(f.fileno(), 0, access=mmap.ACCESS_READ) as mm:
            mm.seek(start_pos)
            
            current_pos = start_pos
            while current_pos < end_pos:
                line = mm.readline()
                current_pos = mm.tell()
                
                if not line:
                    break
                    
                try:
                    parts = line.decode().strip().split(';', 1)
                    key = parts[0]
                    value = float(parts[1])
                    
                    if key in local_min:
                        if value < local_min[key]:
                            local_min[key] = value
                    else:
                        local_min[key] = value
                        
                    if key in local_max:
                        if value > local_max[key]:
                            local_max[key] = value
                    else:
                        local_max[key] = value
                        
                    if key in local_sums:
                        local_sums[key] += value
                        local_counts[key] += 1
                    else:
                        local_sums[key] = value
                        local_counts[key] = 1
                except:
                    continue
    
    return local_min, local_max, local_sums, local_counts

def get_file_chunks(file_path, num_chunks):
    file_size = os.path.getsize(file_path)
    chunk_size = file_size // num_chunks
    
    chunks = []
    with open(file_path, 'r') as f:
        with mmap.mmap(f.fileno(), 0, access=mmap.ACCESS_READ) as mm:
            for i in range(num_chunks):
                start_pos = i * chunk_size
                
                end_pos = file_size if i == num_chunks - 1 else (i + 1) * chunk_size
                
                if i < num_chunks - 1:
                    mm.seek(end_pos)
                    mm.readline()
                    end_pos = mm.tell()
                
                chunks.append((start_pos, end_pos))
    
    return chunks

def main(input_file="testcase.txt", output_file="output.txt"):
    num_workers = min(4, multiprocessing.cpu_count())
    
    chunks = get_file_chunks(input_file, num_workers)
    
    results = []
    with concurrent.futures.ProcessPoolExecutor(max_workers=num_workers) as executor:
        futures = [executor.submit(process_chunk, input_file, start, end) for start, end in chunks]
        for future in concurrent.futures.as_completed(futures):
            results.append(future.result())
    
    min_values = {}
    max_values = {}
    sum_values = {}
    count_values = {}
    
    for mins, maxs, sums, counts in results:
        for key, value in mins.items():
            min_values[key] = min(min_values.get(key, float('inf')), value)
            
        for key, value in maxs.items():
            max_values[key] = max(max_values.get(key, float('-inf')), value)
            
        for key, value in sums.items():
            sum_values[key] = sum_values.get(key, 0) + value
            count_values[key] = count_values.get(key, 0) + counts[key]
    
    with open(output_file, 'w') as f:
        for key in sorted(min_values.keys()):
            min_temp = math.ceil(min_values[key] * 10) / 10
            mean_temp = math.ceil((sum_values[key] / count_values[key]) * 10) / 10
            max_temp = math.ceil(max_values[key] * 10) / 10
            f.write(f"{key}={min_temp}/{mean_temp}/{max_temp}\n")

if __name__ == "__main__":
    main()
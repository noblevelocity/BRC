import math
import concurrent.futures
import multiprocessing
import os
import mmap
import array

def process_chunk(file_path, start_pos, end_pos):
    results = {}
    
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
                    
                    if key in results:
                        # Array structure: [min, max, sum, count]
                        if value < results[key][0]:
                            results[key][0] = value
                        if value > results[key][1]:
                            results[key][1] = value
                        results[key][2] += value
                        results[key][3] += 1
                    else:
                        # Initialize with [min, max, sum, count]
                        results[key] = [value, value, value, 1]
                except:
                    continue
    
    return results

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
    
    merged = {}
    for result_dict in results:
        for key, values in result_dict.items():
            if key in merged:
                # [min, max, sum, count]
                merged[key][0] = min(merged[key][0], values[0])
                merged[key][1] = max(merged[key][1], values[1])
                merged[key][2] += values[2]
                merged[key][3] += values[3]
            else:
                merged[key] = values.copy()
    
    with open(output_file, 'w') as f:
        for key in sorted(merged.keys()):
            min_temp = math.ceil(merged[key][0] * 10) / 10
            mean_temp = math.ceil((merged[key][2] / merged[key][3]) * 10) / 10
            max_temp = math.ceil(merged[key][1] * 10) / 10
            f.write(f"{key}={min_temp}/{mean_temp}/{max_temp}\n")

if __name__ == "__main__":
    main()
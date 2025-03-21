import math

def main(input_file_name="testcase.txt", output_file_name="output.txt"):
    input_file = open(input_file_name, "r")
    output_file = open(output_file_name, "w")
    minmap = {}
    maxmap = {}
    meanmap = {}
    for line in input_file:
        li = line.strip().split(';')
        key, value = li[0], float(li[1])
        if key in minmap:
            minmap[key] = min(minmap[key], value)
        else:
            minmap[key] = value
        if key in maxmap:
            maxmap[key] = max(maxmap[key], value)
        else:
            maxmap[key] = value
        if key in meanmap:
            meanmap[key][0] += value
            meanmap[key][1] += 1
        else:
            meanmap[key] = [value, 1]
    for key in meanmap:
        meanmap[key] = meanmap[key][0] / meanmap[key][1]
    for key in sorted(minmap.keys()):
        min_temp = math.ceil(minmap[key] * 10) / 10
        mean_temp = math.ceil(meanmap[key] * 10) / 10
        max_temp = math.ceil(maxmap[key] * 10) / 10
        output_file.write(f"{key}={min_temp}/{mean_temp}/{max_temp}\n")
    output_file.close()
    input_file.close()
if __name__ == "__main__":
    main()
"""
CSCI 570 - Sequence Alignment Project
Basic Algorithm Implementation (Dynamic Programming)
"""
import os.path
import sys
import time
import psutil
from pathlib import Path

# Constants
DELTA = 30
ALPHA = {
    ('A', 'A'): 0, ('A', 'C'): 110, ('A', 'G'): 48, ('A', 'T'): 94,
    ('C', 'A'): 110, ('C', 'C'): 0, ('C', 'G'): 118, ('C', 'T'): 48,
    ('G', 'A'): 48, ('G', 'C'): 118, ('G', 'G'): 0, ('G', 'T'): 110,
    ('T', 'A'): 94, ('T', 'C'): 48, ('T', 'G'): 110, ('T', 'T'): 0
}
input_dir = Path("CSCI570_Project_Minimum_Jul_14/SampleTestCases")

def generate_string(base_string, indices):
    """
    Args:
        base_string (str): The initial base string
        indices (list): List of indices where insertions occur
    Returns:
        str: Final generated string after all insertions
    """
    for i in indices:
        first_part = base_string[:i + 1]
        second_part = base_string[i + 1:]
        base_string = first_part + base_string + second_part

    result = base_string

    return result


def parse_input_file(file_path):
    """
    Args:
        file_path (str): the input path of the file
    Returns:
        tuple: (string1, string2) - the two generated strings
    """
    # pattern = re.compile(r"^input\d+.*$")
    # IMPLEMENT THIS LOOP IN THE UNIT TEST FUNCTION
    # target_files = [file_path for file_path in input_dir.iterdir() if file_path.is_file() and pattern.match(file_path.name)]
    # for file_path in target_files:
    with open(file_path, 'r') as f:
        lines = [line.strip() for line in f.readlines() if line.strip()]

    string1 = lines[0]
    idx=1

    indices1 = []
    while lines[idx].isdigit():
        indices1.append(int(lines[idx]))
        idx += 1

    string2 = lines[idx]
    idx += 1

    indices2 = []
    while idx < len(lines):
        indices2.append(int(lines[idx]))
        idx += 1

    output_string1 = generate_string(string1, indices1)
    output_string2 = generate_string(string2, indices2)

    return output_string1, output_string2


def sequence_alignment(X, Y, delta, alpha):
    """
    Perform sequence alignment using dynamic programming.
    Args:
        X (str): First string
        Y (str): Second string
        delta (int): Gap penalty
        alpha (dict): Dictionary of mismatch costs

    Returns:
        tuple: (cost, aligned_X, aligned_Y)
            - cost: Minimum alignment cost
            - aligned_X: First string
            - aligned_Y: Second string
    """
    m, n = len(X), len(Y)

    dp = [[0] * (n + 1) for _ in range(m+1)]

    for i in range(m+1):
        dp[i][0] = i * delta

    for j in range(n+1):
        dp[0][j] = j * delta

    for i in range(1,m+1):
        for j in range(1, n+1):
            dp[i][j] = min(dp[i-1][j-1] + alpha[X[i-1], Y[j-1]],
                           dp[i-1][j] + delta,
                           dp[j-1][i] + delta)

    minimum_alignment_cost = dp[m][n]
    aligned_x = []
    aligned_y = []


    for i in reversed(range(m, 1)):
        for j in reversed(range(n, 1)):
            if dp[i][j] == dp[i-1][j-1] + alpha[X[i-1], Y[j-1]]:
                aligned_x.append(X[i-1])
                aligned_y.append(Y[j-1])

            elif dp[i][j] == dp[i-1][j] + delta:
                aligned_x.append(X[i-1])
                aligned_y.append(('_'))

            else:
                aligned_x.append('_')
                aligned_y.append(Y[j-1])

    aligned_x.reverse()
    aligned_y.reverse()

    return minimum_alignment_cost, aligned_x, aligned_y


def calculate_alignment_cost(aligned1, aligned2, delta, alpha):
    """
    Args:
        aligned1 (str): First aligned string
        aligned2 (str): Second aligned string
        delta (int): Gap penalty
        alpha (dict): Dictionary of mismatch costs
    Returns:
        int: Total alignment cost
    """
    cost = 0

    for i in range(len(aligned1)):
        if aligned1[i] == '_' or aligned2[i] == '_':
            cost += delta
        else:
            cost += alpha[aligned1[i], aligned2[i]]
    return cost


def process_memory():
    process = psutil.Process()
    memory_info = process.memory_info()
    memory_consumed = int(memory_info.rss / 1024)
    return memory_consumed


def format_output(file_name, output_path, cost, aligned1, aligned2, time_ms, memory_kb):
    if not os.path.exists(output_path):
        os.makedirs(output_path)

    file_path = os.path.join(output_path, file_name+".txt")
    with open(file_path, "w") as f:
        f.write(str(cost))
        f.write(aligned1)
        f.write(aligned2)
        f.write(str(time_ms))
        f.write(str(memory_kb))

    pass


def main():
    """
    Main function to run the alignment algorithm.

    TODO: Implement the main workflow:
    1. Parse command line arguments
    2. Read and parse input file
    3. Measure time and memory
    4. Run alignment algorithm
    5. Write output file
    """

    # TODO: Check command line arguments
    # Should be: python basic.py <input_file> <output_file>

    # TODO: Parse input file to get the two strings

    # TODO: Measure start time
    start_time = time.time()

    # TODO: Run sequence alignment

    # TODO: Measure end time
    end_time = time.time()
    time_ms = (end_time - start_time) * 1000
    # TODO: Get memory usage
    memory = process_memory()

    # TODO: Write output to file

    pass


if __name__ == "__main__":
    main()
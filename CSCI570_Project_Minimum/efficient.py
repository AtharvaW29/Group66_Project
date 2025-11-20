import os.path
import sys
import time
import psutil
import math
from pathlib import Path

# Constants
DELTA = 30
ALPHA = {
    ('A', 'A'): 0, ('A', 'C'): 110, ('A', 'G'): 48, ('A', 'T'): 94,
    ('C', 'A'): 110, ('C', 'C'): 0, ('C', 'G'): 118, ('C', 'T'): 48,
    ('G', 'A'): 48, ('G', 'C'): 118, ('G', 'G'): 0, ('G', 'T'): 110,
    ('T', 'A'): 94, ('T', 'C'): 48, ('T', 'G'): 110, ('T', 'T'): 0
}


# input_dir = Path("CSCI570_Project_Minimum_Jul_14/SampleTestCases")

def generate_string(base_string, indices) -> str:
    for i in indices:
        first_part = base_string[:i + 1]
        second_part = base_string[i + 1:]
        base_string = first_part + base_string + second_part

    result = base_string

    return result


def parse_input_file(file_path) -> tuple[str, str]:
    with open(file_path, 'r') as f:
        lines = [line.strip() for line in f.readlines() if line.strip()]

    string1 = lines[0]
    idx = 1

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

def original_sequence_alignment(X, Y, delta, alpha) -> tuple[int, str, str]:
    """
    Perform sequence alignment using dynamic programming.
    Traceback priority: diagonal > left > up [Bois this should be same for all]
    """
    m, n = len(X), len(Y)

    dp = [[0] * (n + 1) for _ in range(m + 1)]

    # base cases
    for i in range(m + 1):
        dp[i][0] = i * delta

    for j in range(n + 1):
        dp[0][j] = j * delta

    # dp table
    for i in range(1, m + 1):
        for j in range(1, n + 1):

            dp[i][j] = min(dp[i - 1][j - 1] + alpha[X[i - 1], Y[j - 1]],
                           dp[i - 1][j] + delta,
                           dp[i][j - 1] + delta)

    minimum_alignment_cost = dp[m][n]

    aligned_x = []
    aligned_y = []

    i, j = m, n
    while i > 0 or j > 0:
        if i == 0:
            aligned_x.append('_')
            aligned_y.append(Y[j - 1])
            j -= 1
        elif j == 0:
            aligned_x.append(X[i - 1])
            aligned_y.append('_')
            i -= 1
        else:
            match_cost = dp[i - 1][j - 1] + alpha[X[i - 1], Y[j - 1]]
            insert_cost = dp[i][j - 1] + delta

            # Diagonal
            if dp[i][j] == match_cost:
                aligned_x.append(X[i - 1])
                aligned_y.append(Y[j - 1])
                i -= 1
                j -= 1
            # Left
            elif dp[i][j] == insert_cost:
                aligned_x.append('_')
                aligned_y.append(Y[j - 1])
                j -= 1
            # Up
            else:
                aligned_x.append(X[i - 1])
                aligned_y.append('_')
                i -= 1

    aligned_x.reverse()
    aligned_y.reverse()

    return minimum_alignment_cost, ''.join(aligned_x), ''.join(aligned_y)


# This funciton is to find the best scores between X and all prefixes of Y


def sequence_alignment(X, Y, delta, alpha,flag) -> list[int]:
    """
    Perform sequence alignment using dynamic programming.
    Just returns the minimum alignment cost.
    flag:
        0 is to find the best scores between X and all prefixes of Y
        1 is to find the best scores between X and all suffixes of Y
    """
    m, n = len(X), len(Y)

    dp = [[0] * (n + 1) for _ in range(2)]

    # base cases

    dp[0][0] = 0

    for j in range(n + 1):
        dp[0][j] = j * delta

    # dp table
    for i in range(1, m + 1):
        dp[i%2][0] = i * delta
        for j in range(1, n + 1):
            if flag==0:
                dp[i%2][j] = min(dp[(i-1)%2][j - 1] + alpha[X[i - 1], Y[j - 1]],
                               dp[(i-1)%2][j] + delta,
                               dp[i%2][j - 1] + delta)
            else:
                # X[m - i], Y[n - j] means we are aligning reversed strings
                dp[i%2][j] = min(dp[(i-1)%2][j - 1] + alpha[X[m - i], Y[n - j]],
                               dp[(i-1)%2][j] + delta,
                               dp[i%2][j - 1] + delta)


    # This list means that for every index i, dp[m%2][i] is the minimum cost to align X with Y[0..i]
    # If flag==1, dp[m%2][i] is the minimum cost to align reverse X with reverse Y[0..i]
    # -> It is same as aligning X with suffix Y[n-i..n]
    minimum_alignment_cost = dp[m%2] 

    return minimum_alignment_cost


def hirschberg(X, Y, delta, alpha) -> tuple[int, str, str]:
    """
    Hirschberg's algorithm for memory-efficient sequence alignment.
    Returns the aligned sequences as strings.
    """
    
    if len(X) <=2 or len(Y) <=2:
        return original_sequence_alignment(X, Y, delta, alpha)

    k = get_optimal_split_point(X, Y, delta, alpha)
    m = len(X)
    minimum_alignment_cost1, aligned_x1, aligned_y1 = hirschberg(X[:m // 2], Y[:k], delta, alpha)
    minimum_alignment_cost2, aligned_x2, aligned_y2 = hirschberg(X[m // 2:], Y[k:], delta, alpha)
    
    minimum_alignment_cost = minimum_alignment_cost1 + minimum_alignment_cost2
    aligned_x = aligned_x1 + aligned_x2
    aligned_y = aligned_y1 + aligned_y2
    
    return minimum_alignment_cost, aligned_x, aligned_y

def get_optimal_split_point(X, Y, delta, alpha)-> int:
    """
    Helper function to find the optimal split point in Hirschberg's algorithm.
    """
    bestk=0
    best=math.inf
    m , n = len(X), len(Y)
    v1=sequence_alignment(X[:m//2], Y, delta, alpha, 0)
    v2=sequence_alignment(X[m//2:], Y, delta, alpha, 1)
    for j in range(n+1):
        if v1[j]+v2[n-j]<best:
            best=v1[j]+v2[n-j]
            bestk=j

    return bestk


def calculate_alignment_cost(aligned1, aligned2, delta, alpha):
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


def format_output(output_path, cost, aligned1, aligned2, time_ms, memory_kb):
    """Write alignment results to output file"""
    output_dir = os.path.dirname(output_path)
    if output_dir and not os.path.exists(output_dir):
        os.makedirs(output_dir)

    aligned1_str = ''.join(aligned1) if isinstance(aligned1, list) else aligned1
    aligned2_str = ''.join(aligned2) if isinstance(aligned2, list) else aligned2

    with open(output_path, "w") as f:
        f.write(f"{cost}\n")
        f.write(f"{aligned1_str}\n")
        f.write(f"{aligned2_str}\n")
        f.write(f"{time_ms}\n")
        f.write(f"{memory_kb}\n")


def main():
    if len(sys.argv) != 3:
        print("Expected python3/py basic.py <input_file> <output_file>")
        sys.exit(1)

    input_path = sys.argv[1]
    output_path = sys.argv[2]

    string1, string2 = parse_input_file(input_path)

    # Start
    start_time = time.time()

    # main function basic approach
    min_cost, aligned1, aligned2 = sequence_alignment(string1, string2, DELTA, ALPHA)

    cost = calculate_alignment_cost(aligned1, aligned2, DELTA, ALPHA)
    # End
    end_time = time.time()
    time_ms = (end_time - start_time)

    # memory usage
    memory = process_memory()

    format_output(output_path, cost, aligned1, aligned2, time_ms, memory)
    pass


if __name__ == "__main__":
    main()
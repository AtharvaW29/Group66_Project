import sys
import time
import psutil

# Constants
DELTA = 30
ALPHA = {
    ('A', 'A'): 0, ('A', 'C'): 110, ('A', 'G'): 48, ('A', 'T'): 94,
    ('C', 'A'): 110, ('C', 'C'): 0, ('C', 'G'): 118, ('C', 'T'): 48,
    ('G', 'A'): 48, ('G', 'C'): 118, ('G', 'G'): 0, ('G', 'T'): 110,
    ('T', 'A'): 94, ('T', 'C'): 48, ('T', 'G'): 110, ('T', 'T'): 0
}


def generate_string(base_string, indices):
    """
    Generate string by iteratively inserting the string into itself.

    Args:
        base_string: The initial base string
        indices: List of indices where insertions occur

    Returns:
        Final generated string after all insertions
    """
    result = base_string
    for index in indices:
        # Insert result into itself after position 'index'
        result = result[:index + 1] + result + result[index + 1:]
    return result


def parse_input_file(input_path):
    """
    Parse input file and generate the two strings.

    Args:
        input_path: Path to input file

    Returns:
        Tuple of (string1, string2)
    """
    with open(input_path, 'r') as f:
        lines = [line.strip() for line in f.readlines()]

    i = 0
    # Parse first string
    base_string1 = lines[i]
    i += 1

    indices1 = []
    while i < len(lines) and lines[i] and lines[i][0].isdigit():
        indices1.append(int(lines[i]))
        i += 1

    string1 = generate_string(base_string1, indices1)

    # Parse second string
    base_string2 = lines[i]
    i += 1

    indices2 = []
    while i < len(lines) and lines[i] and lines[i][0].isdigit():
        indices2.append(int(lines[i]))
        i += 1

    string2 = generate_string(base_string2, indices2)

    return string1, string2


def sequence_alignment(X, Y, delta, alpha):
    """
    Perform sequence alignment using dynamic programming.

    Args:
        X: First string
        Y: Second string
        delta: Gap penalty
        alpha: Dictionary of mismatch costs

    Returns:
        Tuple of (cost, aligned_X, aligned_Y)
    """
    m, n = len(X), len(Y)

    # Initialize DP table
    dp = [[0] * (n + 1) for _ in range(m + 1)]

    # Base cases
    for i in range(m + 1):
        dp[i][0] = i * delta
    for j in range(n + 1):
        dp[0][j] = j * delta

    # Fill DP table
    for i in range(1, m + 1):
        for j in range(1, n + 1):
            # Case 1: Match/mismatch
            match_cost = dp[i - 1][j - 1] + alpha[(X[i - 1], Y[j - 1])]

            # Case 2: Gap in Y (X[i-1] aligns with gap)
            gap_y = dp[i - 1][j] + delta

            # Case 3: Gap in X (Y[j-1] aligns with gap)
            gap_x = dp[i][j - 1] + delta

            dp[i][j] = min(match_cost, gap_y, gap_x)

    # Backtrack to find alignment
    aligned_x = []
    aligned_y = []

    i, j = m, n
    while i > 0 or j > 0:
        if i > 0 and j > 0 and dp[i][j] == dp[i - 1][j - 1] + alpha[(X[i - 1], Y[j - 1])]:
            # Match/mismatch
            aligned_x.append(X[i - 1])
            aligned_y.append(Y[j - 1])
            i -= 1
            j -= 1
        elif i > 0 and dp[i][j] == dp[i - 1][j] + delta:
            # Gap in Y
            aligned_x.append(X[i - 1])
            aligned_y.append('_')
            i -= 1
        else:
            # Gap in X
            aligned_x.append('_')
            aligned_y.append(Y[j - 1])
            j -= 1

    # Reverse alignments (we built them backwards)
    aligned_x.reverse()
    aligned_y.reverse()

    return dp[m][n], ''.join(aligned_x), ''.join(aligned_y)


def calculate_alignment_cost(aligned1, aligned2, delta, alpha):
    """
    Calculate the cost of a given alignment.

    Args:
        aligned1: First aligned string (with gaps as '_')
        aligned2: Second aligned string (with gaps as '_')
        delta: Gap penalty
        alpha: Dictionary of mismatch costs

    Returns:
        Total alignment cost
    """
    cost = 0
    for i in range(len(aligned1)):
        if aligned1[i] == '_' or aligned2[i] == '_':
            cost += delta
        else:
            cost += alpha[(aligned1[i], aligned2[i])]
    return cost


def process_memory():
    """Get current memory usage in KB"""
    process = psutil.Process()
    memory_info = process.memory_info()
    memory_consumed = int(memory_info.rss / 1024)
    return memory_consumed


def format_output(output_path, cost, aligned1, aligned2, time_ms, memory_kb):
    """
    Write output to file in required format.

    Args:
        output_path: Path to output file
        cost: Alignment cost
        aligned1: First aligned string
        aligned2: Second aligned string
        time_ms: Time in milliseconds
        memory_kb: Memory in kilobytes
    """
    with open(output_path, 'w') as f:
        f.write(f"{cost}\n")
        f.write(f"{aligned1}\n")
        f.write(f"{aligned2}\n")
        f.write(f"{time_ms}\n")
        f.write(f"{memory_kb}\n")


def main():
    """Main function to run the alignment algorithm"""
    if len(sys.argv) != 3:
        print("Usage: python basic.py <input_file> <output_file>")
        sys.exit(1)

    input_path = sys.argv[1]
    output_path = sys.argv[2]

    # Parse input
    string1, string2 = parse_input_file(input_path)

    # Measure time and memory
    start_time = time.time()

    # Run alignment algorithm
    cost, aligned1, aligned2 = sequence_alignment(string1, string2, DELTA, ALPHA)

    end_time = time.time()
    time_ms = (end_time - start_time) * 1000

    # Measure memory after computation
    memory_kb = process_memory()

    # Write output
    format_output(output_path, cost, aligned1, aligned2, time_ms, memory_kb)


if __name__ == "__main__":
    main()
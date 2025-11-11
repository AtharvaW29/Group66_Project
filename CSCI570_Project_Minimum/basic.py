"""
CSCI 570 - Sequence Alignment Project
Basic Algorithm Implementation (Dynamic Programming)

TODO: Implement the basic sequence alignment algorithm using dynamic programming.
"""

import sys
import time
import psutil

# Constants - DO NOT MODIFY
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

    TODO: Implement the string generation logic.

    Algorithm hint:
    - For each index in indices:
        - Insert the current string into itself after position 'index'
        - This should double the length of the string each time

    Args:
        base_string (str): The initial base string
        indices (list): List of indices where insertions occur

    Returns:
        str: Final generated string after all insertions

    Example:
        generate_string("ACTG", [3]) should return "ACTGACTG"
    """
    result = base_string

    # TODO: Implement insertion logic
    # Hint: For each index, you need to split the string and insert itself

    return result


def parse_input_file(input_path):
    """
    Parse input file and generate the two strings.

    TODO: Implement input file parsing.

    Algorithm hint:
    - Read all lines from file
    - Parse first string: base string followed by insertion indices
    - Parse second string: base string followed by insertion indices
    - Use generate_string() for both

    Args:
        input_path (str): Path to input file

    Returns:
        tuple: (string1, string2) - the two generated strings
    """

    # TODO: Read file and parse contents
    # TODO: Extract base string 1 and its indices
    # TODO: Extract base string 2 and its indices
    # TODO: Generate both strings using generate_string()

    string1 = ""
    string2 = ""

    return string1, string2


def sequence_alignment(X, Y, delta, alpha):
    """
    Perform sequence alignment using dynamic programming.

    TODO: Implement the DP algorithm for sequence alignment.

    Algorithm hint:
    1. Create a DP table of size (len(X)+1) x (len(Y)+1)
    2. Initialize base cases (first row and column)
    3. Fill the DP table using the recurrence relation
    4. Backtrack from dp[m][n] to dp[0][0] to construct alignment

    Recurrence relation:
        dp[i][j] = min(
            dp[i-1][j-1] + alpha[X[i-1]][Y[j-1]],  # match/mismatch
            dp[i-1][j] + delta,                      # gap in Y
            dp[i][j-1] + delta                       # gap in X
        )

    Args:
        X (str): First string
        Y (str): Second string
        delta (int): Gap penalty
        alpha (dict): Dictionary of mismatch costs

    Returns:
        tuple: (cost, aligned_X, aligned_Y)
            - cost: Minimum alignment cost
            - aligned_X: First string with gaps (using '_')
            - aligned_Y: Second string with gaps (using '_')
    """
    m, n = len(X), len(Y)

    # TODO: Create DP table (2D array)
    # Hint: Use list comprehension or nested loops

    # TODO: Initialize base cases
    # dp[i][0] = ?
    # dp[0][j] = ?

    # TODO: Fill DP table
    # Use nested loops for i from 1 to m and j from 1 to n

    # TODO: Backtrack to find alignment
    # Start from dp[m][n] and work backwards to dp[0][0]
    # Build aligned strings by determining which case was chosen at each step

    cost = 0
    aligned_x = ""
    aligned_y = ""

    return cost, aligned_x, aligned_y


def calculate_alignment_cost(aligned1, aligned2, delta, alpha):
    """
    Calculate the cost of a given alignment (for verification).

    TODO: Implement cost calculation.

    Algorithm hint:
    - Iterate through both aligned strings position by position
    - If either has a gap ('_'), add delta to cost
    - Otherwise, add alpha[char1][char2] to cost

    Args:
        aligned1 (str): First aligned string (with gaps as '_')
        aligned2 (str): Second aligned string (with gaps as '_')
        delta (int): Gap penalty
        alpha (dict): Dictionary of mismatch costs

    Returns:
        int: Total alignment cost
    """
    cost = 0

    # TODO: Calculate cost by iterating through aligned strings

    return cost


def process_memory():
    """
    Get current memory usage in KB.

    Returns:
        int: Memory consumed in kilobytes
    """
    process = psutil.Process()
    memory_info = process.memory_info()
    memory_consumed = int(memory_info.rss / 1024)
    return memory_consumed


def format_output(output_path, cost, aligned1, aligned2, time_ms, memory_kb):
    """
    Write output to file in required format.

    Output format (5 lines):
    1. Cost (integer)
    2. First aligned string
    3. Second aligned string
    4. Time in milliseconds (float)
    5. Memory in kilobytes (float)

    Args:
        output_path (str): Path to output file
        cost (int): Alignment cost
        aligned1 (str): First aligned string
        aligned2 (str): Second aligned string
        time_ms (float): Time in milliseconds
        memory_kb (float): Memory in kilobytes
    """

    # TODO: Write output to file
    # Make sure to write exactly 5 lines in the correct order

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

    # TODO: Run sequence alignment

    # TODO: Measure end time

    # TODO: Get memory usage

    # TODO: Write output to file

    pass


if __name__ == "__main__":
    main()
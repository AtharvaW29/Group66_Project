import unittest
from pathlib import Path
import re
import time
from basic import (
    sequence_alignment,
    calculate_alignment_cost,
    parse_input_file,
    process_memory,
    format_output
)

# Constants from project
DELTA = 30
ALPHA = {
    ('A', 'A'): 0, ('A', 'C'): 110, ('A', 'G'): 48, ('A', 'T'): 94,
    ('C', 'A'): 110, ('C', 'C'): 0, ('C', 'G'): 118, ('C', 'T'): 48,
    ('G', 'A'): 48, ('G', 'C'): 118, ('G', 'G'): 0, ('G', 'T'): 110,
    ('T', 'A'): 94, ('T', 'C'): 48, ('T', 'G'): 110, ('T', 'T'): 0
}


class MyTestCase(unittest.TestCase):
    def test_end_to_end(self):
        """Test complete pipeline from input to output"""
        input_path = Path("CSCI570_Project_Minimum_Jul_14/SampleTestCases/")
        output_path = Path("CSCI570_Project_Minimum_Jul_14/SampleOutput/")
        expected_output_path = Path("CSCI570_Project_Minimum_Jul_14/SampleTestCases/")

        output_path.mkdir(parents=True, exist_ok=True)

        pattern = re.compile(r"^input\d+\.txt$")
        target_files = [file_path for file_path in input_path.iterdir()
                        if file_path.is_file() and pattern.match(file_path.name)]

        # Sort files by input size for better plotting
        file_sizes = []
        for file_path in target_files:
            string1, string2 = parse_input_file(str(file_path))
            size = len(string1) * len(string2)  # Problem size
            file_sizes.append((file_path, size, len(string1), len(string2)))

        file_sizes.sort(key=lambda x: x[1])  # Sort by problem size

        print(f"\nFound {len(file_sizes)} test files")
        print("\nProcessing in order of size:")
        for i, (file_path, size, len1, len2) in enumerate(file_sizes, 1):
            print(f"  {i}. {file_path.name}: {len1} x {len2} = {size}")

        results = []

        for file_path, size, len1, len2 in file_sizes:
            print(f"\n{'=' * 60}")
            print(f"Testing {file_path.name} (size: {len1} x {len2})")
            print(f"{'=' * 60}")

            string1, string2 = parse_input_file(str(file_path))

            # Run alignment
            start_time = time.time()
            min_cost, aligned1, aligned2 = sequence_alignment(string1, string2, DELTA, ALPHA)
            cost = calculate_alignment_cost(aligned1, aligned2, DELTA, ALPHA)
            end_time = time.time()
            time_ms = (end_time - start_time) * 1000

            memory = process_memory()

            filename_base = file_path.stem
            file_number = filename_base.replace('input', '')

            output_file = output_path / f"output{file_number}.txt"
            format_output(str(output_file), cost, aligned1, aligned2, time_ms, memory)

            # Verify against expected output
            expected_output_file = expected_output_path / f"output{file_number}.txt"

            assert expected_output_file.exists(), f"Expected output file {expected_output_file} not found"

            lines = expected_output_file.read_text().strip().split('\n')
            assert len(lines) == 5, f"Expected 5 lines in output, got {len(lines)}"

            aligned1_str = ''.join(aligned1) if isinstance(aligned1, list) else aligned1
            aligned2_str = ''.join(aligned2) if isinstance(aligned2, list) else aligned2

            expected_cost = int(lines[0])
            assert cost == expected_cost, f"Cost mismatch: expected {expected_cost}, got {cost}"

            assert aligned1_str == lines[1], f"Aligned string 1 mismatch"
            assert aligned2_str == lines[2], f"Aligned string 2 mismatch"

            results.append({
                'file': file_path.name,
                'size': size,
                'len1': len1,
                'len2': len2,
                'cost': cost,
                'time_ms': time_ms,
                'memory_kb': memory
            })

            print(f"✓ Passed - Cost: {cost}, Time: {time_ms:.2f}ms, Memory: {memory}KB")

        # Print summary table
        print(f"\n{'=' * 80}")
        print("SUMMARY (sorted by problem size)")
        print(f"{'=' * 80}")
        print(f"{'File':<15} {'Size (m×n)':<15} {'Cost':<10} {'Time(ms)':<12} {'Memory(KB)':<12}")
        print(f"{'-' * 80}")
        for r in results:
            print(
                f"{r['file']:<15} {r['len1']}×{r['len2']:<12} {r['cost']:<10} {r['time_ms']:<12.2f} {r['memory_kb']:<12}")
        print(f"{'=' * 80}")

    def test_datapoints_basic(self):
        """Test complete pipeline for datapoints"""
        input_path = Path("CSCI570_Project_Minimum_Jul_14/Datapoints/")
        output_path = Path("CSCI570_Project_Minimum_Jul_14/Output/")

        output_path.mkdir(parents=True, exist_ok=True)

        pattern = re.compile(r"^in\d+\.txt$")
        target_files = [file_path for file_path in input_path.iterdir()
                        if file_path.is_file() and pattern.match(file_path.name)]

        # Sort files by input size for better plotting
        file_sizes = []
        for file_path in target_files:
            string1, string2 = parse_input_file(str(file_path))
            size = len(string1) * len(string2)  # Problem size
            file_sizes.append((file_path, size, len(string1), len(string2)))

        file_sizes.sort(key=lambda x: x[1])  # Sort by problem size

        print(f"\nFound {len(file_sizes)} datapoint files")
        print("\nProcessing in order of size:")
        for i, (file_path, size, len1, len2) in enumerate(file_sizes, 1):
            print(f"  {i}. {file_path.name}: {len1} x {len2} = {size}")

        results = []

        for file_path, size, len1, len2 in file_sizes:
            print(f"\n{'=' * 60}")
            print(f"Processing {file_path.name} (size: {len1} x {len2})")
            print(f"{'=' * 60}")

            string1, string2 = parse_input_file(str(file_path))

            # Run alignment
            start_time = time.time()
            min_cost, aligned1, aligned2 = sequence_alignment(string1, string2, DELTA, ALPHA)
            cost = calculate_alignment_cost(aligned1, aligned2, DELTA, ALPHA)
            end_time = time.time()
            time_ms = (end_time - start_time) * 1000

            memory = process_memory()

            filename_base = file_path.stem
            file_number = filename_base.replace('in', '')

            output_file = output_path / f"output{file_number}.txt"
            format_output(str(output_file), cost, aligned1, aligned2, time_ms, memory)

            aligned1_str = ''.join(aligned1) if isinstance(aligned1, list) else aligned1
            aligned2_str = ''.join(aligned2) if isinstance(aligned2, list) else aligned2

            # Basic sanity checks
            assert len(aligned1_str) == len(aligned2_str), "Aligned strings must have same length"
            assert cost >= 0, "Cost must be non-negative"

            # Verify cost calculation
            verified_cost = calculate_alignment_cost(aligned1_str, aligned2_str, DELTA, ALPHA)
            assert cost == verified_cost, f"Cost verification failed: {cost} != {verified_cost}"

            results.append({
                'file': file_path.name,
                'size': size,
                'len1': len1,
                'len2': len2,
                'cost': cost,
                'time_ms': time_ms,
                'memory_kb': memory,
                'length': len(aligned1_str)
            })

            print(f"✓ Completed - Cost: {cost}, Time: {time_ms:.2f}ms, Memory: {memory}KB")

        # Print summary table
        print(f"\n{'=' * 90}")
        print("SUMMARY (sorted by problem size)")
        print(f"{'=' * 90}")
        print(f"{'File':<15} {'Size (m×n)':<15} {'Cost':<10} {'Time(ms)':<12} {'Memory(KB)':<12} {'Align Len':<12}")
        print(f"{'-' * 90}")
        for r in results:
            print(
                f"{r['file']:<15} {r['len1']}×{r['len2']:<12} {r['cost']:<10} {r['time_ms']:<12.2f} {r['memory_kb']:<12} {r['length']:<12}")
        print(f"{'=' * 90}")


if __name__ == '__main__':
    unittest.main()
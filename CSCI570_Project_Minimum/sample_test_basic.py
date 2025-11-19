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
        # compare with expected values
        expected_output_path = Path("CSCI570_Project_Minimum_Jul_14/SampleTestCases/")

        output_path.mkdir(parents=True, exist_ok=True)

        pattern = re.compile(r"^input\d+\.txt$")
        target_files = [file_path for file_path in input_path.iterdir()
                        if file_path.is_file() and pattern.match(file_path.name)]

        for file_path in target_files:
            print(f"Testing {file_path.name}...")

            string1, string2 = parse_input_file(str(file_path))
            print(f"Input string1: {string1}")
            print(f"Input string2: {string2}")
            # Run alignment
            start_time = time.time()
            min_cost, aligned1, aligned2 = sequence_alignment(string1, string2, DELTA, ALPHA)
            cost = calculate_alignment_cost(aligned1, aligned2, DELTA, ALPHA)
            end_time = time.time()
            time_ms = (end_time - start_time)

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

            aligned1_str = ''.join(aligned1)
            aligned2_str = ''.join(aligned2)

            expected_cost = int(lines[0])
            assert cost == expected_cost, f"Cost mismatch: expected {expected_cost}, got {cost}"

            assert aligned1_str == lines[1], f"Aligned string 1 mismatch"
            assert aligned2_str == lines[2], f"Aligned string 2 mismatch"

            print(f"✓ {file_path.name} passed (cost: {cost})")

    def test_datapoints_basic(self):
        """Test complete pipeline from input to output"""
        input_path = Path("CSCI570_Project_Minimum_Jul_14/Datapoints/")
        output_path = Path("CSCI570_Project_Minimum_Jul_14/Output/")
        # expected_output_path = Path("CSCI570_Project_Minimum_Jul_14/SampleTestCases/")

        output_path.mkdir(parents=True, exist_ok=True)

        pattern = re.compile(r"^input\d+\.txt$")
        target_files = [file_path for file_path in input_path.iterdir()
                        if file_path.is_file() and pattern.match(file_path.name)]

        for file_path in target_files:
            print(f"Testing {file_path.name}...")

            string1, string2 = parse_input_file(str(file_path))
            print(f"Input string1: {string1}")
            print(f"Input string2: {string2}")
            # Run alignment
            start_time = time.time()
            min_cost, aligned1, aligned2 = sequence_alignment(string1, string2, DELTA, ALPHA)
            cost = calculate_alignment_cost(aligned1, aligned2, DELTA, ALPHA)
            end_time = time.time()
            time_ms = (end_time - start_time)

            memory = process_memory()

            filename_base = file_path.stem
            file_number = filename_base.replace('input', '')

            output_file = output_path / f"output{file_number}.txt"
            format_output(str(output_file), cost, aligned1, aligned2, time_ms, memory)

            # expected_output_file = expected_output_path / f"output{file_number}.txt"
            #
            # assert expected_output_file.exists(), f"Expected output file {expected_output_file} not found"
            #
            # lines = expected_output_file.read_text().strip().split('\n')
            # assert len(lines) == 5, f"Expected 5 lines in output, got {len(lines)}"
            #
            # aligned1_str = ''.join(aligned1)
            # aligned2_str = ''.join(aligned2)
            #
            # expected_cost = int(lines[0])
            # assert cost == expected_cost, f"Cost mismatch: expected {expected_cost}, got {cost}"
            #
            # assert aligned1_str == lines[1], f"Aligned string 1 mismatch"
            # assert aligned2_str == lines[2], f"Aligned string 2 mismatch"

            print(f"✓ {file_path.name} passed (cost: {cost})")


if __name__ == '__main__':
    unittest.main()

import os.path
import time

import pytest
import sys
from pathlib import  Path
import re
from efficient import (
    generate_string,
    hirschberg,
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

input_dir = Path("CSCI570_Project_Minimum/CSCI570_Project_Minimum_Jul_14/Datapoints")

class TestStringGeneration:
    """Test the string generation mechanism"""

    def test_no_insertions(self):
        """Test base string with no insertions"""
        result = generate_string("ACTG", [])
        assert result == "ACTG"

    def test_single_insertion(self):
        """Test single insertion"""
        result = generate_string("ACTG", [3])
        expected = "ACTGACTG"  # Insert after index 3
        assert result == expected

    def test_multiple_insertions(self):
        """Test the example from project description"""
        result = generate_string("ACTG", [3, 6, 1])
        expected = "ACACTGACTACTGACTGGTGACTACTGACTGG"
        assert result == expected

    def test_insertion_at_start(self):
        """Test insertion at index 0"""
        result = generate_string("AB", [0])
        expected = "AABB"
        assert result == expected

    def test_length_doubling(self):
        """Verify that each insertion doubles the length"""
        base = "ACTG"
        for i in range(1, 5):
            indices = [0] * i
            result = generate_string(base, indices)
            expected_length = len(base) * (2 ** i)
            assert len(result) == expected_length


class TestInputParsing:
    """Test input file parsing"""

    def test_parse_example_input(self, tmp_path):
        """Test parsing the example input file"""
        input_content = """ACTG
3
6
1
1
TACG
1
2
9
2"""
        input_file = tmp_path / "test_input.txt"
        input_file.write_text(input_content)

        string1, string2 = parse_input_file(str(input_file))

        # Verify first string
        expected1 = generate_string("ACTG", [3, 6, 1, 1])
        assert string1 == expected1

        # Verify second string
        expected2 = generate_string("TACG", [1, 2, 9, 2])
        assert string2 == expected2

    def test_parse_minimal_input(self, tmp_path):
        """Test with just base strings, no insertions"""
        input_content = """ACT
TACG"""
        input_file = tmp_path / "test_input.txt"
        input_file.write_text(input_content)

        string1, string2 = parse_input_file(str(input_file))
        assert string1 == "ACT"
        assert string2 == "TACG"

    def test_parse_single_character(self, tmp_path):
        """Test with single character base strings"""
        input_content = """A
C"""
        input_file = tmp_path / "test_input.txt"
        input_file.write_text(input_content)

        string1, string2 = parse_input_file(str(input_file))
        assert string1 == "A"
        assert string2 == "C"


class TestAlignmentCost:
    """Test alignment cost calculation"""

    def test_gap_cost(self):
        """Test pure gap alignment"""
        aligned1 = "A_"
        aligned2 = "_A"
        cost = calculate_alignment_cost(aligned1, aligned2, DELTA, ALPHA)
        expected = 2 * DELTA  # Two gaps
        assert cost == expected

    def test_match_cost(self):
        """Test matching characters"""
        aligned1 = "AAA"
        aligned2 = "AAA"
        cost = calculate_alignment_cost(aligned1, aligned2, DELTA, ALPHA)
        assert cost == 0  # Perfect match

    def test_mismatch_cost(self):
        """Test mismatch cost"""
        aligned1 = "A"
        aligned2 = "C"
        cost = calculate_alignment_cost(aligned1, aligned2, DELTA, ALPHA)
        assert cost == 110  # A-C mismatch

    def test_mixed_alignment(self):
        """Test combination of gaps and mismatches"""
        aligned1 = "A_C"
        aligned2 = "_AC"
        cost = calculate_alignment_cost(aligned1, aligned2, DELTA, ALPHA)
        # 1 gap in string1 + 1 gap in string2 + A-A match + C-C match
        expected = 2 * DELTA
        assert cost == expected

    def test_example_output_cost(self):
        """Test cost from provided example"""
        aligned1 = "_A_CA_CACT__G__A_C_TAC_TGACTG_GTGA__C_TACTGACTGGACTGACTACTGACTGGTGACTACT_GACTG_G"
        aligned2 = "TATTATTA_TACGCTATTATACGCGAC_GCG_GACGCGTA_T_AC__G_CT_ATTA_T_AC__GCGAC_GC_GGAC_GCG"
        cost = calculate_alignment_cost(aligned1, aligned2, DELTA, ALPHA)
        assert cost == 1296


class TestSequenceAlignment:
    """Test the alignment algorithm"""

    def test_empty_strings(self):
        """Test with empty strings"""
        cost, aligned1, aligned2 = hirschberg("", "", DELTA, ALPHA)
        assert cost == 0
        assert aligned1 == ""
        assert aligned2 == ""

    def test_one_empty_string(self):
        """Test with one empty string"""
        cost, aligned1, aligned2 = hirschberg("A", "", DELTA, ALPHA)
        assert cost == DELTA
        assert aligned1 == "A"
        assert aligned2 == "_"

    def test_single_character_match(self):
        """Test single matching characters"""
        cost, aligned1, aligned2 = hirschberg("A", "A", DELTA, ALPHA)
        assert cost == 0
        assert aligned1 == "A"
        assert aligned2 == "A"

    def test_single_character_mismatch(self):
        """Test single mismatching characters"""
        cost, aligned1, aligned2 = hirschberg("A", "C", DELTA, ALPHA)
        # Should choose minimum of: gap+gap=60 or mismatch=110
        assert cost == 60
        # Either A_, _C or _A, C_ are valid
        assert len(aligned1) == 2
        assert len(aligned2) == 2
        assert aligned1.count('_') == 1
        assert aligned2.count('_') == 1

    def test_identical_strings(self):
        """Test identical strings"""
        cost, aligned1, aligned2 = hirschberg("ACTG", "ACTG", DELTA, ALPHA)
        assert cost == 0
        assert aligned1 == "ACTG"
        assert aligned2 == "ACTG"

    def test_alignment_length_consistency(self):
        """Test that aligned strings have equal length"""
        cost, aligned1, aligned2 = hirschberg("ACTG", "TGC", DELTA, ALPHA)
        assert len(aligned1) == len(aligned2)

    def test_alignment_preserves_order(self):
        """Test that original characters maintain their order"""
        cost, aligned1, aligned2 = hirschberg("ACT", "AGT", DELTA, ALPHA)

        # Extract non-gap characters and verify order
        chars1 = [c for c in aligned1 if c != '_']
        chars2 = [c for c in aligned2 if c != '_']

        assert ''.join(chars1) == "ACT"
        assert ''.join(chars2) == "AGT"

    def test_known_example(self):
        """Test with the provided example"""
        string1 = generate_string("ACTG", [3, 6, 1, 1])
        string2 = generate_string("TACG", [1, 2, 9, 2])

        cost, aligned1, aligned2 = hirschberg(string1, string2, DELTA, ALPHA)

        # Verify cost
        assert cost == 1296

        # Verify alignment lengths match
        assert len(aligned1) == len(aligned2)

        # Verify no consecutive gaps in same position (impossible in valid alignment)
        for i in range(len(aligned1)):
            assert not (aligned1[i] == '_' and aligned2[i] == '_')

        # Verify calculated cost matches
        calculated_cost = calculate_alignment_cost(aligned1, aligned2, DELTA, ALPHA)
        assert calculated_cost == cost





class TestOutputFormat:
    """Test output formatting and file writing"""

    def test_output_format(self, tmp_path):
        """Test output file format"""
        output_file = tmp_path / "test_output.txt"

        cost = 1296
        aligned1 = "ACTG"
        aligned2 = "TACG"
        time_ms = 3.72
        memory_kb = 54880

        format_output(str(output_file), cost, aligned1, aligned2, time_ms, memory_kb)

        # Read and verify
        lines = output_file.read_text().strip().split('\n')

        assert len(lines) == 5
        assert lines[0] == "1296"
        assert lines[1] == "ACTG"
        assert lines[2] == "TACG"
        assert float(lines[3]) == 3.72
        assert float(lines[4]) == 54880

    def test_output_line_order(self, tmp_path):
        """Test that output lines are in correct order"""
        output_file = tmp_path / "test_output.txt"

        format_output(str(output_file), 100, "A_", "_A", 1.5, 1024)

        lines = output_file.read_text().strip().split('\n')

        # Line 1: Cost (integer)
        assert lines[0].isdigit()

        # Lines 2-3: Alignments (contain only A, C, G, T, _)
        valid_chars = set('ACGT_')
        assert all(c in valid_chars for c in lines[1])
        assert all(c in valid_chars for c in lines[2])

        # Lines 4-5: Time and memory (floats)
        assert float(lines[3]) >= 0
        assert float(lines[4]) >= 0


class TestEdgeCases:
    """Test edge cases and boundary conditions"""

    def test_max_basic_bounds(self):
        """Test within basic algorithm bounds (j, k <= 10)"""
        # Generate string with j=10 insertions
        base = "A"
        indices = [0] * 10
        result = generate_string(base, indices)
        expected_length = len(base) * (2 ** 10)
        assert len(result) == expected_length

    def test_all_gaps_alignment(self):
        """Test when optimal alignment might be all gaps"""
        # Two strings with high mismatch costs
        cost, aligned1, aligned2 = hirschberg("AA", "CC", DELTA, ALPHA)

        # Verify cost is calculated correctly
        calculated_cost = calculate_alignment_cost(aligned1, aligned2, DELTA, ALPHA)
        assert cost == calculated_cost

    def test_long_string_alignment(self):
        """Test with longer strings"""
        string1 = "ACTGACTGACTG"
        string2 = "TACGTACGTACG"

        cost, aligned1, aligned2 = hirschberg(string1, string2, DELTA, ALPHA)

        # Basic validations
        assert len(aligned1) == len(aligned2)
        assert cost >= 0
        assert ''.join(c for c in aligned1 if c != '_') == string1
        assert ''.join(c for c in aligned2 if c != '_') == string2

    def test_repeated_characters(self):
        """Test with repeated characters"""
        cost, aligned1, aligned2 = hirschberg("AAAA", "AAAA", DELTA, ALPHA)
        assert cost == 0

        cost, aligned1, aligned2 = hirschberg("AAAA", "CCCC", DELTA, ALPHA)
        assert cost > 0


class TestIntegration:
    """Integration tests using sample test cases"""

    def test_sample_input1(self, tmp_path):
        """Test with sample input file 1 if available"""
        # This would test against actual sample files from SampleTestCases
        pass

    def test_end_to_end(self):
        """Test complete pipeline from input to output"""
        input_path = Path("CSCI570_Project_Minimum_Jul_14/SampleTestCases/")
        output_path = Path("CSCI570_Project_Minimum_Jul_14/SampleEfficientOutput/")
        expected_output_path = Path("CSCI570_Project_Minimum_Jul_14/SampleTestCases/")

        # Create output directory if it doesn't exist
        output_path.mkdir(parents=True, exist_ok=True)

        # Find all input files
        pattern = re.compile(r"^input\d+\.txt$")
        target_files = [file_path for file_path in input_path.iterdir()
                        if file_path.is_file() and pattern.match(file_path.name)]

        for file_path in target_files:
            print(f"Testing {file_path.name}...")

            # Parse input
            string1, string2 = parse_input_file(str(file_path))

            # Run alignment
            start_time = time.time()
            min_cost, aligned1, aligned2 = hirschberg(string1, string2, DELTA, ALPHA)
            cost = calculate_alignment_cost(aligned1, aligned2, DELTA, ALPHA)
            end_time = time.time()
            time_ms = (end_time - start_time)

            memory = process_memory()

            # Extract file number (e.g., "input1.txt" -> "1")
            filename_base = file_path.stem  # Gets "input1" from "input1.txt"
            file_number = filename_base.replace('input', '')  # Gets "1"

            # Write output
            output_file = output_path / f"output{file_number}.txt"
            format_output(str(output_file), cost, aligned1, aligned2, time_ms, memory)

            # Verify against expected output
            expected_output_file = expected_output_path / f"output{file_number}.txt"

            assert expected_output_file.exists(), f"Expected output file {expected_output_file} not found"

            lines = expected_output_file.read_text().strip().split('\n')
            assert len(lines) == 5, f"Expected 5 lines in output, got {len(lines)}"

            # Convert aligned lists to strings for comparison
            aligned1_str = ''.join(aligned1)
            aligned2_str = ''.join(aligned2)

            # Compare outputs (with some tolerance for time and memory)
            expected_cost = int(lines[0])
            assert cost == expected_cost, f"Cost mismatch: expected {expected_cost}, got {cost}"

            # Since there can be multiple correct answers, so we leave this out
            # assert aligned1_str == lines[1], f"Aligned string 1 mismatch"
            # assert aligned2_str == lines[2], f"Aligned string 2 mismatch"

            # Don't assert exact time/memory match as they vary by system
            print(f"✓ {file_path.name} passed (cost: {cost})")

class TestMemoryAndTime:
    """Test memory and time measurement functions"""

    def test_time_measurement_positive(self):
        """Test that time measurement returns positive values"""
        # This would test time measurement function
        pass

    def test_memory_measurement_positive(self):
        """Test that memory measurement returns positive values"""
        # This would test memory measurement function
        pass


if __name__ == "__main__":
    pytest.main([__file__, "-v", "--tb=short"])
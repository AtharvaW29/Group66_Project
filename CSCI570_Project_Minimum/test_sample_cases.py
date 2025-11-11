"""
Test runner for sample test cases.
This script runs your implementation against the provided sample test cases
and compares the results.
"""

import os
import sys
from pathlib import Path
from basic import parse_input_file, sequence_alignment, DELTA, ALPHA


def read_expected_output(output_path):
    """Read expected output from file"""
    with open(output_path, 'r') as f:
        lines = [line.strip() for line in f.readlines()]

    expected_cost = int(lines[0])
    expected_aligned1 = lines[1]
    expected_aligned2 = lines[2]

    return expected_cost, expected_aligned1, expected_aligned2


def test_sample_case(input_file, output_file):
    """Test a single sample case"""
    print(f"\nTesting: {input_file.name}")
    print("=" * 60)

    try:
        # Parse input and run alignment
        string1, string2 = parse_input_file(str(input_file))
        print(f"String 1 length: {len(string1)}")
        print(f"String 2 length: {len(string2)}")
        print(f"Problem size (m+n): {len(string1) + len(string2)}")

        # Run alignment
        cost, aligned1, aligned2 = sequence_alignment(string1, string2, DELTA, ALPHA)

        # Read expected output
        expected_cost, expected_aligned1, expected_aligned2 = read_expected_output(output_file)

        # Compare costs
        print(f"\nExpected cost: {expected_cost}")
        print(f"Actual cost:   {cost}")

        if cost == expected_cost:
            print("✓ Cost matches!")
        else:
            print("✗ Cost MISMATCH!")
            return False

        # Verify alignment lengths
        print(f"\nExpected alignment length: {len(expected_aligned1)}")
        print(f"Actual alignment length:   {len(aligned1)}")

        if len(aligned1) != len(aligned2):
            print("✗ Aligned strings have different lengths!")
            return False

        # Verify original strings are preserved in alignment
        actual_str1 = ''.join(c for c in aligned1 if c != '_')
        actual_str2 = ''.join(c for c in aligned2 if c != '_')

        if actual_str1 != string1:
            print("✗ First string not preserved in alignment!")
            return False

        if actual_str2 != string2:
            print("✗ Second string not preserved in alignment!")
            return False

        print("✓ All checks passed!")

        # Show first 50 characters of alignment for verification
        print(f"\nAlignment preview (first 50 chars):")
        print(f"  Your:     {aligned1[:50]}")
        print(f"  Expected: {expected_aligned1[:50]}")
        print(f"  Your:     {aligned2[:50]}")
        print(f"  Expected: {expected_aligned2[:50]}")

        return True

    except Exception as e:
        print(f"✗ Error: {e}")
        import traceback
        traceback.print_exc()
        return False


def main():
    """Run all sample test cases"""
    # Find sample test cases directory
    sample_dir = Path("CSCI570_Project_Minimum_Jul_14/SampleTestCases")

    if not sample_dir.exists():
        print(f"Error: Sample test cases directory not found at {sample_dir}")
        print("Please adjust the path in the script.")
        sys.exit(1)

    # Find all input files
    input_files = sorted(sample_dir.glob("input*.txt"))

    if not input_files:
        print(f"No input files found in {sample_dir}")
        sys.exit(1)

    print(f"Found {len(input_files)} test cases")

    results = []
    for input_file in input_files:
        # Find corresponding output file
        output_file = sample_dir / input_file.name.replace("input", "output")

        if not output_file.exists():
            print(f"Warning: No output file found for {input_file.name}")
            continue

        # Run test
        success = test_sample_case(input_file, output_file)
        results.append((input_file.name, success))

    # Summary
    print("\n" + "=" * 60)
    print("SUMMARY")
    print("=" * 60)

    passed = sum(1 for _, success in results if success)
    total = len(results)

    for name, success in results:
        status = "✓ PASS" if success else "✗ FAIL"
        print(f"{status}: {name}")

    print(f"\nPassed: {passed}/{total}")

    if passed == total:
        print("\n🎉 All tests passed!")
    else:
        print(f"\n⚠ {total - passed} test(s) failed")


if __name__ == "__main__":
    main()
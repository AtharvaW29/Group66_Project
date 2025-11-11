# Testing Guide for CSCI 570 Sequence Alignment Project

## Setup

### Install Dependencies

```bash
pip install pytest psutil
```

## Test Structure

### 1. Unit Tests (`test_basic.py`)

Comprehensive unit tests covering:

- **String Generation Tests**
  - No insertions
  - Single insertion
  - Multiple insertions
  - Edge cases (insertion at start, length doubling verification)

- **Input Parsing Tests**
  - Example input from project description
  - Minimal input (no insertions)
  - Single character strings

- **Alignment Cost Tests**
  - Pure gap alignment
  - Perfect matches
  - Mismatches
  - Mixed alignments
  - Verification against example output

- **Sequence Alignment Algorithm Tests**
  - Empty strings
  - Single characters
  - Identical strings
  - Alignment length consistency
  - Order preservation
  - Known examples

- **Output Format Tests**
  - Correct line order
  - Proper data types
  - File creation

- **Edge Cases**
  - Maximum bounds
  - All gaps
  - Long strings
  - Repeated characters

## Running Tests

### Run All Unit Tests

```bash
pytest test_basic.py -v
```

### Run Specific Test Class

```bash
# Test only string generation
pytest test_basic.py::TestStringGeneration -v

# Test only alignment algorithm
pytest test_basic.py::TestSequenceAlignment -v

# Test only alignment cost calculation
pytest test_basic.py::TestAlignmentCost -v
```

### Run Specific Test

```bash
pytest test_basic.py::TestStringGeneration::test_multiple_insertions -v
```

### Run with Coverage

```bash
pip install pytest-cov
pytest test_basic.py --cov=basic --cov-report=html
```

This creates an HTML coverage report in `htmlcov/index.html`

### Run Sample Test Cases

```bash
python test_sample_cases.py
```

This runs your implementation against all provided sample test cases and compares:
- Alignment cost
- Alignment validity
- String preservation

## Test Output Examples

### Successful Test Output

```
test_basic.py::TestStringGeneration::test_multiple_insertions PASSED
test_basic.py::TestSequenceAlignment::test_known_example PASSED
test_basic.py::TestAlignmentCost::test_example_output_cost PASSED
```

### Failed Test Output

```
test_basic.py::TestSequenceAlignment::test_known_example FAILED

AssertionError: assert 1300 == 1296
Expected alignment cost of 1296 but got 1300
```

## Debugging Failed Tests

### 1. Check String Generation

```python
from basic import generate_string

# Test the example
result = generate_string("ACTG", [3, 6, 1])
print(result)
# Expected: ACACTGACTACTGACTGGTGACTACTGACTGG
```

### 2. Check Alignment Cost

```python
from basic import calculate_alignment_cost, DELTA, ALPHA

aligned1 = "A_"
aligned2 = "_A"
cost = calculate_alignment_cost(aligned1, aligned2, DELTA, ALPHA)
print(f"Cost: {cost}, Expected: {2 * DELTA}")
```

### 3. Test with Simple Cases

```python
from basic import sequence_alignment, DELTA, ALPHA

# Simple test
cost, a1, a2 = sequence_alignment("A", "A", DELTA, ALPHA)
print(f"Cost: {cost}, Alignment: {a1} / {a2}")
# Expected: Cost: 0, Alignment: A / A
```

## Common Issues and Solutions

### Issue 1: String Generation Not Doubling Length

**Problem**: Each insertion should double the string length

**Check**:
```python
base = "ACTG"
result = generate_string(base, [3])
print(len(result))  # Should be 8 (2 * 4)
```

**Solution**: Ensure insertion logic is: `result[:index+1] + result + result[index+1:]`

### Issue 2: Alignment Cost Mismatch

**Problem**: Calculated cost doesn't match expected

**Debug**:
```python
# Print DP table to see computation
# Add debug prints in sequence_alignment function
```

**Common causes**:
- Incorrect gap penalty application
- Wrong mismatch cost lookup
- Error in DP recurrence relation

### Issue 3: Alignment Doesn't Preserve Original Strings

**Problem**: Characters from original string are missing or reordered

**Check**:
```python
aligned1 = "A_C_T"
original = ''.join(c for c in aligned1 if c != '_')
print(original)  # Should be "ACT"
```

**Solution**: Verify backtracking logic correctly traces path through DP table

### Issue 4: Different Alignment but Same Cost

**Note**: This is VALID! Multiple alignments can have the same optimal cost.

Example for "A" and "C":
- Alignment 1: `A_` / `_C` (cost: 60)
- Alignment 2: `_A` / `C_` (cost: 60)

Both are correct! Tests should verify cost, not exact alignment.

## Validation Checklist

Before submission, verify:

- [ ] All unit tests pass
- [ ] Sample test cases pass (correct costs)
- [ ] Output format is correct (5 lines in right order)
- [ ] Aligned strings have equal length
- [ ] Original strings preserved in alignments
- [ ] No impossible alignments (both gaps at same position)
- [ ] Time and memory measurements work
- [ ] Shell script runs correctly

## Performance Testing

### Test with Increasing Problem Sizes

```python
# Create test with different sizes
for j in range(1, 6):
    indices = [0] * j
    string1 = generate_string("ACTG", indices)
    string2 = generate_string("TACG", indices)
    
    start = time.time()
    cost, _, _ = sequence_alignment(string1, string2, DELTA, ALPHA)
    elapsed = time.time() - start
    
    size = len(string1) + len(string2)
    print(f"Size: {size}, Time: {elapsed:.3f}s")
```

### Expected Complexity

- **Basic Algorithm**: 
  - Time: O(m × n)
  - Space: O(m × n)

You should see roughly quadratic growth in both time and space.

## Continuous Testing During Development

Use pytest's watch mode:

```bash
pip install pytest-watch
ptw test_basic.py
```

This automatically reruns tests when you save changes to `basic.py`.

## Questions?

If tests fail and you're unsure why:

1. Run the specific failing test with `-v` flag for details
2. Add print statements to debug
3. Test with simple manual examples first
4. Verify against project description requirements
5. Check the sample outputs provided

## Additional Test Ideas

You can add your own tests for:

- Specific corner cases you're worried about
- Performance benchmarks
- Different gap/mismatch penalty values
- Stress tests with very long strings
- Verification of memory efficiency

Example:

```python
def test_my_corner_case():
    """Test a specific scenario I'm concerned about"""
    cost, a1, a2 = sequence_alignment("AAAA", "TTTT", DELTA, ALPHA)
    # Add your assertions
    assert cost > 0
```

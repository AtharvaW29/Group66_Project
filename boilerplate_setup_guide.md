# Setup and Development Workflow Guide

## Quick Setup

### 1. Install Python Dependencies
```bash
pip install pytest psutil
```

### 2. Project Structure
```
Your_Project_Folder/
├── basic.py                    # Your basic algorithm implementation
├── efficient.py                # Your efficient algorithm implementation
├── test_basic.py              # Unit tests
├── test_sample_cases.py       # Sample test runner
├── basic.sh                    # Shell script for basic
├── efficient.sh               # Shell script for efficient
├── IMPLEMENTATION_GUIDE.md    # Step-by-step guide
├── EXAMPLES_WALKTHROUGH.md    # Concrete examples
└── CSCI570_Project_Minimum_Jul_14/
    ├── SampleTestCases/       # Provided sample inputs/outputs
    │   ├── input1.txt
    │   ├── output1.txt
    │   └── ...
    └── Datapoints/            # Files for generating graphs
        ├── in1.txt
        └── ...
```

### 3. Make Shell Scripts Executable (Unix/Mac/Linux)
```bash
chmod +x basic.sh
chmod +x efficient.sh
```

---

## Development Workflow

### Phase 1: Implement Basic Algorithm

#### Step 1: Implement String Generation
```bash
# 1. Open basic.py
# 2. Implement generate_string() function
# 3. Test it:
python3 -c "from basic import generate_string; print(generate_string('ACTG', [3]))"
# Expected output: ACTGACTG
```

#### Step 2: Implement Input Parsing
```bash
# 1. Implement parse_input_file() in basic.py
# 2. Test with sample input:
python3 -c "from basic import parse_input_file; s1, s2 = parse_input_file('CSCI570_Project_Minimum_Jul_14/SampleTestCases/input1.txt'); print(f'Lengths: {len(s1)}, {len(s2)}')"
```

#### Step 3: Implement DP Algorithm
```bash
# 1. Implement sequence_alignment() in basic.py
# 2. Test with simple strings:
python3 -c "from basic import sequence_alignment, DELTA, ALPHA; cost, a1, a2 = sequence_alignment('A', 'A', DELTA, ALPHA); print(f'Cost: {cost}')"
# Expected: Cost: 0
```

#### Step 4: Implement Cost Calculation
```bash
# 1. Implement calculate_alignment_cost() in basic.py
# 2. Test:
python3 -c "from basic import calculate_alignment_cost, DELTA, ALPHA; print(calculate_alignment_cost('A_', '_A', DELTA, ALPHA))"
# Expected: 60
```

#### Step 5: Complete Main Function
```bash
# 1. Implement format_output() and main() in basic.py
# 2. Test end-to-end:
python3 basic.py CSCI570_Project_Minimum_Jul_14/SampleTestCases/input1.txt test_output.txt
# 3. Check test_output.txt has 5 lines
cat test_output.txt
```

#### Step 6: Test with Shell Script
```bash
# 1. Update basic.sh with correct command
# 2. Test:
./basic.sh CSCI570_Project_Minimum_Jul_14/SampleTestCases/input1.txt test_output.txt
```

---

### Phase 2: Run Unit Tests

#### Run All Tests
```bash
pytest test_basic.py -v
```

#### Run Specific Test Classes
```bash
# Test only string generation
pytest test_basic.py::TestStringGeneration -v

# Test only alignment algorithm
pytest test_basic.py::TestSequenceAlignment -v
```

#### Run Tests with Coverage
```bash
pip install pytest-cov
pytest test_basic.py --cov=basic --cov-report=html
# Open htmlcov/index.html in browser
```

---

### Phase 3: Test Against Sample Cases

```bash
# Run sample test case runner
python3 test_sample_cases.py
```

This will:
- Test against all provided sample inputs
- Compare your costs with expected costs
- Verify alignment validity
- Show which tests pass/fail

---

### Phase 4: Implement Efficient Algorithm

#### Copy Working Functions
```bash
# Copy these from basic.py to efficient.py:
# - generate_string()
# - parse_input_file()
# - calculate_alignment_cost()
# - process_memory()
# - format_output()
```

#### Implement Space-Efficient Functions
1. Implement `space_efficient_alignment_cost()`
2. Implement `find_split_point()`
3. Implement `basic_dp_alignment()` (helper)
4. Implement `memory_efficient_alignment()` (main)

#### Test Efficient Version
```bash
python3 efficient.py CSCI570_Project_Minimum_Jul_14/SampleTestCases/input1.txt test_output_efficient.txt

# Compare costs (should be same as basic)
diff test_output.txt test_output_efficient.txt
# Memory usage should be lower for efficient version
```

---

### Phase 5: Generate Data for Graphs

#### Run on All Datapoint Files
```bash
# Create a script to run all datapoint files
for i in {1..15}; do
    echo "Processing in${i}.txt..."
    ./basic.sh "CSCI570_Project_Minimum_Jul_14/Datapoints/in${i}.txt" "datapoint_basic_${i}.txt"
    ./efficient.sh "CSCI570_Project_Minimum_Jul_14/Datapoints/in${i}.txt" "datapoint_efficient_${i}.txt"
done
```

#### Extract Data for Plotting
```bash
# Create a CSV or extract data from output files
# You'll need: problem_size (m+n), time, memory for both algorithms
```

---

## Testing Strategy

### Test Incrementally
```
1. Test string generation alone
   ↓
2. Test input parsing alone
   ↓
3. Test DP with simple cases (empty, single char)
   ↓
4. Test DP with small cases (2-3 characters)
   ↓
5. Test with sample test cases
   ↓
6. Test with all sample cases
   ↓
7. Test efficient version
```

### Debugging Steps

#### If String Generation Fails
```python
# Test each step manually
base = "ACTG"
result = base
for idx in [3, 6, 1]:
    print(f"Before: {result} (len={len(result)})")
    result = result[:idx+1] + result + result[idx+1:]
    print(f"After index {idx}: {result} (len={len(result)})")
```

#### If DP Cost is Wrong
```python
# Print DP table
def print_table(dp, X, Y):
    print("DP Table:")
    for i in range(len(dp)):
        print(dp[i])
```

#### If Alignment is Invalid
```python
# Verify properties
aligned1 = "A_C"
aligned2 = "_AC"

# Check 1: Equal length
assert len(aligned1) == len(aligned2)

# Check 2: No double gaps
for i in range(len(aligned1)):
    assert not (aligned1[i] == '_' and aligned2[i] == '_')

# Check 3: Original strings preserved
original1 = ''.join(c for c in aligned1 if c != '_')
print(f"Should be 'AC': {original1}")
```

---

## Common Commands Reference

### Run Basic Algorithm
```bash
python3 basic.py input.txt output.txt
# OR
./basic.sh input.txt output.txt
```

### Run Efficient Algorithm
```bash
python3 efficient.py input.txt output.txt
# OR
./efficient.sh input.txt output.txt
```

### Run All Unit Tests
```bash
pytest test_basic.py -v
```

### Run Sample Tests
```bash
python3 test_sample_cases.py
```

### Check Output Format
```bash
# Output should have exactly 5 lines
wc -l output.txt
# Should print: 5 output.txt
```

### Verify Cost
```bash
# First line should be the cost
head -n 1 output.txt
```

---

## Troubleshooting

### Import Errors
```bash
# Make sure you're in the correct directory
pwd

# Make sure basic.py exists
ls -l basic.py

# Check Python version
python3 --version
# Should be 3.6+
```

### Permission Errors (Shell Scripts)
```bash
# Make scripts executable
chmod +x basic.sh efficient.sh
```

### Memory Measurement Not Working
```bash
# Install psutil
pip install psutil

# Test it
python3 -c "import psutil; print('psutil working')"
```

### Tests Not Found
```bash
# Install pytest
pip install pytest

# Verify installation
pytest --version
```

---

## Pre-Submission Checklist

- [ ] `basic.py` runs on all sample inputs
- [ ] `efficient.py` runs on all sample inputs  
- [ ] Both produce same costs (within reasonable bounds)
- [ ] `basic.sh` and `efficient.sh` work correctly
- [ ] Unit tests pass
- [ ] Sample test cases pass
- [ ] Output format is correct (5 lines)
- [ ] Code is commented
- [ ] No plagiarism (implemented yourself!)
- [ ] Graphs generated from datapoints
- [ ] Summary.pdf completed
- [ ] All files in correct directory structure
- [ ] Zip file named correctly (USCIDs separated by underscore)

---

## Quick Test Commands

```bash
# Test 1: Quick functionality test
./basic.sh CSCI570_Project_Minimum_Jul_14/SampleTestCases/input1.txt out1.txt && head -n 1 out1.txt

# Test 2: Verify output format
./basic.sh CSCI570_Project_Minimum_Jul_14/SampleTestCases/input1.txt out1.txt && wc -l out1.txt

# Test 3: Run unit tests
pytest test_basic.py -v --tb=short

# Test 4: Test sample cases
python3 test_sample_cases.py

# Test 5: Compare basic vs efficient cost
./basic.sh CSCI570_Project_Minimum_Jul_14/SampleTestCases/input1.txt out_basic.txt
./efficient.sh CSCI570_Project_Minimum_Jul_14/SampleTestCases/input1.txt out_efficient.txt
diff <(head -n 1 out_basic.txt) <(head -n 1 out_efficient.txt)
```

---

## Time Estimates

- **String Generation**: 30 minutes
- **Input Parsing**: 30 minutes
- **DP Algorithm**: 2-3 hours
- **Testing & Debugging**: 2-3 hours
- **Efficient Version**: 3-4 hours
- **Graphs & Report**: 1-2 hours

**Total**: 10-15 hours

Start early! Don't wait until the deadline! 🚀

---

## Getting Help

1. **Read the project description carefully**
2. **Review lecture slides** (NOT the textbook pseudocode!)
3. **Test with simple examples first**
4. **Use print statements for debugging**
5. **Ask on Piazza** if stuck
6. **Start early** - don't wait!

Good luck! 🎓

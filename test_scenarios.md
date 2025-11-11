# Comprehensive Test Scenarios for Sequence Alignment Project

## Overview

This document details all test scenarios to ensure correctness of your implementation. Each scenario is designed to catch specific types of bugs.

---

## 1. String Generation Tests

### Scenario 1.1: Base String Only (No Insertions)
```
Input: base="ACTG", indices=[]
Expected: "ACTG"
Purpose: Verify base case works
```

### Scenario 1.2: Single Insertion
```
Input: base="ACTG", indices=[3]
Process: 
  - Start: "ACTG"
  - Insert after index 3: "ACTG" + "ACTG" = "ACTGACTG"
Expected: "ACTGACTG"
Purpose: Verify single insertion doubles length
```

### Scenario 1.3: Multiple Insertions (Project Example)
```
Input: base="ACTG", indices=[3, 6, 1]
Process:
  - Start: "ACTG"
  - After index 3: "ACTGACTG" (length 8)
  - After index 6: "ACTGACTACTGACTGG" (length 16)
  - After index 1: "ACACTGACTACTGACTGGTGACTACTGACTGG" (length 32)
Expected: "ACACTGACTACTGACTGGTGACTACTGACTGG"
Purpose: Verify project example works correctly
```

### Scenario 1.4: Insertion at Index 0
```
Input: base="AB", indices=[0]
Process:
  - Start: "AB"
  - Insert after index 0: "A" + "AB" + "B" = "AABB"
Expected: "AABB"
Purpose: Test boundary condition (insertion at start)
```

### Scenario 1.5: Length Doubling Property
```
For any base string and n insertions:
Expected: len(result) = len(base) * 2^n
Purpose: Verify mathematical property holds
```

---

## 2. Input Parsing Tests

### Scenario 2.1: Standard Input Format
```
Input file content:
ACTG
3
6
1
1
TACG
1
2
9
2

Expected:
  string1 = generate_string("ACTG", [3, 6, 1, 1])
  string2 = generate_string("TACG", [1, 2, 9, 2])
Purpose: Test standard format parsing
```

### Scenario 2.2: Minimal Input (No Insertions)
```
Input file content:
ACT
TACG

Expected:
  string1 = "ACT"
  string2 = "TACG"
Purpose: Test edge case with no generation needed
```

### Scenario 2.3: Single Character Strings
```
Input file content:
A
C

Expected:
  string1 = "A"
  string2 = "C"
Purpose: Test minimum possible input
```

---

## 3. Alignment Cost Calculation Tests

### Scenario 3.1: Pure Gap Alignment
```
Aligned1: "A_"
Aligned2: "_A"
Expected Cost: 2 * 30 = 60
Purpose: Verify gap penalty calculation
```

### Scenario 3.2: Perfect Match
```
Aligned1: "AAA"
Aligned2: "AAA"
Expected Cost: 0
Purpose: Verify matching characters have no cost
```

### Scenario 3.3: Single Mismatch
```
Aligned1: "A"
Aligned2: "C"
Expected Cost: 110 (from alpha table)
Purpose: Verify mismatch cost lookup
```

### Scenario 3.4: Mixed Alignment
```
Aligned1: "A_C"
Aligned2: "_AC"
Calculation:
  - Position 0: A vs _ → gap = 30
  - Position 1: _ vs A → gap = 30
  - Position 2: C vs C → match = 0
Expected Cost: 60
Purpose: Verify combination of gaps and matches
```

### Scenario 3.5: Project Example Verification
```
Aligned1: "_A_CA_CACT__G__A_C_TAC_TGACTG_GTGA__C_TACTGACTGGACTGACTACTGACTGGTGACTACT_GACTG_G"
Aligned2: "TATTATTA_TACGCTATTATACGCGAC_GCG_GACGCGTA_T_AC__G_CT_ATTA_T_AC__GCGAC_GC_GGAC_GCG"
Expected Cost: 1296
Purpose: Verify against known correct output
```

---

## 4. Sequence Alignment Algorithm Tests

### Scenario 4.1: Empty Strings
```
Input: X="", Y=""
Expected: cost=0, aligned1="", aligned2=""
Purpose: Test base case
```

### Scenario 4.2: One Empty String
```
Input: X="A", Y=""
Expected: cost=30, aligned1="A", aligned2="_"
Purpose: Test when one string needs all gaps
```

### Scenario 4.3: Single Character Match
```
Input: X="A", Y="A"
Expected: cost=0, aligned1="A", aligned2="A"
Purpose: Simplest match case
```

### Scenario 4.4: Single Character Mismatch
```
Input: X="A", Y="C"
Options:
  1. Match A with C: cost = 110
  2. Gap both: A_ and _C: cost = 60
Expected: cost=60 (cheaper option)
Purpose: Verify algorithm chooses optimal solution
```

### Scenario 4.5: Identical Strings
```
Input: X="ACTG", Y="ACTG"
Expected: cost=0, aligned1="ACTG", aligned2="ACTG"
Purpose: Best case scenario
```

### Scenario 4.6: Alignment Properties

**Property 1: Equal Length**
```
For any alignment:
  len(aligned1) == len(aligned2)
Purpose: Fundamental alignment property
```

**Property 2: Character Order Preservation**
```
For any alignment:
  ''.join(c for c in aligned1 if c != '_') == original_X
  ''.join(c for c in aligned2 if c != '_') == original_Y
Purpose: Original strings must be preserved
```

**Property 3: No Double Gaps**
```
For any position i:
  NOT (aligned1[i] == '_' AND aligned2[i] == '_')
Purpose: Both can't be gaps at same position
```

### Scenario 4.7: Known Example (Project)
```
Input:
  X = generate_string("ACTG", [3, 6, 1, 1])
  Y = generate_string("TACG", [1, 2, 9, 2])
Expected:
  cost = 1296
  len(aligned1) == len(aligned2)
  All properties hold
Purpose: Main integration test
```

---

## 5. Dynamic Programming Correctness Tests

### Scenario 5.1: DP Table Initialization
```
For m x n table:
  dp[0][0] = 0
  dp[i][0] = i * delta for all i
  dp[0][j] = j * delta for all j
Purpose: Verify base cases
```

### Scenario 5.2: DP Recurrence
```
For each cell dp[i][j]:
  dp[i][j] = min(
    dp[i-1][j-1] + alpha[X[i-1]][Y[j-1]],  // match/mismatch
    dp[i-1][j] + delta,                      // gap in Y
    dp[i][j-1] + delta                       // gap in X
  )
Purpose: Verify recurrence relation
```

### Scenario 5.3: Backtracking Correctness
```
Starting from dp[m][n], trace back to dp[0][0]
At each step, verify we came from the cell that gave minimum cost
Purpose: Ensure alignment matches DP table
```

---

## 6. Edge Cases and Boundary Tests

### Scenario 6.1: Maximum Basic Algorithm Bounds
```
Test: j=10, k=10 insertions
String lengths: up to 2^10 * base_length
Purpose: Verify algorithm handles maximum allowed size
```

### Scenario 6.2: Highly Dissimilar Strings
```
Input: X="AAAA", Y="CCCC"
Expected: High cost (all mismatches or gaps)
Purpose: Worst case alignment
```

### Scenario 6.3: Repeated Characters
```
Test cases:
  - X="AAAA", Y="AAAA" → cost=0
  - X="AAAA", Y="CCCC" → high cost
Purpose: Test pattern handling
```

### Scenario 6.4: Long String Performance
```
Test with increasing sizes:
  - Length 100, 200, 400, 800...
Monitor: Time should grow O(n²)
Purpose: Verify complexity
```

---

## 7. Output Format Tests

### Scenario 7.1: Five Line Structure
```
Line 1: Integer (cost)
Line 2: String (aligned1)
Line 3: String (aligned2)
Line 4: Float (time_ms)
Line 5: Float (memory_kb)
Purpose: Verify output format
```

### Scenario 7.2: Valid Characters in Alignment
```
Aligned strings must contain only: A, C, G, T, _
Purpose: Ensure no invalid characters
```

### Scenario 7.3: File Creation
```
If output path doesn't exist, create it
Purpose: Verify file handling
```

---

## 8. Integration Tests

### Scenario 8.1: End-to-End Pipeline
```
Steps:
  1. Read input file
  2. Generate strings
  3. Run alignment
  4. Calculate metrics
  5. Write output file
Purpose: Test complete workflow
```

### Scenario 8.2: All Sample Test Cases
```
For each input/output pair in SampleTestCases:
  1. Run your implementation
  2. Verify cost matches
  3. Verify alignment is valid
Purpose: Validate against known correct outputs
```

---

## 9. Memory and Time Tests

### Scenario 9.1: Memory Measurement
```
Verify: process_memory() returns positive value
Purpose: Ensure measurement works
```

### Scenario 9.2: Time Measurement
```
Verify: Time increases with input size
Purpose: Ensure measurement works
```

### Scenario 9.3: Complexity Verification
```
Test sizes: n=100, 200, 400, 800
Expected: Time roughly quadruples when size doubles
Purpose: Verify O(n²) complexity
```

---

## 10. Error Handling Tests

### Scenario 10.1: Invalid Input File
```
What to test: Non-existent file path
Expected: Graceful error message
```

### Scenario 10.2: Malformed Input
```
Note: Project states "We will never give invalid input"
But good practice to handle anyway
```

---

## Test Execution Order

### Phase 1: Unit Tests (Fast)
1. String generation tests
2. Cost calculation tests
3. Small alignment tests

### Phase 2: Integration Tests (Medium)
4. Input parsing tests
5. Full alignment tests
6. Output format tests

### Phase 3: Sample Cases (Slower)
7. All provided sample test cases

### Phase 4: Performance Tests (Slowest)
8. Large input tests
9. Complexity verification

---

## Success Criteria

Your implementation should:

✅ Pass all unit tests (100%)
✅ Match costs on all sample test cases
✅ Produce valid alignments (equal length, no double gaps)
✅ Preserve original strings in alignments
✅ Handle edge cases correctly
✅ Show O(n²) time complexity
✅ Show O(n²) space complexity
✅ Produce correct output format
✅ Handle the project example correctly (cost=1296)

---

## Debugging Strategy

If tests fail:

1. **Start with simplest tests first**
   - Empty strings
   - Single characters
   - Small examples

2. **Verify each component independently**
   - String generation alone
   - Cost calculation alone
   - DP table construction alone
   - Backtracking alone

3. **Add debug output**
   - Print DP table
   - Print alignment being built
   - Print costs at each step

4. **Compare with expected**
   - Use provided sample outputs
   - Manual calculation for small cases

5. **Test incrementally**
   - Fix one test at a time
   - Don't move on until that test passes

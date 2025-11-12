# Examples Walkthrough

This document walks through concrete examples to help you understand each component.

---

## Example 1: String Generation

### Example 1.1: Single Insertion
```
Base string: "ACTG"
Indices: [3]

Step by step:
- Start: result = "ACTG"
- Process index 3:
  - Position 3 is 'G' (0-indexed: A=0, C=1, T=2, G=3)
  - Insert after position 3 means: keep "ACTG" + insert "ACTG" + keep ""
  - Result: "ACTG" + "ACTG" = "ACTGACTG"

Final result: "ACTGACTG"
Length: 4 → 8 (doubled!)
```

### Example 1.2: Multiple Insertions
```
Base string: "ACTG"
Indices: [3, 6, 1]

Iteration 1 (index=3):
- result = "ACTG"
- Insert after position 3: "ACTG" + "ACTG"
- result = "ACTGACTG"

Iteration 2 (index=6):
- result = "ACTGACTG"
- Position 6 is 'T' (A-C-T-G-A-C-T-G)
  - Positions: 0-1-2-3-4-5-6-7
- Insert after position 6: "ACTGACT" + "ACTGACTG" + "G"
- result = "ACTGACTACTGACTGG"

Iteration 3 (index=1):
- result = "ACTGACTACTGACTGG"
- Position 1 is 'C'
- Insert after position 1: "AC" + "ACTGACTACTGACTGG" + "TGACTACTGACTGG"
- result = "ACACTGACTACTGACTGGTGACTACTGACTGG"

Final result: "ACACTGACTACTGACTGGTGACTACTGACTGG"
Lengths: 4 → 8 → 16 → 32
```

**Your Implementation Hint**:
```python
def generate_string(base_string, indices):
    result = base_string
    for index in indices:
        # Split at position (index + 1)
        left_part = result[:index + 1]
        right_part = result[index + 1:]
        # Insert entire result in the middle
        result = left_part + result + right_part
    return result
```

---

## Example 2: DP Table for Simple Alignment

### Example 2.1: Aligning "A" and "A"
```
X = "A"
Y = "A"

DP Table (2x2):
      ""  A
  "" [ 0, 30]
  A  [30,  ?]

At dp[1][1]:
- Option 1 (match): dp[0][0] + alpha[('A','A')] = 0 + 0 = 0
- Option 2 (gap in Y): dp[0][1] + delta = 30 + 30 = 60
- Option 3 (gap in X): dp[1][0] + delta = 30 + 30 = 60
- Minimum: 0

Final DP Table:
      ""  A
  "" [ 0, 30]
  A  [30,  0]

Cost: 0
Alignment: A / A (perfect match)
```

### Example 2.2: Aligning "A" and "C"
```
X = "A"
Y = "C"

DP Table initialization:
      ""  C
  "" [ 0, 30]
  A  [30,  ?]

At dp[1][1]:
- Option 1 (mismatch): dp[0][0] + alpha[('A','C')] = 0 + 110 = 110
- Option 2 (gap in Y): dp[0][1] + delta = 30 + 30 = 60
- Option 3 (gap in X): dp[1][0] + delta = 30 + 30 = 60
- Minimum: 60

Final DP Table:
      ""  C
  "" [ 0, 30]
  A  [30, 60]

Cost: 60
Possible alignments: 
- "A_" / "_C" (gap in both)
- OR "_A" / "C_" (gap in both, different order)
```

### Example 2.3: Aligning "AC" and "AT"
```
X = "AC"
Y = "AT"

DP Table initialization:
      ""   A   T
  "" [ 0, 30, 60]
  A  [30,  ?,  ?]
  C  [60,  ?,  ?]

Fill cell dp[1][1] (A vs A):
- Match: dp[0][0] + 0 = 0
- Gap in Y: dp[0][1] + 30 = 60
- Gap in X: dp[1][0] + 30 = 60
- Minimum: 0

Fill cell dp[1][2] (A vs AT):
- Match A-T: dp[0][1] + alpha[('A','T')] = 30 + 94 = 124
- Gap in Y: dp[0][2] + 30 = 90
- Gap in X: dp[1][1] + 30 = 30
- Minimum: 30

Fill cell dp[2][1] (AC vs A):
- Match C-A: dp[1][0] + alpha[('C','A')] = 30 + 110 = 140
- Gap in Y: dp[1][1] + 30 = 30
- Gap in X: dp[2][0] + 30 = 90
- Minimum: 30

Fill cell dp[2][2] (AC vs AT):
- Match C-T: dp[1][1] + alpha[('C','T')] = 0 + 48 = 48
- Gap in Y: dp[1][2] + 30 = 60
- Gap in X: dp[2][1] + 30 = 60
- Minimum: 48

Final DP Table:
      ""   A   T
  "" [ 0, 30, 60]
  A  [30,  0, 30]
  C  [60, 30, 48]

Cost: 48
Alignment: AC / AT (C matches with T, mismatch cost 48)
```

---

## Example 3: Backtracking

### Using the "AC" vs "AT" example:
```
DP Table:
      ""   A   T
  "" [ 0, 30, 60]
  A  [30,  0, 30]
  C  [60, 30, 48]

Start at dp[2][2] = 48

Step 1: At (2,2), value is 48
- Check match: dp[1][1] + alpha[('C','T')] = 0 + 48 = 48 ✓
- This matches! So we matched C with T
- Add 'C' to aligned_x, 'T' to aligned_y
- Move to (1,1)

Step 2: At (1,1), value is 0
- Check match: dp[0][0] + alpha[('A','A')] = 0 + 0 = 0 ✓
- This matches! So we matched A with A
- Add 'A' to aligned_x, 'A' to aligned_y
- Move to (0,0)

Step 3: At (0,0), we're done!

Built (backwards):
- aligned_x = ['C', 'A']
- aligned_y = ['T', 'A']

After reversing:
- aligned_x = "AC"
- aligned_y = "AT"

Final alignment: AC / AT
```

---

## Example 4: Alignment with Gaps

### Aligning "ACT" and "A"
```
X = "ACT"
Y = "A"

DP Table:
       ""   A
  ""  [ 0, 30]
  A   [30,  0]
  C   [60, 30]
  T   [90, 60]

Backtracking from dp[3][1] = 60:

At (3,1):
- Check match T-A: dp[2][0] + alpha[('T','A')] = 60 + 94 = 154 ✗
- Check gap in Y: dp[2][1] + 30 = 30 + 30 = 60 ✓
- Add 'T' to aligned_x, '_' to aligned_y
- Move to (2,1)

At (2,1):
- Check match C-A: dp[1][0] + alpha[('C','A')] = 30 + 110 = 140 ✗
- Check gap in Y: dp[1][1] + 30 = 0 + 30 = 30 ✓
- Add 'C' to aligned_x, '_' to aligned_y
- Move to (1,1)

At (1,1):
- Check match A-A: dp[0][0] + 0 = 0 ✓
- Add 'A' to aligned_x, 'A' to aligned_y
- Move to (0,0)

Built (backwards): ['T', 'C', 'A'] and ['_', '_', 'A']
After reversing: "ACT" and "A__"

Final alignment: ACT / A__
Cost: 60 (one match, two gaps)
```

---

## Example 5: Cost Calculation

### Given alignment "A_C" and "_AC":
```
Position 0: 'A' vs '_'
- One is gap, so cost = delta = 30

Position 1: '_' vs 'A'
- One is gap, so cost = delta = 30

Position 2: 'C' vs 'C'
- Match, so cost = alpha[('C','C')] = 0

Total cost: 30 + 30 + 0 = 60
```

### Given alignment "AC" and "AT":
```
Position 0: 'A' vs 'A'
- Match, cost = alpha[('A','A')] = 0

Position 1: 'C' vs 'T'
- Mismatch, cost = alpha[('C','T')] = 48

Total cost: 0 + 48 = 48
```

---

## Example 6: Input File Parsing

### Input file content:
```
ACTG
3
6
TACG
1
```

### Parsing steps:
```
Lines: ["ACTG", "3", "6", "TACG", "1"]

Parsing first string:
- Line 0: "ACTG" → base_string1 = "ACTG"
- Line 1: "3" (is digit) → add to indices1
- Line 2: "6" (is digit) → add to indices1
- Line 3: "TACG" (not digit) → stop, this is base_string2

Result: string1 = generate_string("ACTG", [3, 6])

Parsing second string:
- Line 3: "TACG" → base_string2 = "TACG"
- Line 4: "1" (is digit) → add to indices2
- End of file

Result: string2 = generate_string("TACG", [1])

Return: (string1, string2)
```

---

## Example 7: Complete Workflow

### Input file "test_input.txt":
```
AC
1
AT
```

### Step-by-step execution:

1. **Parse input**:
   ```
   base1 = "AC", indices1 = [1]
   string1 = generate_string("AC", [1])
   - "AC" after index 1: "AC" + "AC" = "ACAC"
   
   base2 = "AT", indices2 = []
   string2 = "AT"
   ```

2. **Run alignment**:
   ```
   X = "ACAC"
   Y = "AT"
   
   Build DP table (5x3):
         ""   A   T
    ""  [ 0, 30, 60]
    A   [30,  ?,  ?]
    C   [60,  ?,  ?]
    A   [90,  ?,  ?]
    C   [120, ?,  ?]
   
   (Fill in using recurrence relation...)
   
   Final cost: dp[4][2]
   ```

3. **Backtrack** to get alignment strings

4. **Output to "test_output.txt"**:
   ```
   <cost>
   <aligned_string1>
   <aligned_string2>
   <time_ms>
   <memory_kb>
   ```

---

## Practice Problems

Try these by hand before implementing:

1. Generate string: base="AB", indices=[1, 2]
2. Align: X="AA", Y="AA"
3. Align: X="AG", Y="GA"
4. Calculate cost of: "A_G" / "_AG"

Solutions:
1. "AB" → "ABAB" → "ABABAB AB"
2. Cost 0, alignment: AA / AA
3. Cost depends on whether match or gaps chosen
4. Cost = 30 + 30 + 0 = 60

---

## Debugging Checklist

When your code doesn't work, check:

- [ ] String generation: Does each iteration double the length?
- [ ] DP table: Are base cases initialized correctly?
- [ ] DP recurrence: Are you using the right formula?
- [ ] Indexing: Remember dp[i][j] uses X[i-1] and Y[j-1]
- [ ] Backtracking: Starting from dp[m][n]?
- [ ] Reversal: Did you reverse the aligned strings?
- [ ] Cost calculation: Matching the logic correctly?
- [ ] Output format: Exactly 5 lines?

---

Good luck! Work through these examples carefully, and your implementation will be solid! 💪

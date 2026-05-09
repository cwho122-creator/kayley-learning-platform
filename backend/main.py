"""FastAPI main application - Kayley's ADHD-Friendly Learning Platform."""
import json
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager

from backend.database import init_db, SessionLocal
from backend.routers import auth_router, lessons_router, quiz_router, progress_router
from backend.models import Subject, Unit, Lesson, Quiz, QuizQuestion, RAPCard


def seed_content():
    """Seed the database with MYP Year 8 curriculum content."""
    db = SessionLocal()
    
    # Check if already seeded
    if db.query(Subject).first():
        db.close()
        return
    
    # ─── Create Subjects ───────────────────────────────────────────────────────
    math_subject = Subject(name="Math", color="#6366F1")  # Indigo
    science_subject = Subject(name="Science", color="#10B981")  # Emerald
    db.add_all([math_subject, science_subject])
    db.commit()
    
    # ═══════════════════════════════════════════════════════════════════════════
    # MATH UNITS & LESSONS
    # ═══════════════════════════════════════════════════════════════════════════
    
    math_units_data = [
        {
            "title": "Unit 1: The Same But Different",
            "unit_number": 1,
            "description": "Introduction to algebraic expressions, directed numbers, and simplifying expressions.",
            "week_start": 1,
            "week_end": 7,
            "lessons": [
                {
                    "title": "Algebraic Expressions & Notation",
                    "lesson_number": 1,
                    "duration_minutes": 10,
                    "content": """# 📝 Algebraic Expressions & Notation

Welcome! Today we're learning about **algebraic expressions** — the building blocks of algebra! 🎉

## What is an Algebraic Expression?

An algebraic expression is like a math sentence that uses:
- **Numbers** (like 3, 5, 100)
- **Letters** (like x, y, n) — these are called **variables**
- **Operation signs** (+, −, ×, ÷)

### Examples:
- `x + 5` → "x plus 5"
- `3y - 7` → "3 times y, minus 7"
- `2a + 3b` → "2 times a, plus 3 times b"

## The RAP Strategy Reminder 📋

When you see a problem, use RAP:
1. **R**ead it carefully
2. **A**sk: "What is it asking?"
3. **P**ut your answer in the box

## Key Words to Spot 🔍

| Key Word | Means |
|----------|-------|
| variable | a letter (x, y, n) |
| term | a single piece (3x, 5, y) |
| expression | math sentence with + or − |
| coefficient | the number in front of a letter |

## Try It! 🎯

Write these as algebraic expressions:
1. "5 more than x" → `x + 5`
2. "twice a number" → `2n`
3. "7 less than y" → `y - 7`

---

**🎯 Movement Break! Stand up and stretch! You earned it!** 🧘

---

## Color Coding Helper

Remember:
- Positive numbers: 🔵 BLUE
- Negative numbers: 🔴 RED
- Unknowns (variables): 🟢 GREEN

---

**Great job! You've completed this lesson!** ⭐""",
                    "has_movement_break": True,
                    "movement_break_after_minutes": 7
                },
                {
                    "title": "Substitution into Expressions",
                    "lesson_number": 2,
                    "duration_minutes": 10,
                    "content": """# 🔄 Substitution into Expressions

## What is Substitution?

**Substitution** means putting a number in place of a letter/variable.

### Example:
If `x = 4`, find `x + 3`
- Replace x with 4: `4 + 3`
- Answer: `7` ✅

## Step-by-Step Checklist ✓

**Step 1:** Find the variable (letter)
**Step 2:** Find what number equals
**Step 3:** Replace (substitute) the letter with the number
**Step 4:** Calculate!

## Let's Practice Together!

### Example 1:
If `a = 5`, find `2a + 1`
- Step 1: Variable is `a`
- Step 2: `a = 5`
- Step 3: `2(5) + 1`  *(2 times 5)*
- Step 4: `10 + 1 = 11` ✅

### Example 2:
If `n = 3`, find `4n - 5`
- Step 1: Variable is `n`
- Step 2: `n = 3`
- Step 3: `4(3) - 5`
- Step 4: `12 - 5 = 7` ✅

## Watch Out! ⚠️

- `3x` means `3 × x`
- `ab` means `a × b`
- Numbers next to letters mean MULTIPLY!

---

**🧘 Movement Break: Do 5 jumping jacks!** 

---

## Try These! (Max 3 steps each)

**Remember: Use your checklist!**

1. If `b = 6`, find `b + 4` → `6 + 4 = 10` ✅
2. If `x = 3`, find `5x` → `5 × 3 = 15` ✅
3. If `y = 8`, find `y - 3` → `8 - 3 = 5` ✅

---

**Fantastic work! You're getting it!** 🌟""",
                    "has_movement_break": True,
                    "movement_break_after_minutes": 7
                },
                {
                    "title": "Directed Numbers - Addition & Subtraction",
                    "lesson_number": 3,
                    "duration_minutes": 10,
                    "content": """# ➕➖ Directed Numbers: Adding & Subtracting

## What are Directed Numbers? 📊

Directed numbers are positive (+) and negative (−) numbers.
Think of them like a **number line**:

```
←───●───●───●───●───●───●───●───→
  -4  -3  -2  -1   0  +1  +2  +3
```

## Color Coding Rule 🎨

- **Positive numbers**: 🔵 BLUE (above zero)
- **Negative numbers**: 🔴 RED (below zero)

## Adding Directed Numbers

### Rule 1: Same Signs →
**Same signs = ADD, keep the sign!**

- `(+3) + (+5) = +8`  (blue + blue = blue 8)
- `(−3) + (−5) = −8`  (red + red = red 8)

### Rule 2: Different Signs ↔
**Different signs = SUBTRACT, keep the bigger sign!**

- `(+7) + (−4) = +3`  (7 blue, 4 red → 3 blue)
- `(−7) + (+4) = −3`  (7 red, 4 blue → 3 red)

## Visual Number Line 🔢

**Example: (+5) + (−3)**
1. Start at +5 (5 steps to the right of zero)
2. Move 3 steps LEFT (because −3)
3. Land on +2 ✅

## Subtracting Directed Numbers

**Turn it into addition!**

`(+6) − (+4)` = `(+6) + (−4)` = `+2`

`(−6) − (−3)` = `(−6) + (+3)` = `−3`

### Trick:
**Subtracting = Adding the opposite**

## Your Checklist ✓

1. Are the signs the SAME or DIFFERENT?
2. Same? → ADD and keep sign
3. Different? → SUBTRACT, keep bigger number's sign

---

**🏃 Movement Break! March in place for 10 seconds!**

---

## Practice Time!

1. `(+4) + (+6) =` → `+10` ✅
2. `(−3) + (−7) =` → `−10` ✅
3. `(+8) + (−5) =` → `+3` ✅
4. `(+6) − (+2) =` → `+4` ✅

---

**Brilliant! Directed numbers are now your friends!** 🎉""",
                    "has_movement_break": True,
                    "movement_break_after_minutes": 7
                },
                {
                    "title": "Directed Numbers - Multiplication & Division",
                    "lesson_number": 4,
                    "duration_minutes": 10,
                    "content": """# ✖️➗ Directed Numbers: Multiplying & Dividing

## The Magic Rule! ✨

**Same Signs → POSITIVE (+)**  
**Different Signs → NEGATIVE (−)**

## Multiplication Rules

| Signs | Result | Example |
|-------|--------|---------|
| (+)(+) | + | `(+3) × (+4) = +12` |
| (−)(−) | + | `(−3) × (−4) = +12` |
| (+)(−) | − | `(+3) × (−4) = −12` |
| (−)(+) | − | `(−3) × (+4) = −12` |

## Division Rules (Same as multiplication!)

| Signs | Result | Example |
|-------|--------|---------|
| (+)(+) | + | `(+12) ÷ (+3) = +4` |
| (−)(−) | + | `(−12) ÷ (−3) = +4` |
| (+)(−) | − | `(+12) ÷ (−3) = −4` |
| (−)(+) | − | `(−12) ÷ (+3) = −4` |

## Memory Trick! 🧠

**"Friend or Foe?"**
- Same sign = FRIEND = POSITIVE 😊
- Different sign = FOE = NEGATIVE 😠

## Step-by-Step Checklist ✓

**Step 1:** Ignore signs, do the operation
**Step 2:** Count negatives... are there 0 or 2? → POSITIVE
**Step 3:** Are there 1 or 3 negatives? → NEGATIVE

## Practice!

1. `(−4) × (−3) = +12` ✅ (two negatives = positive!)
2. `(+5) × (−2) = −10` ✅ (different = negative)
3. `(−20) ÷ (+4) = −5` ✅ (different = negative)
4. `(−6) × (−2) × (−1) = −12` ✅ (three negatives = negative)

---

**🧘 Stretch Break: Touch your toes and count to 5!**

---

**You're mastering this! Keep going!** 💪""",
                    "has_movement_break": True,
                    "movement_break_after_minutes": 7
                },
                {
                    "title": "Like and Unlike Terms",
                    "lesson_number": 5,
                    "duration_minutes": 10,
                    "content": """# 🔍 Like and Unlike Terms

## What are Terms? 📦

A **term** is a single piece of an expression:
- Can be a number: `5`
- Can be a variable: `x`
- Can be both: `3x`

## Like Terms = Same "Flavor" 🍨

**Like terms** have the SAME variables with the SAME powers.

### Examples of Like Terms:
- `3x` and `5x` ✅ (both have x)
- `2y` and `7y` ✅ (both have y)
- `4` and `9` ✅ (both are plain numbers)
- `x²` and `3x²` ✅ (both have x²)

## Unlike Terms = Different "Flavor" 🍨🍦

**Unlike terms** have different variables or powers.

### Examples:
- `3x` and `3y` ❌ (x vs y)
- `2x` and `2x²` ❌ (x vs x²)
- `5` and `5n` ❌ (number vs variable)

## Why Does This Matter? 🤔

You can ONLY combine (add/subtract) **LIKE terms**!

### ✅ Correct:
- `3x + 5x = 8x`
- `7y - 2y = 5y`
- `4 + 9 = 13`

### ❌ Wrong:
- `3x + 5y` cannot combine (different letters!)
- `2 + 3n` cannot combine (number vs variable!)

## Your Checklist ✓

**Step 1:** Circle the coefficient (number in front)
**Step 2:** Underline the variable part
**Step 3:** Are the underlines the SAME? → LIKE terms!

---

**🏃 Movement Break: Stand up and spin around once!**

---

## Practice - Like or Unlike?

1. `4x` and `6x` → **LIKE** ✅ (both x)
2. `3a` and `3b` → **UNLIKE** ❌ (different letters)
3. `7` and `7` → **LIKE** ✅ (both numbers)
4. `2m²` and `5m` → **UNLIKE** ❌ (different powers!)

---

**Excellent! You can spot the difference!** 👏""",
                    "has_movement_break": True,
                    "movement_break_after_minutes": 7
                },
                {
                    "title": "Simplifying Algebraic Expressions",
                    "lesson_number": 6,
                    "duration_minutes": 10,
                    "content": """# ✂️ Simplifying Algebraic Expressions

## What Does "Simplify" Mean?

**Simplify** = make it smaller and easier!

Like cleaning up your room — get rid of the clutter! 🧹

## The Process

1. **Find like terms** (same variable)
2. **Combine them** (add or subtract coefficients)
3. **Write the simplified answer**

## Step-by-Step Example

Simplify: `3x + 5 + 2x - 3`

**Step 1:** Group like terms
- `3x + 2x` (both have x)
- `5 - 3` (both are plain numbers)

**Step 2:** Combine each group
- `3x + 2x = 5x`
- `5 - 3 = 2`

**Step 3:** Write it together
- `5x + 2` ✅

## Another Example

Simplify: `4a + 3b - 2a + 7 - b`

**Step 1:** Group like terms
- `4a - 2a` (a terms)
- `3b - b` (b terms)
- `7` (numbers)

**Step 2:** Combine
- `4a - 2a = 2a`
- `3b - b = 2b`
- `7`

**Step 3:** Answer: `2a + 2b + 7` ✅

## Your Checklist ✓

1. Find terms with the SAME variable
2. Circle coefficients, add/subtract them
3. Keep the variable part the same
4. Write numbers at the end

---

**🧘 Movement Break: Take 3 deep breaths!**

---

## Practice

1. `2x + 4x = 6x` ✅
2. `5y - 2y = 3y` ✅
3. `3a + 4 + a + 2 = 4a + 6` ✅

---

**You're simplifying like a pro!** 🌟""",
                    "has_movement_break": True,
                    "movement_break_after_minutes": 7
                }
            ]
        },
        {
            "title": "Unit 2: Patterns and Relations",
            "unit_number": 2,
            "description": "Algebraic equations, linear relationships, and graphing.",
            "week_start": 8,
            "week_end": 15,
            "lessons": [
                {
                    "title": "One-Step Equations",
                    "lesson_number": 1,
                    "duration_minutes": 10,
                    "content": """# 🎯 One-Step Equations

## What is an Equation?

An **equation** shows that two things are EQUAL using the `=` sign.

```
x + 5 = 10
↑      ↑
this   equals this
```

## The Goal 🏆

**Solve for x** = find what number x equals!

## One-Step Equation Rules

Whatever you do to ONE side, you MUST do to the OTHER!

## Addition Equations

`x - 3 = 7`

**Think:** What minus 3 equals 7?
**Answer:** x = 10

**To undo subtraction, ADD!**
```
x - 3 = 7
+ 3  + 3
x    = 10
```

## Subtraction Equations

`x + 4 = 9`

**Think:** What plus 4 equals 9?
**Answer:** x = 5

**To undo addition, SUBTRACT!**
```
x + 4 = 9
- 4  - 4
x    = 5
```

## Your Checklist ✓

1. Find what operation is being done to x (+ − × ÷)
2. Do the OPPOSITE operation to BOTH sides
3. Write your answer: x = ___

---

**🏃 Movement Break: Run in place for 10 seconds!**

---

## Practice

1. `x + 6 = 15` → `x = 9` ✅
2. `x - 4 = 10` → `x = 14` ✅
3. `x + 8 = 20` → `x = 12` ✅

---

**You solved it! Amazing!** 🎉""",
                    "has_movement_break": True,
                    "movement_break_after_minutes": 7
                },
                {
                    "title": "Two-Step Equations",
                    "lesson_number": 2,
                    "duration_minutes": 10,
                    "content": """# 🎯 Two-Step Equations

## What's Different?

Two-step equations have **TWO operations** to undo!

## Example

`3x + 5 = 20`

### Step 1: Undo Addition/Subtraction FIRST
```
3x + 5 = 20
- 5    - 5     ← undo +5
3x    = 15
```

### Step 2: Undo Multiplication/Division SECOND
```
3x = 15
÷ 3   ÷ 3     ← undo ×3
x  = 5
```

**Answer: x = 5** ✅

## The Golden Rule 💛

**Order matters!**

1. **FIRST:** Undo + or −
2. **SECOND:** Undo × or ÷

## Your Checklist ✓

1. Is there a + or −? Undo it FIRST!
2. Is there a × or ÷? Undo it SECOND!
3. Write your answer

---

**🧘 Movement Break: Do 5 arm circles!**

---

## Practice

1. `2x + 3 = 11`
   - `2x = 8`
   - `x = 4` ✅

2. `4x - 5 = 15`
   - `4x = 20`
   - `x = 5` ✅

---

**You're an equation solver! 🏆**""",
                    "has_movement_break": True,
                    "movement_break_after_minutes": 7
                },
                {
                    "title": "Linear Patterns and Relationships",
                    "lesson_number": 3,
                    "duration_minutes": 10,
                    "content": """# 📈 Linear Patterns

## What is a Pattern? 🔍

A **pattern** is something that REPEATS or GROWS the same way each time!

## Linear Patterns

**Linear** = increases or decreases by the SAME amount each step!

### Example:
```
Term:   1    2    3    4
Value:  3    5    7    9
         ↗   ↗   ↗
        +2  +2  +2
```
Pattern: **Add 2 each time!**

## Finding the Rule

**Step 1:** Look at the CHANGE between terms
**Step 2:** Find the PATTERN
**Step 3:** Write the RULE

### If term is n:
Pattern above: starts at 1, adds 2 each time
Rule: `2n + 1`

Check: n=1 → 2(1)+1 = 3 ✅

## Visual Pattern Example

🟦 🟦
🟦 🟦 🟦
🟦 🟦 🟦 🟦

Term 1: 2 squares
Term 2: 3 squares
Term 3: 4 squares

Pattern: Add 1 each time
Rule: `n + 1`

---

**🏃 Movement Break: Jump like a frog! 🐸**

---

## Your Checklist ✓

1. Write out the terms
2. Find the difference (change)
3. Is it the SAME each time? → LINEAR!
4. Write the rule

---

**Patterns are everywhere! Great job!** 🌟""",
                    "has_movement_break": True,
                    "movement_break_after_minutes": 7
                },
                {
                    "title": "Graphing Linear Equations",
                    "lesson_number": 4,
                    "duration_minutes": 10,
                    "content": """# 📊 Graphing Linear Equations

## The Coordinate Plane

```
        y
        ↑
   4    |
   3    |
   2    |
   1    |
  ──────┼────────→ x
  -4   -1    1    2    3    4
  -1    |
  -2    |
  -3    |
  -4    |
```

## Points

A point = `(x, y)`
- First number = x (left/right)
- Second number = y (up/down)

## Example: Graph y = 2x + 1

**Step 1:** Make a TABLE of values
| x | y = 2x + 1 |
|---|------------|
| 0 | 1 |
| 1 | 3 |
| 2 | 5 |
| 3 | 7 |

**Step 2:** Plot the points
- (0, 1)
- (1, 3)
- (2, 5)
- (3, 7)

**Step 3:** Draw a LINE through them!

## Your Checklist ✓

1. Pick 3 x-values (0, 1, 2 works well)
2. Calculate y for each
3. Plot the points
4. Connect with a straight line

---

**🧘 Movement Break: Draw a big circle in the air with your arms!**

---

## Try Graphing!

For `y = x + 2`:
| x | y |
|---|---|
| 0 | 2 |
| 1 | 3 |
| 2 | 4 |

Plot: (0,2), (1,3), (2,4) and connect!

---

**You're graphing like a mathematician!** 🧮""",
                    "has_movement_break": True,
                    "movement_break_after_minutes": 7
                }
            ]
        },
        {
            "title": "Unit 3: Measurement",
            "unit_number": 3,
            "description": "Area, perimeter, volume, and scale.",
            "week_start": 16,
            "week_end": 22,
            "lessons": [
                {
                    "title": "Area of 2D Shapes",
                    "lesson_number": 1,
                    "duration_minutes": 10,
                    "content": """# 📐 Area of 2D Shapes

## What is Area? 📏

**Area** = how much SPACE is inside a shape!

We measure in **square units** (like cm², m²)

## Square
```
█████
█████
█████

Area = side × side
A = s²
```
If side = 4 cm → A = 4 × 4 = **16 cm²**

## Rectangle
```
████████████
████████████

Area = length × width
A = l × w
```
If l = 8 cm, w = 3 cm → A = 8 × 3 = **24 cm²**

## Triangle
```
    △
   ╱ ╲
  ╱   ╲
 ╱____╲

Area = ½ × base × height
A = ½bh
```
If base = 6 cm, height = 4 cm → A = ½ × 6 × 4 = **12 cm²**

## Circle
```
    ◯
   ╱  ╲
  │    │
   ╲  ╱

Area = π × radius²
A = πr²
```
If radius = 3 cm → A = π × 9 ≈ **28.27 cm²**

## Your Checklist ✓

1. Identify the shape
2. Find the formula
3. Plug in the numbers
4. Calculate!

---

**🏃 Movement Break: Do 5 star jumps! ⭐**

---

## Practice

1. Square: side = 5 cm → 25 cm² ✅
2. Rectangle: l = 7, w = 4 → 28 cm² ✅
3. Triangle: b = 8, h = 3 → 12 cm² ✅

---

**Area master! Well done!** 🎉""",
                    "has_movement_break": True,
                    "movement_break_after_minutes": 7
                },
                {
                    "title": "Perimeter",
                    "lesson_number": 2,
                    "duration_minutes": 10,
                    "content": """# 📏 Perimeter

## What is Perimeter? 🔲

**Perimeter** = the DISTANCE AROUND the outside of a shape!

Think: If you walked around a field, how far would you walk?

## How to Calculate

**ADD UP ALL THE SIDES!**

## Square
```
──────
│    │
│    │
──────

P = 4 × side
```
If side = 5 cm → P = 4 × 5 = **20 cm**

## Rectangle
```
────────────
│          │
────────────

P = 2 × (length + width)
P = 2(l + w)
```
If l = 8 cm, w = 3 cm → P = 2(8 + 3) = **22 cm**

## Triangle
```
    △
   ╱ ╲
  ╱   ╲

P = side₁ + side₂ + side₃
```
If sides = 3, 4, 5 cm → P = 3 + 4 + 5 = **12 cm**

## Circle (Circumference)
```
    ◯

C = 2 × π × radius
C = 2πr
```
If r = 4 cm → C = 2 × π × 4 ≈ **25.13 cm**

## Your Checklist ✓

1. Count all the sides
2. Add them together (or use the formula!)
3. Don't forget the unit!

---

**🧘 Movement Break: Trace a square in the air with your finger!**

---

## Practice

1. Square: side = 6 cm → 24 cm ✅
2. Rectangle: l = 10, w = 5 → 30 cm ✅
3. Triangle: 3 + 4 + 5 = 12 cm ✅

---

**Perimeter pro! Great job!** 🌟""",
                    "has_movement_break": True,
                    "movement_break_after_minutes": 7
                },
                {
                    "title": "Volume of 3D Shapes",
                    "lesson_number": 3,
                    "duration_minutes": 10,
                    "content": """# 📦 Volume of 3D Shapes

## What is Volume? 🎲

**Volume** = how much SPACE is INSIDE a 3D shape!

We measure in **cubic units** (like cm³, m³)

## Cube
```
    ┌────┐
   /│   /│
  └────┐│
  │ │  │ │
  │ └──│─┘
  │/   │
  └────┘

Volume = side³
V = s³
```
If side = 3 cm → V = 3³ = **27 cm³**

## Rectangular Prism (Cuboid)
```
    ┌────────┐
   /│       /│
  / │      / │
  └────────┐ │
  │  └─────┼─┘
  │ /      │/
  └────────┘

Volume = length × width × height
V = l × w × h
```
If l = 5, w = 3, h = 4 → V = 5 × 3 × 4 = **60 cm³**

## Cylinder
```
    ┌──────┐
    │ ○○○ │  ← circle top
    └──────┘
   ╱      ╲
  │        │
  │        │
   ───────

Volume = π × radius² × height
V = πr²h
```
If r = 2, h = 5 → V = π × 4 × 5 ≈ **62.83 cm³**

## Your Checklist ✓

1. Identify the 3D shape
2. Remember the formula
3. Plug in numbers
4. Calculate!

---

**🏃 Movement Break: Pretend you're filling a box! Stack imaginary blocks!**

---

## Practice

1. Cube: s = 4 cm → 64 cm³ ✅
2. Cuboid: l = 6, w = 2, h = 3 → 36 cm³ ✅

---

**Volume virtuoso!** 🎉""",
                    "has_movement_break": True,
                    "movement_break_after_minutes": 7
                },
                {
                    "title": "Scale and Proportion",
                    "lesson_number": 4,
                    "duration_minutes": 10,
                    "content": """# 🔍 Scale and Proportion

## What is Scale? 📐

**Scale** = how much bigger or smaller a drawing is compared to real life!

### Example:
Scale 1:100 means **1 cm on paper = 100 cm in real life**

## Reading Scale

**Scale Factor** = the ratio between drawing and real

If a drawing says "Scale 1:2":
- Real object is **2 times bigger** than the drawing
- Drawing is **½ the size** of real object

## Finding Real Measurements

**Real = Drawing × Scale Factor**

If a room drawing is 5 cm and scale is 1:100:
- Real = 5 cm × 100 = **500 cm = 5 m** ✅

## Finding Drawing Measurements

**Drawing = Real ÷ Scale Factor**

If a 3 m wall is drawn at scale 1:50:
- Drawing = 3 m ÷ 50 = 0.06 m = **6 cm** ✅

## Your Checklist ✓

1. Find the scale (e.g., 1:100)
2. Is it缩小 (scale down) or 放大 (scale up)?
3. Multiply or divide accordingly!

---

**🧘 Movement Break: Walk like a giant (big steps) then like an ant (tiny steps)!**

---

## Practice

1. Scale 1:10, drawing = 4 cm → Real = 40 cm ✅
2. Scale 1:50, real = 5 m = 500 cm → Drawing = 10 cm ✅

---

**Scale expert! Fantastic!** 🌟""",
                    "has_movement_break": True,
                    "movement_break_after_minutes": 7
                }
            ]
        },
        {
            "title": "Unit 4: Statistics and Geometry",
            "unit_number": 4,
            "description": "Data representation, probability, and geometry.",
            "week_start": 23,
            "week_end": 30,
            "lessons": [
                {
                    "title": "Data Collection and Representation",
                    "lesson_number": 1,
                    "duration_minutes": 10,
                    "content": """# 📊 Data Collection and Representation

## What is Data? 📋

**Data** = information we collect!

### Types:
- **Categorical** = categories (color, type, name)
- **Numerical** = numbers (age, height, score)

## Collecting Data

### Survey Questions:
- What is your favorite fruit?
- How many pets do you have?

### Tally Chart:
```
Favorite Fruit | Tally     | Count
───────────────┼───────────┼──────
Apple          | ||||      | 4
Banana         | |||| |    | 6
Orange         | |||       | 3
```

## Bar Graph
```
Apple   ████
Banana  ██████
Orange  ███
         ↑  ↑  ↑
         4  6  3
```

## Pie Chart
```
    Apple 25%
   ┌─────┐
  │       │
  │  50%  │ Banana
  │ Orange│
  │  25%  │
  └─────┘
```

## Your Checklist ✓

1. Collect your data (survey, observation)
2. Tally and count
3. Choose the right graph
4. Draw it clearly!

---

**🏃 Movement Break: Dance for 10 seconds to your favorite song! 💃**

---

## Practice

Create a tally chart for favorite subjects:
- Math: 8 students
- Science: 6 students
- English: 5 students

---

**Data detective! Excellent work!** 🔍""",
                    "has_movement_break": True,
                    "movement_break_after_minutes": 7
                },
                {
                    "title": "Probability Basics",
                    "lesson_number": 2,
                    "duration_minutes": 10,
                    "content": """# 🎲 Probability Basics

## What is Probability? 🎯

**Probability** = how LIKELY something is to happen!

### Words we use:
- **Certain** = will definitely happen (100%)
- **Likely** = probably will happen
- **Even chance** = 50/50
- **Unlikely** = probably won't happen
- **Impossible** = can never happen (0%)

## The Probability Scale

```
0%          50%         100%
│───────────│───────────│
Impossible  Even       Certain
```

## Calculating Probability

```
Probability = Number of ways it can happen
              ─────────────────────────────
              Total number of possible outcomes
```

### Example: Rolling a 4 on a die

- Ways to get 4: **1** (just the 4)
- Total outcomes: **6** (1, 2, 3, 4, 5, 6)

P(4) = 1/6 ≈ **16.7%**

## Probability Words

| Word | Fraction | Percentage |
|------|----------|------------|
| Impossible | 0 | 0% |
| Unlikely | 1/4 | 25% |
| Even | 1/2 | 50% |
| Likely | 3/4 | 75% |
| Certain | 1 | 100% |

## Your Checklist ✓

1. Count favorable outcomes (what you want)
2. Count total outcomes (all possibilities)
3. Write as fraction, then convert to %

---

**🧘 Movement Break: Spin once and land on one foot - 50% chance of wobble! 😄**

---

## Practice

1. Coin flip (heads): 1/2 = 50% ✅
2. Rolling even number (2,4,6): 3/6 = 50% ✅
3. Rolling 7 on a die: 0/6 = 0% ✅

---

**Probability master! Well done!** 🎉""",
                    "has_movement_break": True,
                    "movement_break_after_minutes": 7
                },
                {
                    "title": "Angles and Triangles",
                    "lesson_number": 3,
                    "duration_minutes": 10,
                    "content": """# 📐 Angles and Triangles

## What is an Angle? 🔺

An angle is formed by two lines that meet at a point!

```
    ╱
   ╱  
  ╱   
 ╱    
╱______
```

## Types of Angles

| Type | Size | Example |
|------|------|---------|
| Acute | < 90° | |
| Right | = 90° | |
| Obtuse | > 90° but < 180° | |
| Straight | = 180° | |
| Reflex | > 180° | |

## Triangles

### By Angles:
- **Acute triangle**: All angles < 90°
- **Right triangle**: One angle = 90°
- **Obtuse triangle**: One angle > 90°

### By Sides:
- **Equilateral**: All sides equal (3 equal angles = 60° each)
- **Isosceles**: 2 equal sides, 2 equal angles
- **Scalene**: No equal sides, no equal angles

## Triangle Angle Rule 💡

**All triangles add up to 180°!**

### Example:
A triangle
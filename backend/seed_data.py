"""Seed the database with content."""
import json
from datetime import datetime
from backend.database import SessionLocal
from backend.models import (
    Subject, Unit, Lesson, Quiz, QuizQuestion, RAPCard
)


def seed_database():
    """Add all lessons, quizzes, and RAP cards to the database."""
    db = SessionLocal()
    
    # Check if already seeded
    if db.query(Subject).first():
        print("✅ Database already has content! Skipping seed.")
        db.close()
        return
    
    try:
        # ===== CREATE MATH SUBJECT =====
        math_subject = Subject(name="Math", color="#6366F1")
        db.add(math_subject)
        db.flush()
        
        # ===== MATH UNIT 1 =====
        unit1 = Unit(
            subject_id=math_subject.id,
            title="Unit 1: The Same But Different - Expressions & Directed Numbers",
            unit_number=1,
            description="Introduction to algebraic expressions and working with positive and negative numbers.",
            week_start=1,
            week_end=7
        )
        db.add(unit1)
        db.flush()
        
        # Lesson 1: Algebraic Expressions
        lesson1 = Lesson(
            unit_id=unit1.id,
            title="Algebraic Expressions & Notation",
            lesson_number=1,
            duration_minutes=8,
            content="""# 📝 Algebraic Expressions

An **algebraic expression** uses numbers, letters, and math symbols!

## What is a letter in math?
- A letter (like `x`, `y`, or `a`) represents a **number we don't know yet** 🤔
- We call it a **variable**

## Examples:
- `x + 5` means: some number plus 5
- `3y` means: 3 times some number
- `2x - 7` means: 2 times some number minus 7

## Key words:
- **Term** = a part of an expression (like `3x` or `5`)
- **Coefficient** = the number in front of the letter (like the `3` in `3x`)
- **Variable** = the letter (like the `x`)

Try: What's the coefficient in `7y`? 🎯 Answer: 7!
""",
            has_movement_break=True,
            movement_break_after_minutes=7
        )
        db.add(lesson1)
        db.flush()
        
        # RAP Cards for Lesson 1
        rap1_read = RAPCard(
            lesson_id=lesson1.id,
            card_number=1,
            title="📖 READ",
            description="Read the problem carefully and underline key words",
            example_text="Read: 'What is the coefficient in 5x + 3?'\nUnderline: coefficient, 5x",
            checklist_items='["Read slowly", "Underline key words", "Look for numbers and letters"]'
        )
        db.add(rap1_read)
        
        rap1_ask = RAPCard(
            lesson_id=lesson1.id,
            card_number=2,
            title="❓ ASK",
            description="Ask yourself: What am I looking for? What do I know?",
            example_text="Ask: What is a coefficient? (the number in front of the letter)",
            checklist_items='["What am I looking for?", "Do I know all the key words?", "What are the clues?"]'
        )
        db.add(rap1_ask)
        
        rap1_put = RAPCard(
            lesson_id=lesson1.id,
            card_number=3,
            title="✍️ PUT",
            description="Put your answer: Write the coefficient clearly",
            example_text="Answer: The coefficient is 5",
            checklist_items='["Write the answer clearly", "Check my work", "Is it labeled?"]'
        )
        db.add(rap1_put)
        db.flush()
        
        # Quiz for Lesson 1
        quiz1 = Quiz(
            lesson_id=lesson1.id,
            title="Algebraic Expressions Quiz",
            max_questions=3,
            passing_score=70
        )
        db.add(quiz1)
        db.flush()
        
        q1_1 = QuizQuestion(
            quiz_id=quiz1.id,
            question_number=1,
            question_text="What does 4x mean?",
            question_type="multiple_choice",
            options=json.dumps(["4 + x", "4 times x", "x divided by 4", "x to the power 4"]),
            correct_answer="4 times x",
            explanation="When a number is right next to a letter (no sign between them), it means MULTIPLY! So 4x = 4 × x 🎯",
            points=10,
            color_hint="4x"
        )
        db.add(q1_1)
        
        q1_2 = QuizQuestion(
            quiz_id=quiz1.id,
            question_number=2,
            question_text="In the expression 7y + 3, what is the coefficient of y?",
            question_type="numeric",
            options=None,
            correct_answer="7",
            explanation="The coefficient is the number IN FRONT of the letter! In 7y, the coefficient is 7. The +3 is separate. ✨",
            points=10,
            color_hint="7y"
        )
        db.add(q1_2)
        
        q1_3 = QuizQuestion(
            quiz_id=quiz1.id,
            question_number=3,
            question_text="Write an expression for: 'A number multiplied by 5, then add 2'",
            question_type="free_response",
            options=None,
            correct_answer="5x + 2",
            explanation="Let the unknown number be x. Multiply by 5 = 5x. Then add 2 = 5x + 2. Perfect! 🌟",
            points=10,
            color_hint="expression"
        )
        db.add(q1_3)
        db.flush()
        
        # ===== LESSON 2: DIRECTED NUMBERS =====
        lesson2 = Lesson(
            unit_id=unit1.id,
            title="Directed Numbers: Positive & Negative",
            lesson_number=2,
            duration_minutes=10,
            content="""# 🌡️ Directed Numbers (Positive & Negative)

**Directed numbers** tell us how far from zero, AND in which direction!

## Think of a thermometer 🌡️
- **Above zero** = POSITIVE (warm! +)
- **Below zero** = NEGATIVE (cold! -)
- **Right at zero** = ZERO

## Number Line:
```
-5  -4  -3  -2  -1   0   +1  +2  +3  +4  +5
 ←-←-←-←-←- COLD - ZERO - WARM -→-→-→-→-→
```

## Examples:
- Temperature is -3°C (3 degrees BELOW zero) ❄️
- Your score is +5 (5 points ABOVE zero) 🎉
- Money: -$10 means you OWE $10 💸

## Rules for Adding:
- Same sign? ADD them, keep the sign ➕
- Different signs? SUBTRACT them, keep the BIG sign ⚖️

### Example: (-3) + (-2)
- Both negative → ADD: 3 + 2 = 5 → Answer: -5

### Example: 7 + (-3)
- Different signs → SUBTRACT: 7 - 3 = 4 → Answer: +4
""",
            has_movement_break=True,
            movement_break_after_minutes=7
        )
        db.add(lesson2)
        db.flush()
        
        # RAP Cards for Lesson 2
        rap2_read = RAPCard(
            lesson_id=lesson2.id,
            card_number=1,
            title="📖 READ",
            description="Look for the + or - sign in front of each number",
            example_text="Read: (-3) + (-2) = ?\nNotice: Both numbers have - signs",
            checklist_items='["Look for + or - signs", "Count the numbers", "Is it addition or subtraction?"]'
        )
        db.add(rap2_read)
        
        rap2_ask = RAPCard(
            lesson_id=lesson2.id,
            card_number=2,
            title="❓ ASK",
            description="Do the signs match? Same or different?",
            example_text="Ask: Are both signs the same?\n-3 and -2 both have - signs ✓ They match!",
            checklist_items='["Same sign or different?", "Which number is bigger?", "What's the rule?"]'
        )
        db.add(rap2_ask)
        
        rap2_put = RAPCard(
            lesson_id=lesson2.id,
            card_number=3,
            title="✍️ PUT",
            description="Write the answer with the correct sign",
            example_text="Answer: -3 + -2 = -5",
            checklist_items='["Do the math", "Add the - sign", "Is it right?"]'
        )
        db.add(rap2_put)
        db.flush()
        
        # Quiz for Lesson 2
        quiz2 = Quiz(
            lesson_id=lesson2.id,
            title="Directed Numbers Quiz",
            max_questions=3,
            passing_score=70
        )
        db.add(quiz2)
        db.flush()
        
        q2_1 = QuizQuestion(
            quiz_id=quiz2.id,
            question_number=1,
            question_text="What is (-5) + (-3)?",
            question_type="numeric",
            options=None,
            correct_answer="-8",
            explanation="Both numbers are negative (same sign), so ADD: 5 + 3 = 8, then keep the negative → -8 ❄️",
            points=10,
            color_hint="(-5) + (-3)"
        )
        db.add(q2_1)
        
        q2_2 = QuizQuestion(
            quiz_id=quiz2.id,
            question_number=2,
            question_text="What is 7 + (-2)?",
            question_type="numeric",
            options=None,
            correct_answer="5",
            explanation="Different signs! SUBTRACT: 7 - 2 = 5. The bigger number is +7, so the answer is +5 🌞",
            points=10,
            color_hint="7 + (-2)"
        )
        db.add(q2_2)
        
        q2_3 = QuizQuestion(
            quiz_id=quiz2.id,
            question_number=3,
            question_text="The temperature was -4°C. It dropped 3 more degrees. What's the new temperature?",
            question_type="numeric",
            options=None,
            correct_answer="-7",
            explanation="Started at -4, dropped 3 more = (-4) + (-3) = -7°C 🥶",
            points=10,
            color_hint="dropped"
        )
        db.add(q2_3)
        db.flush()
        
        # ===== CREATE SCIENCE SUBJECT =====
        science_subject = Subject(name="Science", color="#10B981")
        db.add(science_subject)
        db.flush()
        
        # ===== SCIENCE UNIT 1 =====
        unit2 = Unit(
            subject_id=science_subject.id,
            title="Unit 1: Life & Organization - Cells",
            unit_number=1,
            description="Understanding the basic units of life - cells!",
            week_start=1,
            week_end=7
        )
        db.add(unit2)
        db.flush()
        
        # Lesson 3: Introduction to Cells
        lesson3 = Lesson(
            unit_id=unit2.id,
            title="What Are Cells?",
            lesson_number=1,
            duration_minutes=9,
            content="""# 🔬 What Are Cells?

**A cell is the smallest unit of LIFE!** 🧬

## Think of it this way:
- Your body is made of BILLIONS of cells 😮
- Each cell is SO TINY you need a microscope to see it 🔍
- But each cell is ALIVE! It grows, eats, and makes babies (divides)

## Two Types of Cells:

### 🦠 Prokaryotic Cells (Pro-carry-oh-tic)
- **Very small** (bacteria are this type)
- **No nucleus** (no central brain room)
- **Super simple!**

### 🧬 Eukaryotic Cells (You-carry-oh-tic)
- **Bigger** (your cells are this type!)
- **Has a nucleus** (the brain room with DNA) 🧠
- **More organized** with special parts (organelles)

## The Nucleus 🧠
- The **center** of the cell
- Contains **DNA** (the instructions for making you!)
- Like the cell's brain!

## Parts of a Cell:
| Part | Job |
|------|-----|
| **Cell Membrane** | Gatekeeper - lets things in/out |
| **Nucleus** | Brain - stores DNA |
| **Mitochondria** | Power plant - makes energy |
| **Ribosome** | Factory - makes proteins |
| **Cell Wall** | Armor - supports the cell |

Pretty cool, right? 🎉
""",
            has_movement_break=True,
            movement_break_after_minutes=7
        )
        db.add(lesson3)
        db.flush()
        
        # RAP Cards for Lesson 3
        rap3_read = RAPCard(
            lesson_id=lesson3.id,
            card_number=1,
            title="📖 READ",
            description="Read about cell types carefully",
            example_text="Read: 'Eukaryotic cells have a nucleus, prokaryotic cells don't'",
            checklist_items='["Read each part", "Find the key differences", "Look for examples"]'
        )
        db.add(rap3_read)
        
        rap3_ask = RAPCard(
            lesson_id=lesson3.id,
            card_number=2,
            title="❓ ASK",
            description="What's the main difference? Draw it!",
            example_text="Ask: Does this cell have a nucleus?\nIf YES → Eukaryotic\nIf NO → Prokaryotic",
            checklist_items='["What are we comparing?", "Draw both types", "What's different?"]'
        )
        db.add(rap3_ask)
        
        rap3_put = RAPCard(
            lesson_id=lesson3.id,
            card_number=3,
            title="✍️ PUT",
            description="Label the parts of a cell",
            example_text="Write: Cell Membrane, Nucleus, Mitochondria, etc.",
            checklist_items='["Label each part", "Write what it does", "Check spelling"]'
        )
        db.add(rap3_put)
        db.flush()
        
        # Quiz for Lesson 3
        quiz3 = Quiz(
            lesson_id=lesson3.id,
            title="Cells Quiz",
            max_questions=3,
            passing_score=70
        )
        db.add(quiz3)
        db.flush()
        
        q3_1 = QuizQuestion(
            quiz_id=quiz3.id,
            question_number=1,
            question_text="Which type of cell has a nucleus?",
            question_type="multiple_choice",
            options=json.dumps(["Prokaryotic", "Eukaryotic", "Neither", "Both"]),
            correct_answer="Eukaryotic",
            explanation="Eukaryotic cells have a nucleus (the brain room!). Prokaryotic cells are too simple and don't have one. 🧠",
            points=10,
            color_hint="nucleus"
        )
        db.add(q3_1)
        
        q3_2 = QuizQuestion(
            quiz_id=quiz3.id,
            question_number=2,
            question_text="What is the job of the mitochondria?",
            question_type="free_response",
            options=None,
            correct_answer="make energy",
            explanation="Mitochondria is the 'power plant' of the cell! It makes energy so the cell can work. ⚡",
            points=10,
            color_hint="mitochondria"
        )
        db.add(q3_2)
        
        q3_3 = QuizQuestion(
            quiz_id=quiz3.id,
            question_number=3,
            question_text="Which cell part is the 'gatekeeper' that controls what enters and exits?",
            question_type="multiple_choice",
            options=json.dumps(["Cell wall", "Cell membrane", "Nucleus", "Ribosome"]),
            correct_answer="Cell membrane",
            explanation="The cell membrane is like a security guard! It decides what can come in and what can go out. 🚪",
            points=10,
            color_hint="gatekeeper"
        )
        db.add(q3_3)
        db.flush()
        
        # Commit everything
        db.commit()
        print("✅ Database seeded successfully!")
        print("   - Math Unit 1: 2 lessons with quizzes and RAP cards")
        print("   - Science Unit 1: 1 lesson with quiz and RAP cards")
        
    except Exception as e:
        db.rollback()
        print(f"❌ Error seeding database: {e}")
        raise
    finally:
        db.close()


if __name__ == "__main__":
    seed_database()

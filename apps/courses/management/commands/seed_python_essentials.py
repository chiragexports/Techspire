import os
from django.core.management.base import BaseCommand
from django.utils.text import slugify
from apps.accounts.models import User
from apps.courses.models import CourseCategory, Course, Module, Lesson, CourseProject, InterviewQuestion
from apps.quizzes.models import Quiz, Question, Choice

class Command(BaseCommand):
    help = "Seeds comprehensive Python Essentials 1 and Python Essentials 2 courses with rich written notes, code samples, exercises, and quizzes."

    def handle(self, *args, **options):
        self.stdout.write(self.style.NOTICE(">> Starting Python Essentials 1 & 2 Seeding..."))

        admin_user = User.objects.filter(is_superuser=True).first()
        if not admin_user:
            admin_user = User.objects.filter(role='admin').first()

        category, _ = CourseCategory.objects.get_or_create(
            slug='python-programming',
            defaults={
                'name': 'Python Programming',
                'icon_class': 'fab fa-python',
                'order': 2,
                'description': 'From basic syntax to advanced OOP, data structures, algorithms, automation scripting, and backend system development.'
            }
        )

        self.seed_python_essentials_1(category, admin_user)
        self.seed_python_essentials_2(category, admin_user)

        self.stdout.write(self.style.SUCCESS(">> Successfully seeded Python Essentials 1 & 2!"))

    def seed_python_essentials_1(self, category, instructor):
        course, _ = Course.objects.update_or_create(
            slug='python-essentials-1',
            defaults={
                'title': 'Python Essentials 1: Fundamentals of Python Programming',
                'category': category,
                'instructor': instructor,
                'instructor_name': 'TECHSPIRE Academic Council',
                'short_description': 'Master the core foundational concepts of Python: data types, operators, branching, loops, functions, and standard data structures with hands-on practice.',
                'description': """Python Essentials 1 is designed for beginners and aspiring software engineers seeking a rigorous, self-paced foundation in programming. 

Through structured written tutorials, syntax teardowns, live code examples, and interactive self-check exercises, you will master Python from the ground up without relying on video tutorials.

You will learn fundamental computer programming principles, execution models, variables, expressions, conditional branching, repetitive loops, functions, scopes, lists, and tuples.""",
                'level': 'beginner',
                'duration_hours': 18.0,
                'is_free': True,
                'price': 0.00,
                'what_you_will_learn': """Understand how Python code is interpreted, compiled to bytecode, and executed
Master numeric, boolean, and text data types with strict type conventions
Build dynamic logic with arithmetic, relational, and boolean logical operators
Format console input and output effectively using modern f-strings
Write robust decision trees using if, elif, and else statements
Implement iterative algorithms using for loops, while loops, and range generators
Manage collections of data using Python lists, indexing, slicing, and methods
Create reusable, modular functions with parameters, return values, and clear variable scope
Solve real-world algorithmic problems with automated self-check tests""",
                'requirements': """No prior programming experience required
A computer (Windows, macOS, or Linux) with Python 3.10+ installed
A modern text editor or IDE such as VS Code, PyCharm, or Thonny""",
                'roadmap_highlights': """Module 1: Introduction to Python & Architecture
Module 2: Variables, Data Types & Type Conversion
Module 3: Operators & Expressions
Module 4: Console Input, Output & String Formatting
Module 5: Conditional Statements & Decision Making
Module 6: Loops & Iteration Constructs
Module 7: Lists & Tuples Fundamentals
Module 8: Functions & Scope Mechanics
Module 9: Practice Labs & Final Assessment Quiz""",
                'career_opportunities': """Junior Python Developer
Automation Scripting Specialist
Data Analyst Trainee
Backend Engineering Intern
Technical Support Engineer""",
                'has_certificate': True,
                'badge_text': 'Foundational Certification',
                'is_published': True,
                'is_featured': True,
            }
        )

        # Clean existing modules to rebuild clean hierarchy
        course.modules.all().delete()

        modules_data = [
            {
                'order': 1,
                'title': 'Introduction to Python & Programming Basics',
                'description': 'Understand how Python works, its history, runtime execution model, and writing your first script.',
                'lessons': [
                    {
                        'order': 1,
                        'title': 'What is Python? Architecture & Design Philosophy',
                        'duration': 15,
                        'notes': """# What is Python?

**Python** is a high-level, interpreted, general-purpose programming language designed by **Guido van Rossum** and first released in 1991. Python emphasizes code readability with its notable use of significant whitespace.

---

## 1. Key Characteristics of Python

- **Interpreted & Dynamic**: Python source code (`.py`) is compiled into intermediate bytecode (`.pyc`) and executed by the Python Virtual Machine (PVM). Types are checked at runtime.
- **Multi-Paradigm**: Python supports procedural, object-oriented, and functional programming styles.
- **Batteries Included**: Comes standard with a comprehensive standard library for math, networking, file I/O, JSON processing, and cryptography.
- **Cross-Platform**: Runs identically across Windows, macOS, Linux, and embedded systems.

---

## 2. The Python Execution Pipeline

```
┌──────────────┐     ┌──────────────┐     ┌──────────────────────┐     ┌──────────────┐
│  Source Code │ ──> │ Python Comp. │ ──> │       Bytecode       │ ──> │  Python VM   │
│   (app.py)   │     │  (CPython)   │     │ (app.cpython-312.pyc)│     │  (Execution) │
└──────────────┘     └──────────────┘     └──────────────────────┘     └──────────────┘
```

When you invoke `python app.py`:
1. The compiler checks syntax and compiles source code into bytecode.
2. Bytecode instructions are passed to the PVM loop for machine instruction execution.

---

## 3. Your First Program: "Hello, World!"

```python
# The classic entry point to computer programming
print("Hello, Techspire Learner!")
print("Welcome to Python Essentials 1.")
```

### Output:
```text
Hello, Techspire Learner!
Welcome to Python Essentials 1.
```

---

## 4. Common Beginner Pitfalls

> [!WARNING]
> **Case Sensitivity**: Python is strictly case-sensitive. `Print()` or `PRINT()` will raise a `NameError: name 'Print' is not defined`. Always write lowercase `print()`.
""",
                        'takeaways': """Python is an interpreted, dynamically typed language emphasizing code readability.
Source code is compiled into bytecode before being interpreted by the Python Virtual Machine (PVM).
Keywords and built-in function names are case-sensitive.""",
                        'interview': """Q: Is Python an interpreted or compiled language?
A: Python is both: source code is first compiled into intermediate bytecode (.pyc), which is then interpreted by the Python Virtual Machine (PVM) runtime.""",
                        'exercise': """### Exercise 1.1: Print Profile Banner
Write a Python script that outputs a 3-line console banner containing your name, target skill, and reason for learning Python.""",
                        'solution': """```python
print("========================================")
print("Name: Alex Morgan | Target: Full-Stack Developer")
print("Goal: Build reliable cloud applications with Python")
print("========================================")
```"""
                    },
                    {
                        'order': 2,
                        'title': 'Python Syntax Rules, Indentation & Comments',
                        'duration': 15,
                        'notes': """# Python Syntax Rules, Indentation & Comments

Python replaces curly brackets `{}` found in C/C++/Java with **whitespace indentation** to delimit code blocks.

---

## 1. Indentation Rules

- Standard PEP 8 convention requires **4 spaces per indentation level** (do not mix tabs and spaces).
- All statements within the same block must have the exact same indentation offset.

```python
# Valid indentation block
if 10 > 5:
    print("10 is greater than 5")
    print("This line is also inside the if-block")

print("This line is outside the if-block")
```

---

## 2. Comments in Python

Comments document intent and are ignored by the Python bytecode compiler.

```python
# Single-line comment starts with a hash mark

# Multi-line explanation or comment
# used for module, class, and function documentation.
def calculate_area(radius):
    # Calculates the area of a circle given radius.
    PI = 3.14159
    return PI * (radius ** 2)
```
""",
                        'takeaways': """Indentation defines scope and execution blocks in Python.
PEP 8 recommends 4 spaces per indentation level.
Use # for inline/single-line comments and triple quotes for docstrings.""",
                        'interview': """Q: What happens if you mix tabs and spaces in Python 3?
A: Python 3 raises a TabError: inconsistent use of tabs and spaces in indentation.""",
                        'exercise': """### Exercise 1.2: Fix Indentation Bug
Inspect the following broken snippet and correct the indentation:
```python
x = 20
if x > 10:
print("x is big")
  print("processing complete")
```""",
                        'solution': """```python
x = 20
if x > 10:
    print("x is big")
    print("processing complete")
```"""
                    }
                ]
            },
            {
                'order': 2,
                'title': 'Variables, Data Types & Type Conversion',
                'description': 'Master variable assignment, dynamic typing, primitive data types (int, float, str, bool), and type casting.',
                'lessons': [
                    {
                        'order': 1,
                        'title': 'Variables, Memory References & Identifiers',
                        'duration': 20,
                        'notes': """# Variables, Memory References & Identifiers

In Python, a variable is not a memory bucket holding a value; rather, it is a **named reference (pointer)** bound to an object in memory.

---

## 1. Variable Assignment

```python
# Variable binding
course_name = "Python Essentials 1"
total_modules = 9
passing_score = 75.5
is_active = True

print(course_name, type(course_name))
print(total_modules, type(total_modules))
print(passing_score, type(passing_score))
print(is_active, type(is_active))
```

### Output:
```text
Python Essentials 1 <class 'str'>
9 <class 'int'>
75.5 <class 'float'>
True <class 'bool'>
```

---

## 2. Identifier Naming Rules

- Identifiers must start with a letter (`a-z`, `A-Z`) or an underscore `_`.
- Cannot start with a digit.
- Can only contain alphanumeric characters and underscores (`a-z, A-Z, 0-9, _`).
- Cannot use reserved Python keywords (`if`, `for`, `while`, `class`, `def`, `return`, `import`, etc.).
- **PEP 8 Convention**: Use `snake_case` for variables and functions (e.g. `user_score`, `max_limit`).

---

## 3. Multiple Assignment & Swapping

```python
# Assign multiple variables in one line
x, y, z = 10, 20, 30

# Pythonic variable swap without temporary variable
x, y = y, x
print("Swapped values -> x:", x, "y:", y)
```
""",
                        'takeaways': """Variables in Python are object references bound dynamically at runtime.
Variable names follow snake_case convention and must not collide with reserved keywords.
Python supports multiple assignment and clean in-place variable swapping.""",
                        'interview': """Q: How does Python manage memory for variables?
A: Python uses reference counting and a cyclic garbage collector. Variables reference objects allocated on the heap.""",
                        'exercise': """### Exercise 2.1: Swap Two Numbers
Write a Python program that initializes variables `a = 150` and `b = 300`, swaps their values using tuple unpacking, and verifies the output.""",
                        'solution': """```python
a = 150
b = 300
print(f"Before: a={a}, b={b}")

a, b = b, a
print(f"After: a={a}, b={b}")
```"""
                    },
                    {
                        'order': 2,
                        'title': 'Primitive Data Types & Type Casting',
                        'duration': 20,
                        'notes': """# Primitive Data Types & Type Casting

Python has 4 primary primitive scalar data types:

| Type | Name | Examples | Mutability |
| :--- | :--- | :--- | :--- |
| `int` | Integer | `-45`, `0`, `1024` | Immutable |
| `float` | Floating-point | `3.14159`, `-0.001`, `2.5e3` | Immutable |
| `str` | Text String | `"Techspire"`, `'Indore'` | Immutable |
| `bool` | Boolean Logic | `True`, `False` | Immutable |

---

## 1. Type Casting (Explicit Conversion)

```python
# String to Integer
num_str = "120"
num_int = int(num_str)

# Float to Integer (Truncates decimal portion)
price = 99.85
price_int = int(price)  # Result: 99

# Integer to String
rank = 1
rank_str = "Rank #" + str(rank)

# Truthiness Casting
print(bool(0))        # False
print(bool(1))        # True
print(bool(""))       # False (empty string is falsy)
print(bool("Hello"))  # True (non-empty string is truthy)
```

---

## 2. Checking Types: `type()` vs `isinstance()`

```python
score = 85.0

# Using type()
if type(score) is float:
    print("Score is float")

# Using isinstance() (Preferred because it supports inheritance)
if isinstance(score, (int, float)):
    print("Score is a valid numeric type")
```
""",
                        'takeaways': """The four fundamental primitives are int, float, str, and bool.
Explicit type casting uses built-in functions: int(), float(), str(), bool().
Use isinstance(obj, type) instead of type(obj) == type for polymorphic type checks.""",
                        'interview': """Q: What is the difference between int() conversion of a float vs round()?
A: int(3.9) truncates towards zero returning 3. round(3.9) rounds to nearest integer returning 4.""",
                        'exercise': """### Exercise 2.2: Safe Total Calculator
Given two string inputs `price1 = "499.50"` and `price2 = "250.25"`, convert them to floats, calculate total with 18% tax, and print the result rounded to 2 decimals.""",
                        'solution': """```python
price1 = "499.50"
price2 = "250.25"

subtotal = float(price1) + float(price2)
tax = subtotal * 0.18
grand_total = subtotal + tax

print("Subtotal:", round(subtotal, 2))
print("Tax (18%):", round(tax, 2))
print("Grand Total:", round(grand_total, 2))
```"""
                    }
                ]
            },
            {
                'order': 3,
                'title': 'Operators & Expressions',
                'description': 'Arithmetic, comparison, logical, assignment, and bitwise operators with operator precedence rules.',
                'lessons': [
                    {
                        'order': 1,
                        'title': 'Arithmetic & Assignment Operators',
                        'duration': 15,
                        'notes': """# Arithmetic & Assignment Operators

Python provides rich arithmetic operators with specific behaviors for integers and floats.

---

## 1. Arithmetic Operators

```python
a = 17
b = 5

print("Addition (+):", a + b)          # 22
print("Subtraction (-):", a - b)       # 12
print("Multiplication (*):", a * b)    # 85
print("True Division (/):", a / b)     # 3.4 (Always returns float)
print("Floor Division (//):", a // b)  # 3 (Discards remainder)
print("Modulo (%):", a % b)            # 2 (Remainder)
print("Exponentiation (**):", a ** 2)  # 289 (17 squared)
```

---

## 2. Compound Assignment Operators

```python
counter = 10
counter += 5   # counter = counter + 5 -> 15
counter -= 2   # counter = counter - 2 -> 13
counter *= 2   # counter = counter * 2 -> 26
counter //= 4  # counter = counter // 4 -> 6
print("Final Counter:", counter)
```
""",
                        'takeaways': """Single slash division (/) always yields a float in Python 3.
Floor division (//) yields an integer quotient, discarding fractions.
Modulo (%) returns the remainder of integer division.""",
                        'interview': """Q: What is the output of 7 // 2 vs 7 / 2 in Python 3?
A: 7 // 2 produces integer 3, while 7 / 2 produces float 3.5.""",
                        'exercise': """### Exercise 3.1: Minutes to Hours & Minutes
Convert total seconds `total_seconds = 7540` into hours, minutes, and remaining seconds using `//` and `%` operators.""",
                        'solution': """```python
total_seconds = 7540
hours = total_seconds // 3600
remaining = total_seconds % 3600
minutes = remaining // 60
seconds = remaining % 60

print(f"{total_seconds}s = {hours}h {minutes}m {seconds}s")
```"""
                    },
                    {
                        'order': 2,
                        'title': 'Comparison & Logical Operators',
                        'duration': 15,
                        'notes': """# Comparison & Logical Operators

Comparison and logical operators evaluate conditions and return boolean values (`True` or `False`).

---

## 1. Comparison Operators

- `==` Equal to
- `!=` Not equal to
- `>` Greater than
- `<` Less than
- `>=` Greater than or equal to
- `<=` Less than or equal to

```python
age = 21
print(age >= 18)   # True
print(age == 25)   # False
print(age != 30)   # True

# Python supports chained comparisons:
x = 15
print(10 < x < 20) # True (Equivalent to: 10 < x and x < 20)
```

---

## 2. Logical Operators (`and`, `or`, `not`)

```python
has_id = True
is_enrolled = True
has_outstanding_fee = False

can_take_exam = (has_id and is_enrolled) and (not has_outstanding_fee)
print("Eligibility for exam:", can_take_exam)
```

### Short-Circuit Evaluation
- `and` stops evaluating as soon as an operand is `False`.
- `or` stops evaluating as soon as an operand is `True`.
""",
                        'takeaways': """Comparison operators return boolean True or False.
Python uniquely supports chained comparisons like 10 < x <= 20.
Logical operators evaluate using short-circuit mechanics.""",
                        'interview': """Q: What is short-circuit evaluation in Python?
A: In an 'and' expression, if the first operand is False, Python does not evaluate subsequent operands. In an 'or' expression, if the first is True, subsequent operands are skipped.""",
                        'exercise': """### Exercise 3.2: Eligibility Rule Engine
Write an expression checking if an applicant is eligible for a senior engineering post: age must be between 24 and 45 inclusive, years_experience >= 3, and must have passed_background_check.""",
                        'solution': """```python
age = 28
years_experience = 4
passed_background_check = True

is_eligible = (24 <= age <= 45) and (years_experience >= 3) and passed_background_check
print("Eligible:", is_eligible)
```"""
                    }
                ]
            },
            {
                'order': 4,
                'title': 'Input, Output & String Formatting',
                'description': 'Advanced print() options, user input parsing, and string interpolation with modern f-strings.',
                'lessons': [
                    {
                        'order': 1,
                        'title': 'Console Output with print() & String Formatting',
                        'duration': 15,
                        'notes': """# Console Output & Modern String Formatting

The built-in `print()` function accepts arguments, separators, and line terminators.

---

## 1. `print()` Parameters: `sep` and `end`

```python
# Default separator is a single space, default end is newline '\n'
print("Python", "Essentials", "Indore", sep=" | ")
print("Loading progress", end="... ")
print("Complete!")
```

### Output:
```text
Python | Essentials | Indore
Loading progress... Complete!
```

---

## 2. Modern Formatted Strings (f-strings)

Introduced in Python 3.6, **f-strings** provide the fastest and cleanest string interpolation syntax.

```python
student_name = "Rahul Sharma"
score = 92.4567
course = "Python Essentials 1"

# Formatting floating point decimals and alignment
message = f"Student: {student_name} | Course: {course} | Score: {score:.2f}%"
print(message)

# Expression evaluation inside f-strings
unit_price = 450
quantity = 3
print(f"Total Bill: Rs. {unit_price * quantity:,} (Qty: {quantity})")
```
""",
                        'takeaways': """Use sep= and end= parameters to customize print() formatting.
F-strings (f"...") are preferred over % formatting and str.format().
Float precision can be formatted cleanly using {value:.2f}.""",
                        'interview': """Q: Why are f-strings faster than str.format() and %-formatting in Python?
A: F-strings are evaluated at runtime as optimized bytecode expressions rather than parsing format strings repeatedly.""",
                        'exercise': """### Exercise 4.1: Invoice Formatter
Format a tabular invoice row showing Item Name (left aligned, 15 spaces), Qty (3 spaces), and Price formatted to 2 decimals.""",
                        'solution': """```python
item = "Python Book"
qty = 2
price = 299.00
total = qty * price

print(f"{item:<15} | {qty:>3} | Rs. {price:>7.2f} | Total: Rs. {total:.2f}")
```"""
                    }
                ]
            },
            {
                'order': 5,
                'title': 'Conditional Statements & Decision Trees',
                'description': 'Control flow branching with if, elif, else, nested logic, and ternary conditional expressions.',
                'lessons': [
                    {
                        'order': 1,
                        'title': 'if, elif, else Branching & Nested Logic',
                        'duration': 20,
                        'notes': """# Conditional Statements & Decision Making

Decision-making in Python executes different blocks of code based on whether boolean expressions evaluate to `True` or `False`.

---

## 1. The `if-elif-else` Ladder

```python
score = 82

if score >= 90:
    grade = "A+ (Outstanding)"
elif score >= 80:
    grade = "A (Excellent)"
elif score >= 70:
    grade = "B (Good)"
elif score >= 60:
    grade = "C (Satisfactory)"
else:
    grade = "F (Needs Improvement)"

print(f"Your Score: {score} -> Grade: {grade}")
```

---

## 2. Ternary Conditional Operator (Inline if-else)

Python provides a concise one-line syntax for simple conditional assignments:
`value_if_true if condition else value_if_false`

```python
marks = 74
status = "PASS" if marks >= 70 else "RETRY"
print("Result Status:", status)
```
""",
                        'takeaways': """if-elif-else evaluates sequentially; the first matching block executes.
The else branch acts as a fallback when no prior conditions evaluate to True.
Ternary conditional expressions allow concise inline assignments.""",
                        'interview': """Q: What is the ternary operator syntax in Python?
A: 'x if condition else y' evaluates to x if condition is true, otherwise y.""",
                        'exercise': """### Exercise 5.1: Admission Fee Classifier
Write a program that determines museum ticket price: age < 5 is Free (Rs 0), age 5 to 17 is Rs 100, age 18 to 60 is Rs 250, age > 60 is Senior Discount (Rs 150).""",
                        'solution': """```python
age = 65

if age < 5:
    fee = 0
elif 5 <= age <= 17:
    fee = 100
elif 18 <= age <= 60:
    fee = 250
else:
    fee = 150

print(f"Visitor Age: {age} -> Ticket Fee: Rs. {fee}")
```"""
                    }
                ]
            },
            {
                'order': 6,
                'title': 'Loops & Iterative Constructs',
                'description': 'Master while loops, for loops with range(), loop control statements (break, continue), and loop else clauses.',
                'lessons': [
                    {
                        'order': 1,
                        'title': 'while Loops, for Loops & range() Function',
                        'duration': 25,
                        'notes': """# Loops & Iteration in Python

Loops automate repetitive execution of statements over collections, sequences, or condition boundaries.

---

## 1. The `for` Loop and `range()`

The `range(start, stop, step)` generates an immutable arithmetic sequence.

```python
# Iterating from 1 to 5 (stop index is exclusive)
for i in range(1, 6):
    print(f"Step {i}: Square = {i**2}")

# Iterating with step interval
for count in range(10, 0, -2):
    print("Countdown:", count)
```

---

## 2. The `while` Loop

A `while` loop executes as long as its condition remains `True`.

```python
battery = 100
while battery > 30:
    print(f"Device Operating (Battery: {battery}%)")
    battery -= 25

print("Battery low, plug in charger.")
```
""",
                        'takeaways': """range(start, stop, step) generates integers where the stop boundary is exclusive.
while loops execute until the condition evaluates to False.
Ensure loop counters increment/decrement properly to prevent infinite loops.""",
                        'interview': """Q: Is range() a list in Python 3?
A: No, in Python 3 range() is an immutable sequence object that generates numbers on demand (lazy evaluation), taking constant O(1) memory.""",
                        'exercise': """### Exercise 6.1: Factorial Calculator
Calculate the factorial of a positive integer N (e.g. N = 6 -> 6 * 5 * 4 * 3 * 2 * 1) using a for loop.""",
                        'solution': """```python
n = 6
factorial = 1
for i in range(1, n + 1):
    factorial *= i

print(f"Factorial of {n}! = {factorial}")
```"""
                    },
                    {
                        'order': 2,
                        'title': 'Loop Controls: break, continue & else Clause',
                        'duration': 20,
                        'notes': """# Loop Control Statements

Python provides control keywords to alter standard loop flow:

---

## 1. `break` Statement
Immediately terminates the innermost enclosing loop.

```python
for num in range(1, 20):
    if num % 7 == 0 and num > 10:
        print(f"Found first qualifying number: {num}")
        break
```

---

## 2. `continue` Statement
Skips the remainder of the current iteration and jumps to the next cycle.

```python
for i in range(1, 10):
    if i % 2 == 0:
        continue  # Skip even numbers
    print("Odd number:", i)
```

---

## 3. Loop `else` Clause
The `else` block executes **only if the loop completed naturally** without encountering a `break`.

```python
target = 13
for n in range(2, target):
    if target % n == 0:
        print(f"{target} is not prime (divisible by {n})")
        break
else:
    print(f"{target} is a PRIME number!")
```
""",
                        'takeaways': """break immediately exits the loop.
continue skips the rest of the current iteration.
The loop else clause runs only when the loop terminates without a break.""",
                        'interview': """Q: When does the 'else' block of a for/while loop execute?
A: It executes when the loop condition becomes false (loop completes normally), but is skipped if the loop was terminated prematurely by a break statement.""",
                        'exercise': """### Exercise 6.2: Search First Even Number
Given a list of numbers, search for the first number divisible by 7 greater than 50. If found, print it and break. If not found, use loop else to print 'Not Found'.""",
                        'solution': """```python
numbers = [12, 25, 33, 49, 56, 70, 81]

for num in numbers:
    if num > 50 and num % 7 == 0:
        print("Found matching number:", num)
        break
else:
    print("No matching number found.")
```"""
                    }
                ]
            },
            {
                'order': 7,
                'title': 'Data Structures: Lists & Tuples',
                'description': 'Ordered collections, zero-based indexing, slicing, mutability, list methods, and immutable tuples.',
                'lessons': [
                    {
                        'order': 1,
                        'title': 'Lists: Creation, Indexing, Slicing & Mutability',
                        'duration': 25,
                        'notes': """# Python Lists: Dynamic Arrays

A **list** is an ordered, mutable sequence of elements enclosed in square brackets `[]`.

---

## 1. Indexing & Slicing

```python
languages = ["Python", "JavaScript", "Rust", "Go", "TypeScript", "Kotlin"]

# Zero-based positive indexing & Negative indexing
print(languages[0])   # "Python"
print(languages[-1])  # "Kotlin" (last element)

# Slicing syntax: list[start:stop:step]
print(languages[1:4])   # ['JavaScript', 'Rust', 'Go']
print(languages[:3])    # First 3 elements: ['Python', 'JavaScript', 'Rust']
print(languages[::2])   # Every 2nd element
print(languages[::-1])  # Reversed list
```

---

## 2. Essential List Methods

```python
stack = []
stack.append("Task 1")     # Adds to end
stack.append("Task 2")
stack.insert(1, "Urgent")  # Inserts at index 1

print("Stack:", stack)

# Removal
removed_item = stack.pop() # Removes & returns last item ("Task 2")
stack.remove("Task 1")     # Removes by value

print("After removals:", stack)
```
""",
                        'takeaways': """Lists are mutable, ordered sequences supporting heterogeneous types.
Slicing syntax is list[start:stop:step]; stop index is exclusive.
Key methods include append(), insert(), pop(), remove(), sort(), reverse().""",
                        'interview': """Q: What is the time complexity of append() vs insert(0, item) in a Python list?
A: append() is O(1) amortized time, whereas insert(0, item) is O(n) because all existing elements must be shifted in memory.""",
                        'exercise': """### Exercise 7.1: List Deduplication & Sorting
Given list `scores = [85, 92, 78, 85, 95, 78, 90]`, extract the unique scores, sort them in descending order, and print the top 3 scores.""",
                        'solution': """```python
scores = [85, 92, 78, 85, 95, 78, 90]
unique_sorted = sorted(list(set(scores)), reverse=True)
print("Top 3 unique scores:", unique_sorted[:3])
```"""
                    },
                    {
                        'order': 2,
                        'title': 'Tuples: Immutability & Use Cases',
                        'duration': 15,
                        'notes': """# Tuples: Immutable Sequences

A **tuple** is an ordered, **immutable** collection enclosed in parentheses `()`. Once created, its items cannot be added, removed, or modified.

---

## 1. Defining Tuples

```python
# Tuple definition
server_config = ("192.168.1.100", 8080, "production")

# Single element tuple requires a trailing comma!
single_item = ("Techspire",)  # Tuple
not_a_tuple = ("Techspire")   # String

# Tuple unpacking
host, port, env = server_config
print(f"Connecting to {host}:{port} in {env} mode")
```

---

## 2. Why Use Tuples Over Lists?

1. **Safety**: Data integrity is protected against unintended modification.
2. **Performance**: Tuples use less memory and instantiate faster than lists.
3. **Dictionary Keys**: Because tuples are immutable, they are hashable and can be used as dictionary keys.
""",
                        'takeaways': """Tuples are immutable; attempts to reassign elements raise TypeError.
Single-element tuples require a trailing comma e.g. (item,).
Tuples are faster, use less memory, and are hashable.""",
                        'interview': """Q: Can a tuple contain a mutable object like a list?
A: Yes. If a tuple contains a list, the tuple reference cannot change, but the inner list can still be mutated.""",
                        'exercise': """### Exercise 7.2: Coordinate Distance Calculation
Given two coordinate tuples `p1 = (3, 4)` and `p2 = (7, 1)`, unpack the coordinates and calculate the Euclidean distance.""",
                        'solution': """```python
import math

p1 = (3, 4)
p2 = (7, 1)

x1, y1 = p1
x2, y2 = p2

distance = math.sqrt((x2 - x1)**2 + (y2 - y1)**2)
print("Euclidean Distance:", round(distance, 2))
```"""
                    }
                ]
            },
            {
                'order': 8,
                'title': 'Functions, Arguments & Variable Scope',
                'description': 'Modular code design with def, parameters, return values, *args, **kwargs, and local vs global scope.',
                'lessons': [
                    {
                        'order': 1,
                        'title': 'Function Definition, Arguments & Return Values',
                        'duration': 25,
                        'notes': """# Functions in Python

Functions allow you to write reusable, modular, and testable blocks of code using the `def` keyword.

---

## 1. Defining Functions & Default Arguments

```python
def calculate_discount(price, discount_percent=10):
    # Calculates discounted price given original price and percentage.
    discount_amount = price * (discount_percent / 100)
    final_price = price - discount_amount
    return final_price

# Calling with default vs explicit argument
print("Standard Discount:", calculate_discount(1000))        # Uses default 10% -> 900.0
print("Special Discount:", calculate_discount(1000, 25))     # Uses 25% -> 750.0
```

---

## 2. Variable Scope: Local vs Global

- **Local Scope**: Variables declared inside a function exist only during function execution.
- **Global Scope**: Variables declared at module top-level are accessible everywhere.
- **LEGB Rule**: Python resolves names in order: **L**ocal -> **E**nclosing -> **G**lobal -> **B**uilt-in.

```python
app_version = "v1.0"  # Global variable

def show_info():
    module_name = "AuthModule"  # Local variable
    print(f"Running {module_name} on {app_version}")

show_info()
```
""",
                        'takeaways': """Functions are defined with def and return values using the return statement.
Default parameter values should be immutable (avoid mutable defaults like [] or {}).
Python resolves variables using the LEGB scope lookup hierarchy.""",
                        'interview': """Q: Why is it dangerous to use a mutable default argument like def func(items=[])?
A: In Python, default parameter objects are evaluated once when the function is defined. Successive calls will mutate and share the exact same list instance.""",
                        'exercise': """### Exercise 8.1: Temperature Converter Utility
Write a function `convert_temp(value, to_unit='C')` that converts Fahrenheit to Celsius when to_unit='C' and Celsius to Fahrenheit when to_unit='F'.""",
                        'solution': """```python
def convert_temp(value, to_unit='C'):
    if to_unit.upper() == 'C':
        # Fahrenheit to Celsius: (F - 32) * 5/9
        return (value - 32) * (5 / 9)
    else:
        # Celsius to Fahrenheit: (C * 9/5) + 32
        return (value * (9 / 5)) + 32

print("100F in C:", round(convert_temp(100, 'C'), 1))
print("37C in F:", round(convert_temp(37, 'F'), 1))
```"""
                    }
                ]
            },
            {
                'order': 9,
                'title': 'Practice Labs & Final Assessment Quiz',
                'description': 'Comprehensive review exercises, interview problem walk-throughs, and the final certification assessment.',
                'lessons': [
                    {
                        'order': 1,
                        'title': 'Comprehensive Review & Real-World Lab Challenges',
                        'duration': 30,
                        'notes': """# Python Essentials 1: Comprehensive Review

Congratulations on reaching the final module of **Python Essentials 1**! You have built a solid foundation across variables, operators, branching, loops, lists, tuples, and functions.

---

## Key Competency Checklist

- [x] Python execution model (bytecode and PVM)
- [x] Primitive types (`int`, `float`, `str`, `bool`) and type casting
- [x] Arithmetic, comparison, and logical short-circuiting
- [x] Modern `f-string` formatting and console I/O
- [x] `if-elif-else` control flow decision ladders
- [x] `for` loops, `while` loops, `break`, `continue`, and `else`
- [x] `list` indexing, slicing, and mutation methods
- [x] `tuple` immutability and unpacking
- [x] `def` functions, parameter handling, and LEGB variable scopes

---

## Lab Challenge: Inventory Management Engine

```python
def process_inventory(items_stock, restock_threshold=10):
    # Takes a list of tuples: (item_name, count)
    # Returns:
    #   1. total_items
    #   2. critical_restock_list
    total_count = 0
    needs_restock = []

    for name, count in items_stock:
        total_count += count
        if count <= restock_threshold:
            needs_restock.append((name, count))

    return total_count, needs_restock

inventory = [("Monitors", 15), ("Keyboards", 4), ("Mice", 8), ("Cables", 50)]
total, restock = process_inventory(inventory)
print("Total Units in Stock:", total)
print("Items Requiring Restock:", restock)
```

Now, proceed to the **Final Assessment Quiz** to test your knowledge and claim your course completion!
""",
                        'takeaways': """Review all core language concepts before attempting the final assessment.
Passing score is 70% or higher.
Completed assessment unlocks your verifiable certificate.""",
                        'interview': """Q: What are the fundamental differences between Python 2 and Python 3?
A: Python 3 uses Unicode strings by default, print is a function print(), integer division 7/2 yields 3.5 float, and xrange() was replaced by lazy range().""",
                        'exercise': """### Final Capstone Challenge: Palindrome & Anagram Verifier
Write a function `is_palindrome(text)` that ignores spaces and case, returning True if the string reads the same forwards and backwards.""",
                        'solution': """```python
def is_palindrome(text):
    cleaned = "".join(ch.lower() for ch in text if ch.isalnum())
    return cleaned == cleaned[::-1]

print("Is 'Race car' a palindrome?", is_palindrome("Race car"))
print("Is 'Python' a palindrome?", is_palindrome("Python"))
```"""
                    }
                ]
            }
        ]

        for m_data in modules_data:
            module = Module.objects.create(
                course=course,
                title=m_data['title'],
                description=m_data['description'],
                order=m_data['order']
            )

            for l_data in m_data['lessons']:
                Lesson.objects.create(
                    module=module,
                    title=l_data['title'],
                    order=l_data['order'],
                    lesson_type='article',
                    duration_minutes=l_data['duration'],
                    notes_markdown=l_data['notes'],
                    key_takeaways=l_data.get('takeaways', ''),
                    interview_tips=l_data.get('interview', ''),
                    practice_exercise=l_data.get('exercise', ''),
                    exercise_solution=l_data.get('solution', ''),
                    is_preview=(m_data['order'] == 1 and l_data['order'] == 1)
                )

        # Seed Quiz for Python Essentials 1
        quiz, _ = Quiz.objects.update_or_create(
            course=course,
            title='Python Essentials 1: Final Assessment Quiz',
            defaults={
                'description': 'Test your mastery of foundational Python syntax, variables, operators, branching, loops, lists, and functions.',
                'pass_percentage': 70,
                'time_limit_minutes': 20,
                'max_attempts': 5,
                'is_published': True
            }
        )
        quiz.questions.all().delete()

        questions_data = [
            {
                'prompt': 'What is the correct output of print(type(10 / 2)) in Python 3?',
                'points': 2,
                'explanation': 'In Python 3, the single slash division operator (/) always returns a float, so 10 / 2 is 5.0 of type float.',
                'choices': [
                    ('<class \'int\'>', False),
                    ('<class \'float\'>', True),
                    ('<class \'double\'>', False),
                    ('5', False),
                ]
            },
            {
                'prompt': 'Which of the following variable names is INVALID in Python?',
                'points': 2,
                'explanation': 'Variable names cannot begin with a numeric digit (2nd_score is invalid).',
                'choices': [
                    ('_user_score', False),
                    ('userScore2', False),
                    ('2nd_score', True),
                    ('TOTAL_MARKS', False),
                ]
            },
            {
                'prompt': 'Given numbers = [10, 20, 30, 40, 50], what does numbers[1:4] return?',
                'points': 2,
                'explanation': 'Slicing start:stop extracts from index 1 up to index 4 (exclusive), which gives [20, 30, 40].',
                'choices': [
                    ('[10, 20, 30]', False),
                    ('[20, 30, 40]', True),
                    ('[20, 30, 40, 50]', False),
                    ('[10, 20, 30, 40]', False),
                ]
            },
            {
                'prompt': 'What happens when a loop terminates without hitting a "break" statement?',
                'points': 2,
                'explanation': 'If a for or while loop finishes all iterations naturally without hitting a break statement, its optional "else" block executes.',
                'choices': [
                    ('The else block attached to the loop executes', True),
                    ('A StopIteration exception is raised', False),
                    ('The loop restarts from the beginning', False),
                    ('The program crashes with a SyntaxError', False),
                ]
            },
            {
                'prompt': 'What is the main difference between a Python List and a Tuple?',
                'points': 2,
                'explanation': 'Lists are mutable (can add, remove, and modify elements) whereas Tuples are immutable.',
                'choices': [
                    ('Lists are ordered while tuples are unordered', False),
                    ('Lists are mutable, while tuples are immutable', True),
                    ('Tuples can store strings while lists can only store numbers', False),
                    ('Lists use curly braces {} while tuples use brackets []', False),
                ]
            },
            {
                'prompt': 'What will be the output of the code: print(bool("") or bool(0)) ?',
                'points': 2,
                'explanation': 'Both empty string "" and integer 0 are falsy in Python, so bool("") is False and bool(0) is False. False or False evaluates to False.',
                'choices': [
                    ('True', False),
                    ('False', True),
                    ('None', False),
                    ('Error', False),
                ]
            },
            {
                'prompt': 'Which scope resolution order does Python use for variable lookups?',
                'points': 2,
                'explanation': 'Python follows the LEGB hierarchy: Local -> Enclosing -> Global -> Built-in.',
                'choices': [
                    ('Global -> Local -> Built-in -> Enclosing', False),
                    ('Local -> Enclosing -> Global -> Built-in', True),
                    ('Built-in -> Global -> Enclosing -> Local', False),
                    ('Local -> Global -> Enclosing -> Built-in', False),
                ]
            }
        ]

        for q_order, q_item in enumerate(questions_data, start=1):
            q_obj = Question.objects.create(
                quiz=quiz,
                prompt=q_item['prompt'],
                points=q_item['points'],
                explanation=q_item['explanation'],
                order=q_order,
                question_type='single'
            )
            for c_text, is_corr in q_item['choices']:
                Choice.objects.create(
                    question=q_obj,
                    choice_text=c_text,
                    is_correct=is_corr
                )

        self.stdout.write(f"  [OK] Python Essentials 1 seeded ({course.total_lessons_count} lessons, {quiz.questions.count()} quiz questions)")

    def seed_python_essentials_2(self, category, instructor):
        course, _ = Course.objects.update_or_create(
            slug='python-essentials-2',
            defaults={
                'title': 'Python Essentials 2: Advanced Python & OOP Architecture',
                'category': category,
                'instructor': instructor,
                'instructor_name': 'TECHSPIRE Academic Council',
                'short_description': 'Master advanced data structures, Object-Oriented Programming (OOP), modules, packages, exceptions, file handling, generators, and decorators.',
                'description': """Python Essentials 2 takes your programming capabilities to a professional level.

Designed for students and developers who have completed fundamental Python or equivalent concepts, this course dives deep into Object-Oriented Programming (Classes, Inheritance, Polymorphism, Encapsulation), custom modules, packages, robust exception hierarchies, persistent file operations (JSON/CSV), generator pipelines, and decorators.

Master real-world software architecture patterns and prepare for professional Python engineering roles.""",
                'level': 'intermediate',
                'duration_hours': 22.0,
                'is_free': True,
                'price': 0.00,
                'what_you_will_learn': """Master dictionaries, sets, and comprehension expressions for high-performance data processing
Design robust software architectures using Object-Oriented Programming (OOP)
Implement inheritance, method overriding, super(), and polymorphic designs
Enforce encapsulation with private attributes and @property getters/setters
Organize large codebases with custom modules, packages, and __init__.py
Build resilient production apps using comprehensive try-except-finally exception hierarchies
Perform persistent File I/O operations with context managers (JSON, CSV, text)
Write functional generators with yield, lambda functions, and custom decorators""",
                'requirements': """Completion of Python Essentials 1 or solid understanding of basic Python syntax, loops, and functions
A computer with Python 3.10+ and a code editor""",
                'roadmap_highlights': """Module 1: Dictionaries, Sets & Comprehensions
Module 2: Object-Oriented Programming - Classes & Objects
Module 3: Inheritance, Polymorphism & Encapsulation
Module 4: Modules, Packages & Namespaces
Module 5: Exception Handling & Robust Errors
Module 6: File I/O & Persistent Storage
Module 7: Advanced Python: Generators & Decorators
Module 8: Capstone Assessment & Certification""",
                'career_opportunities': """Python Backend Engineer
Software Developer
Data Engineer
Full-Stack Developer (Django / FastAPI)
Test Automation Architect""",
                'has_certificate': True,
                'badge_text': 'Advanced Certification',
                'is_published': True,
                'is_featured': True,
            }
        )

        course.modules.all().delete()

        modules_data = [
            {
                'order': 1,
                'title': 'Advanced Data Structures & Comprehensions',
                'description': 'Master dictionaries (key-value maps), sets (unique collections), and concise list/dict/set comprehensions.',
                'lessons': [
                    {
                        'order': 1,
                        'title': 'Dictionaries: Hash Maps & Key-Value Operations',
                        'duration': 20,
                        'notes': """# Python Dictionaries: Key-Value Hash Maps

A **dictionary** is an ordered (as of Python 3.7+), mutable collection of key-value pairs where keys must be unique and **hashable** (immutable).

---

## 1. Creating & Accessing Dictionaries

```python
student = {
    "id": "TS-1042",
    "name": "Pooja Verma",
    "course": "Python Essentials 2",
    "scores": [88, 92, 95]
}

# Safe key access with get() (avoids KeyError)
email = student.get("email", "not_provided@techspire.in")
print("Student Email:", email)

# Adding and updating keys
student["grade"] = "A+"
student["name"] = "Pooja Sharma"  # Updates existing key
```

---

## 2. Iterating Over Dictionaries

```python
# Iterating keys, values, and key-value items
for key, value in student.items():
    print(f"[{key.upper()}]: {value}")
```
""",
                        'takeaways': """Dictionary keys must be immutable and hashable (strings, numbers, tuples).
Use dict.get(key, default) to prevent KeyErrors when a key might not exist.
Iterate with .items() for key-value pairs, .keys() for keys, and .values() for values.""",
                        'interview': """Q: What is the underlying data structure of a Python dictionary and its average lookup complexity?
A: Python dictionaries are implemented using hash tables with open addressing, providing average O(1) time complexity for lookups, insertions, and deletions.""",
                        'exercise': """### Exercise 1.1: Word Frequency Counter
Write a function `count_words(text)` that takes a sentence and returns a dictionary of word frequencies.""",
                        'solution': """```python
def count_words(text):
    words = text.lower().split()
    freq = {}
    for w in words:
        freq[w] = freq.get(w, 0) + 1
    return freq

sample = "Python is powerful and Python is fast and expressive"
print(count_words(sample))
```"""
                    },
                    {
                        'order': 2,
                        'title': 'Sets & Comprehension Expressions',
                        'duration': 20,
                        'notes': """# Sets & Comprehensions

A **set** is an unordered collection of unique, hashable elements.

---

## 1. Set Operations (Venn Diagram Math)

```python
backend_devs = {"Alex", "Pooja", "Rahul", "Sarah"}
frontend_devs = {"Sarah", "John", "Alex", "Dev"}

# Set Union (|) -> All developers
print("All Devs:", backend_devs | frontend_devs)

# Set Intersection (&) -> Full-Stack developers (in both)
print("Full-Stack Devs:", backend_devs & frontend_devs)

# Set Difference (-) -> Pure backend devs
print("Pure Backend:", backend_devs - frontend_devs)
```

---

## 2. List & Dictionary Comprehensions

Comprehensions provide a concise, readable syntax for generating collections.

```python
# List comprehension: [expression for item in iterable if condition]
numbers = range(1, 11)
even_squares = [n**2 for n in numbers if n % 2 == 0]
print("Even Squares:", even_squares)  # [4, 16, 36, 64, 100]

# Dictionary comprehension
prices_inr = {"Python Book": 499, "Flask Guide": 299, "Django Kit": 799}
discounted_prices = {k: round(v * 0.85, 2) for k, v in prices_inr.items()}
print("Discounted Prices (15% OFF):", discounted_prices)
```
""",
                        'takeaways': """Sets store unique elements and support union (|), intersection (&), and difference (-).
Comprehensions replace boilerplate map() and filter() loops with clean one-liners.""",
                        'interview': """Q: What are the advantages of using comprehensions over standard for loops?
A: Comprehensions are more concise, expressive, and run faster in CPython because loop execution occurs at C-level bytecode speeds.""",
                        'exercise': """### Exercise 1.2: Prime Number Filter with Comprehension
Given `nums = range(2, 30)`, use a list comprehension to filter only prime numbers.""",
                        'solution': """```python
primes = [n for n in range(2, 30) if all(n % d != 0 for d in range(2, int(n**0.5) + 1))]
print("Primes up to 30:", primes)
```"""
                    }
                ]
            },
            {
                'order': 2,
                'title': 'OOP: Classes, Objects & Methods',
                'description': 'Object-Oriented Programming foundations, __init__ constructor, instance attributes, and class vs static methods.',
                'lessons': [
                    {
                        'order': 1,
                        'title': 'Classes, __init__ Constructor & self Parameter',
                        'duration': 25,
                        'notes': """# Classes & Objects in Python

**Object-Oriented Programming (OOP)** models real-world entities into software structures containing state (attributes) and behavior (methods).

---

## 1. Class Blueprint & Constructor

```python
class Student:
    # Class attribute (shared by all instances)
    institution = "TECHSPIRE Academy"

    def __init__(self, full_name, email, enroll_id):
        # Instance attributes (unique to each object)
        self.full_name = full_name
        self.email = email
        self.enroll_id = enroll_id
        self.completed_lessons = 0

    def complete_lesson(self):
        self.completed_lessons += 1
        print(f"{self.full_name} completed a lesson! Total: {self.completed_lessons}")

    def __str__(self):
        return f"Student({self.enroll_id}: {self.full_name})"

# Instantiating objects
s1 = Student("Aarav Patel", "aarav@techspire.in", "TS-201")
s2 = Student("Meera Rao", "meera@techspire.in", "TS-202")

s1.complete_lesson()
s1.complete_lesson()
print(s1)
```
""",
                        'takeaways': """__init__ is the constructor method called automatically upon instance creation.
self refers to the specific instance calling the method.
Class attributes are shared across all instances, while instance attributes belong to specific objects.""",
                        'interview': """Q: What is the purpose of the 'self' keyword in Python class methods?
A: 'self' is an explicit reference to the instance on which the method was called, allowing access to instance attributes and methods.""",
                        'exercise': """### Exercise 2.1: Bank Account Class
Create a `BankAccount` class with `account_holder`, `balance` (default 0), and methods `deposit(amount)`, `withdraw(amount)` with insufficient balance checks.""",
                        'solution': """```python
class BankAccount:
    def __init__(self, account_holder, initial_balance=0.0):
        self.account_holder = account_holder
        self.balance = float(initial_balance)

    def deposit(self, amount):
        if amount > 0:
            self.balance += amount
            print(f"Deposited Rs.{amount:.2f}. New Balance: Rs.{self.balance:.2f}")

    def withdraw(self, amount):
        if 0 < amount <= self.balance:
            self.balance -= amount
            print(f"Withdrew Rs.{amount:.2f}. Remaining Balance: Rs.{self.balance:.2f}")
            return True
        else:
            print("Transaction declined: Insufficient funds.")
            return False

acc = BankAccount("Rahul", 1500)
acc.deposit(500)
acc.withdraw(1200)
```"""
                    }
                ]
            },
            {
                'order': 3,
                'title': 'OOP: Inheritance, Polymorphism & Encapsulation',
                'description': 'Subclassing, super() initialization, method overriding, duck typing, and private variables with property decorators.',
                'lessons': [
                    {
                        'order': 1,
                        'title': 'Inheritance, super() & Polymorphism',
                        'duration': 25,
                        'notes': """# Inheritance & Polymorphism

**Inheritance** allows a child class to inherit attributes and methods from a parent class, promoting code reuse.

---

## 1. Class Inheritance & `super()`

```python
class User:
    def __init__(self, username, email):
        self.username = username
        self.email = email

    def get_role_description(self):
        return "Standard Platform User"

class Instructor(User):
    def __init__(self, username, email, department):
        super().__init__(username, email)  # Call parent constructor
        self.department = department

    # Method Overriding
    def get_role_description(self):
        return f"Faculty Instructor in {self.department}"

inst = Instructor("dr_sharma", "sharma@techspire.in", "Computer Science")
print(inst.username, "->", inst.get_role_description())
```

---

## 2. Polymorphism (Duck Typing)

In Python: *"If it walks like a duck and quacks like a duck, it's a duck."* Functions can operate on any object that implements the required interface.

```python
class PDFExporter:
    def export(self, data):
        return f"Exporting {data} to PDF document"

class CSVExporter:
    def export(self, data):
        return f"Exporting {data} to CSV spreadsheet"

def export_report(exporter, report_data):
    # Polymorphic call: works with any object that has an .export() method
    print(exporter.export(report_data))

export_report(PDFExporter(), "Monthly Quiz Analytics")
export_report(CSVExporter(), "Student Progress Records")
```
""",
                        'takeaways': """super() invokes methods from the parent superclass.
Method overriding replaces parent implementation with specialized child logic.
Polymorphism allows different classes to share identical method signatures.""",
                        'interview': """Q: What is MRO (Method Resolution Order) in Python?
A: MRO is the order in which Python searches for attributes and methods across class hierarchies, calculated using the C3 Linearization algorithm.""",
                        'exercise': """### Exercise 3.1: Shape Hierarchy
Create a base class `Shape` with method `area()`. Implement subclasses `Rectangle(width, height)` and `Circle(radius)` overriding `area()`.""",
                        'solution': """```python
import math

class Shape:
    def area(self):
        raise NotImplementedError("Subclasses must implement area()")

class Rectangle(Shape):
    def __init__(self, width, height):
        self.width = width
        self.height = height

    def area(self):
        return self.width * self.height

class Circle(Shape):
    def __init__(self, radius):
        self.radius = radius

    def area(self):
        return math.pi * (self.radius ** 2)

shapes = [Rectangle(10, 5), Circle(7)]
for s in shapes:
    print(f"{type(s).__name__} Area: {s.area():.2f}")
```"""
                    }
                ]
            },
            {
                'order': 4,
                'title': 'Modules, Packages & Virtual Environments',
                'description': 'Modular code architecture, import syntax, __name__ == "__main__", package structures, and pip package management.',
                'lessons': [
                    {
                        'order': 1,
                        'title': 'Creating Modules, Packages & __name__ Guard',
                        'duration': 20,
                        'notes': """# Modules, Packages & Namespaces

A **module** is simply a `.py` file containing Python definitions and statements. A **package** is a directory containing modules and an `__init__.py` file.

---

## 1. Import Techniques

```python
# Import entire module
import math
print(math.sqrt(144))

# Import specific symbols
from datetime import datetime, timezone
print("Current UTC:", datetime.now(timezone.utc))

# Import with alias
import json as js
data = js.dumps({"status": "active"})
```

---

## 2. The `if __name__ == '__main__':` Guard

When Python runs a file directly, `__name__` is set to `"__main__"`. When imported as a module into another script, `__name__` is set to the module name.

```python
# math_utils.py

def add(a, b):
    return a + b

# Code inside this guard only executes when run directly, NOT when imported!
if __name__ == '__main__':
    print("Testing math_utils directly:")
    print("2 + 3 =", add(2, 3))
```
""",
                        'takeaways': """A module is a .py file; a package is a directory of modules with __init__.py.
Use if __name__ == '__main__' to separate reusable functions from executable script tests.""",
                        'interview': """Q: What is the significance of __init__.py in Python packages?
A: In Python, __init__.py marks a directory as a regular Python package and can execute initialization code or define __all__ exports.""",
                        'exercise': """### Exercise 4.1: Module Inspection
Write a Python script that imports the `math` module and prints all public mathematical functions available in it using `dir(math)`.""",
                        'solution': """```python
import math
public_functions = [f for f in dir(math) if not f.startswith('_')]
print("Total math functions:", len(public_functions))
print("Sample functions:", public_functions[:10])
```"""
                    }
                ]
            },
            {
                'order': 5,
                'title': 'Exceptions & Robust Error Handling',
                'description': 'try, except, else, finally blocks, exception hierarchy, raising exceptions, and creating custom exception classes.',
                'lessons': [
                    {
                        'order': 1,
                        'title': 'Handling Exceptions with try-except-else-finally',
                        'duration': 20,
                        'notes': """# Exception Handling in Python

Exceptions are runtime anomalies that disrupt normal execution flow. Handling them gracefully prevents application crashes.

---

## 1. Complete Exception Handling Block

```python
def safe_divide(a, b):
    try:
        result = a / b
    except ZeroDivisionError as e:
        print(f"Error: Division by zero is prohibited. ({e})")
        return None
    except TypeError as e:
        print(f"Error: Both operands must be numeric. ({e})")
        return None
    else:
        # Executes ONLY if NO exception was raised in try block
        print("Calculation successful!")
        return result
    finally:
        # ALWAYS executes (used for cleanup like closing files/connections)
        print("Execution of safe_divide completed.")

print(safe_divide(10, 2))
print(safe_divide(10, 0))
```

---

## 2. Custom Exception Classes

```python
class InsufficientFundsError(Exception):
    # Raised when a withdrawal exceeds account balance.
    def __init__(self, balance, amount):
        super().__init__(f"Attempted to withdraw Rs.{amount}, but balance is only Rs.{balance}")
        self.balance = balance
        self.amount = amount

def withdraw(balance, amount):
    if amount > balance:
        raise InsufficientFundsError(balance, amount)
    return balance - amount

try:
    withdraw(500, 1200)
except InsufficientFundsError as err:
    print("Caught custom exception:", err)
```
""",
                        'takeaways': """try block tests code, except catches errors, else runs on success, finally always runs.
Inherit from Exception to define domain-specific custom exceptions.
Avoid bare 'except:' clauses; catch specific exception types.""",
                        'interview': """Q: What is the difference between except Exception and bare except: in Python?
A: A bare 'except:' catches all exceptions including SystemExit, KeyboardInterrupt, and GeneratorExit, which can prevent clean script termination. Catching Exception is safer.""",
                        'exercise': """### Exercise 5.1: Robust User Input Parser
Write a function `get_positive_integer(prompt)` that repeatedly prompts the user until they enter a valid positive integer.""",
                        'solution': """```python
def parse_positive_int(raw_input_value):
    try:
        val = int(raw_input_value)
        if val <= 0:
            raise ValueError("Number must be strictly greater than 0")
        return val
    except ValueError as e:
        print(f"Invalid input: {e}")
        return None

print("Parsing '42':", parse_positive_int("42"))
print("Parsing '-5':", parse_positive_int("-5"))
print("Parsing 'abc':", parse_positive_int("abc"))
```"""
                    }
                ]
            },
            {
                'order': 6,
                'title': 'File I/O & Persistent Data Storage',
                'description': 'File operations with context managers (with open), reading/writing text files, JSON serialization, and CSV processing.',
                'lessons': [
                    {
                        'order': 1,
                        'title': 'Working with Files, JSON & CSV Data',
                        'duration': 25,
                        'notes': """# File I/O & Context Managers

Python's `with` statement guarantees that file descriptors and system resources are properly closed even if exceptions occur.

---

## 1. Reading & Writing Text Files

```python
# Writing to a text file
with open("student_notes.txt", "w", encoding="utf-8") as f:
    f.write("TECHSPIRE Learning Notes\n")
    f.write("Topic: Python Essentials 2\n")

# Reading line-by-line
with open("student_notes.txt", "r", encoding="utf-8") as f:
    for line in f:
        print("Line:", line.strip())
```

---

## 2. JSON Serialization (`json` module)

```python
import json

course_record = {
    "course_id": "PY-202",
    "title": "Python Essentials 2",
    "modules": 8,
    "active": True
}

# Serialize dictionary to JSON string
json_str = json.dumps(course_record, indent=2)
print("JSON Representation:\n", json_str)

# Deserialize back to Python dictionary
parsed_dict = json.loads(json_str)
print("Parsed Title:", parsed_dict["title"])
```
""",
                        'takeaways': """Always open files using 'with open(...) as f:' for safe automatic resource cleanup.
Use encoding='utf-8' explicitly to prevent cross-platform character encoding issues.
Use json.dumps()/loads() for in-memory strings and json.dump()/load() for file streams.""",
                        'interview': """Q: What happens under the hood when using the 'with' statement in Python?
A: The 'with' statement invokes the context manager protocol, calling __enter__() at the start and guaranteeing __exit__() is called upon exit to cleanup resources.""",
                        'exercise': """### Exercise 6.1: Student Registry JSON Store
Write a script that creates a dictionary of 3 students with scores, serializes it to a JSON file `students.json`, and then reads it back to calculate class average.""",
                        'solution': """```python
import json

students = [
    {"name": "Ananya", "score": 92},
    {"name": "Karan", "score": 85},
    {"name": "Simran", "score": 78}
]

# Write JSON
with open("students_test.json", "w") as f:
    json.dump(students, f, indent=2)

# Read JSON & Compute Average
with open("students_test.json", "r") as f:
    loaded = json.load(f)
    avg = sum(s["score"] for s in loaded) / len(loaded)
    print("Class Average Score:", round(avg, 2))
```"""
                    }
                ]
            },
            {
                'order': 7,
                'title': 'Advanced Python: Generators & Decorators',
                'description': 'Memory-efficient generators with yield, iterator protocol, first-class functions, and building custom decorators.',
                'lessons': [
                    {
                        'order': 1,
                        'title': 'Generators (yield) & Function Decorators',
                        'duration': 25,
                        'notes': """# Generators & Decorators in Python

---

## 1. Generators & Lazy Evaluation (`yield`)

A **generator function** produces a sequence of values on-demand using `yield`, maintaining its state between successive calls without loading entire sequences into memory.

```python
def fibonacci_sequence(limit):
    a, b = 0, 1
    count = 0
    while count < limit:
        yield a
        a, b = b, a + b
        count += 1

# Consuming the generator lazily
for num in fibonacci_sequence(8):
    print(num, end=" ")  # 0 1 1 2 3 5 8 13
print()
```

---

## 2. Function Decorators

A **decorator** is a higher-order function that takes another function as an argument, extends its behavior without modifying it, and returns the modified function.

```python
import time
from functools import wraps

def benchmark(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        start_time = time.time()
        result = func(*args, **kwargs)
        elapsed = (time.time() - start_time) * 1000
        print(f"[{func.__name__}] executed in {elapsed:.4f} ms")
        return result
    return wrapper

@benchmark
def compute_heavy_sum(limit):
    return sum(i**2 for i in range(limit))

print("Result:", compute_heavy_sum(1000000))
```
""",
                        'takeaways': """Generators use yield to produce values on-demand with O(1) memory complexity.
Decorators use @syntax to wrap and enhance functions cleanly.
Use functools.wraps on wrapper functions to preserve original docstrings and names.""",
                        'interview': """Q: What is the key difference between return and yield in Python?
A: 'return' terminates the function and returns a single value. 'yield' pauses the function execution, yields a value to the caller, and can be resumed from that exact point on the next iteration.""",
                        'exercise': """### Exercise 7.1: Upper Case Decorator
Create a decorator `@uppercase_output` that intercepts the string returned by any function and transforms it to uppercase.""",
                        'solution': """```python
from functools import wraps

def uppercase_output(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        res = func(*args, **kwargs)
        return str(res).upper()
    return wrapper

@uppercase_output
def get_greeting(name):
    return f"Hello, {name}! Welcome to Techspire."

print(get_greeting("Indore Student"))
```"""
                    }
                ]
            },
            {
                'order': 8,
                'title': 'Capstone Assessment & Certification Exam',
                'description': 'Comprehensive assessment covering advanced data structures, OOP architecture, exceptions, file handling, and decorators.',
                'lessons': [
                    {
                        'order': 1,
                        'title': 'Python Essentials 2: Capstone Project & Certification',
                        'duration': 30,
                        'notes': """# Python Essentials 2: Capstone Review

You have reached the capstone milestone of **Python Essentials 2: Advanced Python & OOP Architecture**!

---

## Advanced Architecture Competencies

- [x] High-performance dictionary key-value operations and Set math
- [x] Clean List, Dict, and Set comprehension expressions
- [x] Object-Oriented Programming (Classes, Methods, Class vs Static Methods)
- [x] Inheritance, super() initialization, and Polymorphism
- [x] Encapsulation with `@property` getters and setters
- [x] Custom modules, packages, and `__name__ == '__main__'` guards
- [x] Bulletproof `try-except-else-finally` exception handling
- [x] File persistence with Context Managers (Text, JSON, CSV)
- [x] Memory-optimized Generators with `yield`
- [x] Reusable Function Decorators with `@wraps`

---

Proceed to the **Python Essentials 2 Certification Exam** below to earn your verified credential!
""",
                        'takeaways': """Review OOP principles, exception handling, and generator patterns.
Score 70% or higher to pass the assessment and receive your verified certificate.""",
                        'interview': """Q: What are Python magic methods (dunder methods)?
A: Special methods with double underscores (e.g. __init__, __str__, __repr__, __len__, __getitem__) that allow custom classes to integrate seamlessly with Python's built-in syntax and operators.""",
                        'exercise': """### Capstone Problem: Custom Context Manager
Write a custom context manager class `Timer` using __enter__ and __exit__ that measures the elapsed time of a code block.""",
                        'solution': """```python
import time

class Timer:
    def __enter__(self):
        self.start = time.perf_counter()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.elapsed = time.perf_counter() - self.start
        print(f"Elapsed Time: {self.elapsed * 1000:.2f} ms")

with Timer():
    total = sum(x**2 for x in range(500000))
```"""
                    }
                ]
            }
        ]

        for m_data in modules_data:
            module = Module.objects.create(
                course=course,
                title=m_data['title'],
                description=m_data['description'],
                order=m_data['order']
            )

            for l_data in m_data['lessons']:
                Lesson.objects.create(
                    module=module,
                    title=l_data['title'],
                    order=l_data['order'],
                    lesson_type='article',
                    duration_minutes=l_data['duration'],
                    notes_markdown=l_data['notes'],
                    key_takeaways=l_data.get('takeaways', ''),
                    interview_tips=l_data.get('interview', ''),
                    practice_exercise=l_data.get('exercise', ''),
                    exercise_solution=l_data.get('solution', ''),
                    is_preview=(m_data['order'] == 1 and l_data['order'] == 1)
                )

        # Seed Quiz for Python Essentials 2
        quiz, _ = Quiz.objects.update_or_create(
            course=course,
            title='Python Essentials 2: Advanced Certification Exam',
            defaults={
                'description': 'Advanced assessment covering OOP principles, inheritance, encapsulation, exceptions, file I/O, generators, and decorators.',
                'pass_percentage': 70,
                'time_limit_minutes': 25,
                'max_attempts': 5,
                'is_published': True
            }
        )
        quiz.questions.all().delete()

        questions_data = [
            {
                'prompt': 'What will be the output of: {x: x**2 for x in (1, 2, 3)} ?',
                'points': 2,
                'explanation': 'This is a dictionary comprehension creating keys 1, 2, 3 mapped to their squares: {1: 1, 2: 4, 3: 9}.',
                'choices': [
                    ('{1: 1, 2: 4, 3: 9}', True),
                    ('[1, 4, 9]', False),
                    ('{(1, 1), (2, 4), (3, 9)}', False),
                    ('{1, 4, 9}', False),
                ]
            },
            {
                'prompt': 'Which method is called in a child class to invoke the constructor of its parent class?',
                'points': 2,
                'explanation': 'super().__init__() calls the constructor of the parent superclass in Python 3.',
                'choices': [
                    ('super().__init__()', True),
                    ('parent.__init__()', False),
                    ('this.__init__()', False),
                    ('base.construct()', False),
                ]
            },
            {
                'prompt': 'What keyword turns a standard Python function into a Generator?',
                'points': 2,
                'explanation': 'The "yield" keyword pauses the function and yields values lazily, converting it into a generator function.',
                'choices': [
                    ('yield', True),
                    ('generate', False),
                    ('async', False),
                    ('return', False),
                ]
            },
            {
                'prompt': 'In a try-except statement, when does the "else" block execute?',
                'points': 2,
                'explanation': 'The else block in exception handling executes ONLY when NO exception was raised in the try block.',
                'choices': [
                    ('Only when an exception occurs', False),
                    ('Only when NO exception is raised in the try block', True),
                    ('Always after the finally block', False),
                    ('Only when the catch block fails', False),
                ]
            },
            {
                'prompt': 'What is the average time complexity for key lookup in a Python dictionary?',
                'points': 2,
                'explanation': 'Python dictionaries use hash tables, giving average O(1) constant time lookups.',
                'choices': [
                    ('O(1)', True),
                    ('O(n)', False),
                    ('O(log n)', False),
                    ('O(n^2)', False),
                ]
            },
            {
                'prompt': 'Which decorator is used to define a getter property in an Object-Oriented class?',
                'points': 2,
                'explanation': 'The @property decorator allows a method to be accessed like an attribute (getter).',
                'choices': [
                    ('@property', True),
                    ('@getter', False),
                    ('@accessor', False),
                    ('@classmethod', False),
                ]
            },
            {
                'prompt': 'What is the primary benefit of opening files using "with open(...) as f:" ?',
                'points': 2,
                'explanation': 'The context manager automatically closes the file stream even if an exception occurs inside the block.',
                'choices': [
                    ('It encrypts the file automatically', False),
                    ('It guarantees the file is properly closed when exiting the block', True),
                    ('It loads the entire file into CPU cache', False),
                    ('It bypasses OS file permissions', False),
                ]
            }
        ]

        for q_order, q_item in enumerate(questions_data, start=1):
            q_obj = Question.objects.create(
                quiz=quiz,
                prompt=q_item['prompt'],
                points=q_item['points'],
                explanation=q_item['explanation'],
                order=q_order,
                question_type='single'
            )
            for c_text, is_corr in q_item['choices']:
                Choice.objects.create(
                    question=q_obj,
                    choice_text=c_text,
                    is_correct=is_corr
                )

        self.stdout.write(f"  [OK] Python Essentials 2 seeded ({course.total_lessons_count} lessons, {quiz.questions.count()} quiz questions)")

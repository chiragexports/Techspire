"""
Comprehensive 23 Chapters Data for Python Programming: Zero to Professional Masterclass.
"""

PYTHON_CHAPTERS_23 = [
    {
        'order': 1,
        'title': 'Chapter 1: Python Fundamentals, Syntax & Memory Model',
        'is_preview': True,
        'read_time_mins': 25,
        'summary': 'Interpreter execution flow, bytecode compilation, PVM, dynamic typing, variables, and memory references.',
        'content': '''# Chapter 1: Python Fundamentals, Syntax & Memory Model

## Learning Objectives
- Understand Python's execution model: Source Code -> Bytecode -> PVM.
- Master variable assignment and Python's heap memory reference model.
- Learn naming conventions (PEP 8), keywords, and primitive data types.
- Control program flow using conditional statements, `for` loops, `while` loops, `break`, `continue`, and `pass`.

---

## 1. What is Python and How It Works
Python is a high-level, interpreted, dynamically typed language created by Guido van Rossum.

```
[ Source Code (.py) ]
         │
         ▼
[ Python Interpreter / Compiler ] ──► Generates Bytecode (.pyc)
         │
         ▼
[ Python Virtual Machine (PVM) ]  ──► Executes Bytecode on CPU
```

> [!IMPORTANT]
> Python is both compiled and interpreted. The interpreter first translates `.py` files into intermediate **Bytecode** before the PVM executes it.

---

## 2. Variables and Memory Model (References vs Values)
In Python, variables are names that reference objects residing in heap memory.

```python
# Variables store memory addresses (references)
a = [1, 2, 3]
b = a
b.append(4)

print(a)  # Output: [1, 2, 3, 4] -> Both a and b point to the SAME object!
print(id(a) == id(b))  # Output: True
```

---

## 3. Control Flow & Loops
```python
# For loop with enumerate and range
fruits = ['apple', 'banana', 'cherry']
for index, fruit in enumerate(fruits, start=1):
    print(f"{index}. {fruit.capitalize()}")

# While loop with break/continue
counter = 0
while counter < 10:
    counter += 1
    if counter % 2 == 0:
        continue  # Skip even numbers
    if counter > 7:
        break     # Exit loop
    print(f"Odd: {counter}")
```

---

## Common Mistakes & Best Practices
- **Mistake**: Checking boolean variables with `if x == True:` instead of pythonic `if x:`.
- **Best Practice**: Adhere to PEP 8: `snake_case` for variables/functions, `UPPER_CASE` for constants, `PascalCase` for classes.

## Interview Q&A
**Q: Is Python call-by-value or call-by-reference?**
*A: Python is "Call-by-Object-Reference" (or Call-by-Sharing). If you pass a mutable object (like a list/dict) and modify it in-place, the change reflects outside. If you pass an immutable object (int, str, tuple), reassignment binds a new object locally.*
''',
        'takeaways': 'Python compiles to bytecode first; variables are references to heap objects; use PEP 8 conventions.',
        'interview': 'Explain Python memory management, reference counting, and Garbage Collector (gc module).',
        'exercise': 'Write a program that takes a sentence from user input and counts the frequency of uppercase, lowercase, digits, and whitespace.',
        'solution': '''```python
def analyze_string(text):
    stats = {'upper': 0, 'lower': 0, 'digits': 0, 'spaces': 0}
    for char in text:
        if char.isupper(): stats['upper'] += 1
        elif char.islower(): stats['lower'] += 1
        elif char.isdigit(): stats['digits'] += 1
        elif char.isspace(): stats['spaces'] += 1
    return stats
```'''
    },
    {
        'order': 2,
        'title': 'Chapter 2: Python Data Structures (Strings, Lists, Tuples, Sets, Dicts)',
        'is_preview': False,
        'read_time_mins': 35,
        'summary': 'Deep dive into mutable vs immutable data structures, hash tables, slicing, time complexity, and comprehensions.',
        'content': '''# Chapter 2: Python Data Structures Deep Dive

## Learning Objectives
- Master the internal mechanics of Strings, Lists, Tuples, Sets, and Dictionaries.
- Understand Time Complexity $O(1)$ vs $O(N)$ for common operations.
- Write expressive List, Dictionary, and Set Comprehensions.

---

## 1. Summary of Built-in Structures

| Structure | Mutable? | Ordered? | Duplicate Keys/Values? | Internal Implementation |
| :--- | :--- | :--- | :--- | :--- |
| **String** | No | Yes | Yes | Contiguous char array in memory |
| **List** | Yes | Yes | Yes | Dynamic Array (over-allocated pointers) |
| **Tuple** | No | Yes | Yes | Fixed-size array (faster than list) |
| **Set** | Yes | No | Unique only | Hash Table (dummy values) |
| **Dictionary** | Yes | Yes (3.7+) | Unique Keys | Compact Hash Table ($O(1)$ average lookup) |

---

## 2. Advanced Comprehensions
```python
# List comprehension with condition
squares = [x**2 for x in range(1, 11) if x % 2 == 0]

# Dictionary comprehension (inverting a mapping)
original = {'a': 1, 'b': 2, 'c': 3}
inverted = {v: k for k, v in original.items()}
# Result: {1: 'a', 2: 'b', 3: 'c'}
```
''',
        'takeaways': 'Dict and Set lookups are O(1) average due to hash tables; Lists are dynamic arrays with O(1) amortized append.',
        'interview': 'Why cannot a list or dictionary be used as a dictionary key or set element? (Answer: Because they are mutable and unhashable).',
    },
    {
        'order': 3,
        'title': 'Chapter 3: Functions, Scopes, LEGB, Lambda & Recursion',
        'is_preview': False,
        'read_time_mins': 30,
        'summary': 'Function definitions, *args, **kwargs, default argument traps, LEGB rule, lambda expressions, and recursion.',
        'content': '''# Chapter 3: Functions, Scopes & Functional Constructs

## 1. The LEGB Scope Resolution Rule
When Python resolves a variable name, it checks scopes in this strict order:
1. **L**ocal — Variables defined inside current function
2. **E**nclosing — Enclosing functions (closures)
3. **G**lobal — Top-level script/module variables
4. **B**uilt-in — Pre-defined names like `len`, `range`, `print`

## 2. Flexible Arguments: `*args` and `**kwargs`
```python
def build_api_endpoint(base_url, *path_segments, **query_params):
    path = "/".join(str(s).strip("/") for s in path_segments)
    query_str = "&".join(f"{k}={v}" for k, v in query_params.items())
    full_url = f"{base_url.rstrip('/')}/{path}"
    return f"{full_url}?{query_str}" if query_str else full_url

url = build_api_endpoint("https://api.techspire.in", "v1", "courses", category="python", limit=10)
# Output: https://api.techspire.in/v1/courses?category=python&limit=10
```
''',
        'takeaways': 'Never use mutable default arguments like def foo(x=[]); use def foo(x=None) instead.',
        'interview': 'What is the default argument trap in Python functions?',
    },
    {
        'order': 4,
        'title': 'Chapter 4: Modules, Packages, Virtual Environments & Packaging',
        'is_preview': False,
        'read_time_mins': 25,
        'summary': '__init__.py, __name__ == "__main__", sys.path, pip, venv, pyproject.toml, and modular package architecture.',
        'content': '''# Chapter 4: Modules, Packages & Virtual Environments

## 1. Module vs Package Architecture
- **Module**: A single Python file (`math_utils.py`).
- **Package**: A directory containing Python modules and an `__init__.py` file.

```
my_project/
├── pyproject.toml
├── src/
│   └── my_package/
│       ├── __init__.py
│       ├── core.py
│       └── utils.py
└── tests/
    └── test_core.py
```

## 2. The `if __name__ == "__main__":` idiom
When a file is run directly: `__name__` is set to `"__main__"`.
When imported: `__name__` is set to the module's import path.
''',
        'takeaways': 'Always isolate dependencies using venv or uv; understand sys.path and relative vs absolute imports.',
        'interview': 'What is the role of __init__.py in Python packages?',
    },
    {
        'order': 5,
        'title': 'Chapter 5: File Handling (Text, CSV, JSON, Binary & Pathlib)',
        'is_preview': False,
        'read_time_mins': 30,
        'summary': 'File I/O modes, context managers (with), pathlib module, CSV parsing, JSON serialization, and binary file streams.',
        'content': '''# Chapter 5: Robust File Handling & Serialization

## 1. Modern File Handling with `pathlib`
```python
from pathlib import Path
import json

data_dir = Path("data")
data_dir.mkdir(exist_ok=True)

file_path = data_dir / "students.json"
payload = {"school": "TECHSPIRE", "students": [{"id": 1, "name": "Aarav"}]}

# Writing JSON cleanly
file_path.write_text(json.dumps(payload, indent=2), encoding="utf-8")

# Reading JSON
loaded_data = json.loads(file_path.read_text(encoding="utf-8"))
print(loaded_data["school"])  # Output: TECHSPIRE
```
''',
        'takeaways': 'Always use `with open(...)` to guarantee deterministic file descriptor closure; prefer `pathlib.Path`.',
        'interview': 'What is the difference between text mode ("r") and binary mode ("rb") in file I/O?',
    },
    {
        'order': 6,
        'title': 'Chapter 6: Exception Handling, Custom Exceptions & Error Hierarchy',
        'is_preview': False,
        'read_time_mins': 25,
        'summary': 'try-except-else-finally, exception hierarchies, raising exceptions, and building custom domain exception classes.',
        'content': '''# Chapter 6: Production Exception Handling

## 1. Complete Exception Syntax Lifecycle
```python
try:
    value = int(user_input)
    result = 100 / value
except ValueError as e:
    print(f"Invalid input integer: {e}")
except ZeroDivisionError:
    print("Cannot divide by zero!")
else:
    # Executes ONLY if NO exception was raised in try block
    print(f"Calculation succeeded: {result}")
finally:
    # ALWAYS executes regardless of errors (cleanup resources)
    print("Execution complete.")
```

## 2. Custom Domain Exception Hierarchy
```python
class TechspireError(Exception):
    """Base exception for LMS domain errors."""
    pass

class InsufficientBalanceError(TechspireError):
    def __init__(self, required, available):
        super().__init__(f"Required ₹{required}, but available balance is only ₹{available}.")
        self.required = required
        self.available = available
```
''',
        'takeaways': 'Never catch bare `except:`; always catch specific exceptions; use `else` for code that runs only on success.',
        'interview': 'Explain the difference between `except Exception:` and `except BaseException:`.',
    },
    {
        'order': 7,
        'title': 'Chapter 7: Object-Oriented Programming (OOP) Architecture Mastery',
        'is_preview': False,
        'read_time_mins': 45,
        'summary': 'Classes, objects, dunder methods, encapsulation, inheritance, polymorphism, MRO, ABC, and real-world banking systems.',
        'content': '''# Chapter 7: Object-Oriented Programming (OOP) Architecture

## 1. Class Architecture & Real-World Banking System
```
          ┌────────────────────────┐
          │     Account (ABC)      │
          ├────────────────────────┤
          │ - account_number: str  │
          │ - holder_name: str     │
          │ - _balance: float      │
          ├────────────────────────┤
          │ + deposit(amount)      │
          │ + withdraw(amount)*    │
          │ + get_balance()        │
          └───────────┬────────────┘
                      │
         ┌────────────┴────────────┐
         ▼                         ▼
┌──────────────────┐      ┌──────────────────┐
│  SavingsAccount  │      │  CurrentAccount  │
├──────────────────┤      ├──────────────────┤
│ - interest_rate  │      │ - overdraft_limit│
└──────────────────┘      └──────────────────┘
```

```python
from abc import ABC, abstractmethod

class Account(ABC):
    def __init__(self, account_number: str, holder_name: str, initial_balance: float = 0.0):
        self.account_number = account_number
        self.holder_name = holder_name
        self._balance = max(0.0, initial_balance)

    @abstractmethod
    def withdraw(self, amount: float) -> bool:
        pass

    def deposit(self, amount: float) -> None:
        if amount <= 0:
            raise ValueError("Deposit amount must be positive.")
        self._balance += amount

    @property
    def balance(self) -> float:
        return self._balance

class SavingsAccount(Account):
    def __init__(self, account_number: str, holder_name: str, min_balance: float = 1000.0, **kwargs):
        super().__init__(account_number, holder_name, **kwargs)
        self.min_balance = min_balance

    def withdraw(self, amount: float) -> bool:
        if self._balance - amount >= self.min_balance:
            self._balance -= amount
            return True
        return False
```
''',
        'takeaways': 'Master OOP pillars: Encapsulation (private/protected conventions), Inheritance, Polymorphism, Abstraction.',
        'interview': 'Explain Python MRO (Method Resolution Order) and the C3 Linearization algorithm.',
    },
    {
        'order': 8,
        'title': 'Chapter 8: Advanced Python (Iterators, Generators, Decorators, Closures & Descriptors)',
        'is_preview': False,
        'read_time_mins': 40,
        'summary': 'Iterables vs Iterators, yield generators, parameterized decorators, closures, contextlib, descriptors, and match-case.',
        'content': '''# Chapter 8: Advanced Python Metaprogramming & Paradigms

## 1. Timing Decorator with Arguments
```python
import time
from functools import wraps

def retry(max_attempts=3, delay_sec=1):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            attempts = 0
            while attempts < max_attempts:
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    attempts += 1
                    if attempts == max_attempts:
                        raise e
                    time.sleep(delay_sec)
        return wrapper
    return decorator

@retry(max_attempts=3, delay_sec=0.5)
def fetch_remote_data():
    # Network request simulation
    return {"status": "success"}
```
''',
        'takeaways': 'Decorators wrap and modify function behavior dynamically; generators provide lazy memory-efficient stream processing.',
        'interview': 'What is the purpose of @wraps from functools in custom decorators?',
    },
    {
        'order': 9,
        'title': 'Chapter 9: Regular Expressions (Regex) in Python',
        'is_preview': False,
        'read_time_mins': 30,
        'summary': 'Character classes, quantifiers, non-greedy matching, capturing groups, lookahead, lookbehind, and the re module.',
        'content': '''# Chapter 9: Regular Expressions (`re` Module)

## 1. Practical Patterns for Validation
```python
import re

# Email validation pattern with named capturing groups
EMAIL_REGEX = re.compile(r'^(?P<username>[a-zA-Z0-9_.+-]+)@(?P<domain>[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+)$')

match = EMAIL_REGEX.match("student@techspire.in")
if match:
    print(f"Username: {match.group('username')}")  # student
    print(f"Domain: {match.group('domain')}")      # techspire.in
```
''',
        'takeaways': 'Pre-compile regex with re.compile() for high-frequency loops; understand greedy vs non-greedy quantifiers (* vs *?).',
        'interview': 'Explain the difference between re.search() and re.match().',
    },
    {
        'order': 10,
        'title': 'Chapter 10: Database Engineering & SQLite Integration',
        'is_preview': False,
        'read_time_mins': 35,
        'summary': 'Relational DB concepts, sqlite3 module, parameterized queries, SQL injection prevention, transactions, and commit/rollback.',
        'content': '''# Chapter 10: Relational Databases & SQLite3

## 1. Parameterized Queries to Prevent SQL Injection
```python
import sqlite3

conn = sqlite3.connect("techspire_lms.db")
cursor = conn.cursor()

# Safe parameterized query
user_email = "student@techspire.in"
cursor.execute("SELECT id, username, first_name FROM accounts_user WHERE email = ?", (user_email,))
user = cursor.fetchone()
print(user)
conn.close()
```
''',
        'takeaways': 'Never format raw user strings into SQL queries; always use parameterized placeholders (?) to prevent SQL injection.',
        'interview': 'What is ACID in database transactions and how is it maintained in Python SQLite?',
    },
    {
        'order': 11,
        'title': 'Chapter 11: Web APIs & RESTful Services Integration',
        'is_preview': False,
        'read_time_mins': 30,
        'summary': 'HTTP lifecycle, request-response models, REST principles, JSON parsing, Requests library, session pooling, and auth.',
        'content': '''# Chapter 11: Web APIs & RESTful Services

## 1. Consuming REST APIs with `requests.Session`
```python
import requests

session = requests.Session()
session.headers.update({
    "User-Agent": "TECHSPIRE-Client/2.0",
    "Accept": "application/json"
})

response = session.get("https://jsonplaceholder.typicode.com/posts/1", timeout=5)
if response.status_code == 200:
    post_data = response.json()
    print(f"Title: {post_data['title']}")
```
''',
        'takeaways': 'Use requests.Session() for connection pooling; always specify explicit timeouts on network calls.',
        'interview': 'Explain HTTP status codes: 200 OK, 201 Created, 400 Bad Request, 401 Unauthorized, 403 Forbidden, 500 Internal Error.',
    },
    {
        'order': 12,
        'title': 'Chapter 12: Computer Networking Fundamentals for Python Developers',
        'is_preview': False,
        'read_time_mins': 30,
        'summary': 'OSI model, TCP/IP stack, IP addressing, ports, DNS lookup, TCP vs UDP protocols, packets, and 3-way handshake.',
        'content': '''# Chapter 12: Computer Networking Fundamentals

## 1. TCP vs UDP Protocol Comparison

| Feature | TCP (Transmission Control Protocol) | UDP (User Datagram Protocol) |
| :--- | :--- | :--- |
| **Connection** | Connection-Oriented (3-way handshake) | Connectionless |
| **Reliability** | Guaranteed delivery (ACK + Retransmit) | Unreliable (Best-effort delivery) |
| **Ordering** | Guarantees ordered packet arrival | Packets may arrive out of order |
| **Speed** | Moderate (Header overhead: 20 bytes) | Ultra-fast (Header overhead: 8 bytes) |
| **Use Cases** | HTTP/HTTPS, WebSockets, File transfer | Video Streaming, Gaming, DNS, VoIP |
''',
        'takeaways': 'TCP provides reliable ordered stream communication; UDP provides fast lightweight datagrams without ACK guarantees.',
        'interview': 'Describe the TCP 3-way handshake (SYN, SYN-ACK, ACK).',
    },
    {
        'order': 13,
        'title': 'Chapter 13: Socket Programming in Python (TCP & UDP Multi-Client)',
        'is_preview': False,
        'read_time_mins': 45,
        'summary': 'Socket API, bind, listen, accept, connect, send, recv, building a multi-client concurrent TCP chat room.',
        'content': '''# Chapter 13: Socket Programming in Python

## 1. TCP Server & Multi-Client Architecture
```
[ Client 1 ] ──── (Connect) ────┐
                                 ▼
[ Client 2 ] ──── (Connect) ──► [ TCP Server (Port 8080) ]
                                 ▲   ├── Thread 1 (Handles Client 1)
[ Client 3 ] ──── (Connect) ────┘   ├── Thread 2 (Handles Client 2)
                                     └── Thread 3 (Handles Client 3)
```

```python
# Multi-threaded TCP Server
import socket
import threading

def handle_client(conn, addr):
    print(f"[NEW CONNECTION] {addr} connected.")
    try:
        while True:
            data = conn.recv(1024)
            if not data: break
            conn.sendall(b"ECHO: " + data)
    finally:
        conn.close()

def start_server(host='127.0.0.1', port=8080):
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((host, port))
    server.listen(5)
    print(f"[LISTENING] Server running on {host}:{port}")
    while True:
        conn, addr = server.accept()
        t = threading.Thread(target=handle_client, args=(conn, addr))
        t.start()
```
''',
        'takeaways': 'A TCP socket lifecycle: socket() -> bind() -> listen() -> accept() -> send/recv -> close().',
        'interview': 'What happens when you call socket.listen(backlog)? What does the backlog parameter represent?',
    },
    {
        'order': 14,
        'title': 'Chapter 14: Multithreading & Concurrency in Python',
        'is_preview': False,
        'read_time_mins': 35,
        'summary': 'Process vs Thread, Global Interpreter Lock (GIL), ThreadPoolExecutor, race conditions, Lock, and Deadlocks.',
        'content': '''# Chapter 14: Multithreading & Concurrency

## 1. Concurrency with `ThreadPoolExecutor`
```python
from concurrent.futures import ThreadPoolExecutor
import time

def process_item(item_id):
    time.sleep(0.1)  # Simulate I/O operation
    return f"Processed item {item_id}"

with ThreadPoolExecutor(max_workers=5) as executor:
    results = list(executor.map(process_item, range(1, 11)))

print(results[:3])
```
''',
        'takeaways': 'Python multithreading is ideal for I/O-bound tasks (network, disk) due to the Global Interpreter Lock (GIL).',
        'interview': 'What is the Python GIL (Global Interpreter Lock) and how does it impact multi-core CPU-bound tasks?',
    },
    {
        'order': 15,
        'title': 'Chapter 15: Multiprocessing & Parallel Computing',
        'is_preview': False,
        'read_time_mins': 35,
        'summary': 'Bypassing the GIL with multiprocessing, Process, Pool, Queue, Pipe, and ProcessPoolExecutor for CPU-heavy tasks.',
        'content': '''# Chapter 15: Multiprocessing for CPU-Bound Workloads

## 1. Parallel Number Crunching with `ProcessPoolExecutor`
```python
from concurrent.futures import ProcessPoolExecutor

def compute_heavy_square(n):
    return n * n

if __name__ == '__main__':
    with ProcessPoolExecutor() as executor:
        numbers = [1_000_000, 2_000_000, 3_000_000]
        results = list(executor.map(compute_heavy_square, numbers))
        print("Parallel Results:", results)
```
''',
        'takeaways': 'Multiprocessing spawns separate OS processes with individual memory spaces and independent PVMs, bypassing the GIL completely.',
        'interview': 'When should you use Multithreading vs Multiprocessing in Python?',
    },
    {
        'order': 16,
        'title': 'Chapter 16: Asynchronous Programming with Asyncio',
        'is_preview': False,
        'read_time_mins': 35,
        'summary': 'Event loop, coroutines, async/await keywords, asyncio.gather, Task management, and non-blocking asynchronous HTTP.',
        'content': '''# Chapter 16: Asynchronous Programming (`asyncio`)

## 1. Single-Threaded High-Performance Concurrency
```python
import asyncio

async def fetch_api(source_name, delay):
    print(f"Starting fetch: {source_name}")
    await asyncio.sleep(delay)
    print(f"Finished fetch: {source_name}")
    return {source_name: "200 OK"}

async def main():
    results = await asyncio.gather(
        fetch_api("User Service", 1.5),
        fetch_api("Order Service", 1.0),
        fetch_api("Payment Service", 0.5)
    )
    print("Combined API responses:", results)

# asyncio.run(main())
```
''',
        'takeaways': 'Asyncio uses cooperative multitasking over a single event loop to handle thousands of concurrent I/O connections.',
        'interview': 'Explain the difference between a synchronous function and a Python coroutine.',
    },
    {
        'order': 17,
        'title': 'Chapter 17: Automated Testing with Pytest & Unittest',
        'is_preview': False,
        'read_time_mins': 30,
        'summary': 'Test-driven development, unittest module, pytest framework, fixtures, parameterized tests, and mock testing.',
        'content': '''# Chapter 17: Automated Testing with Pytest

## 1. Pytest Test Suites & Fixtures
```python
import pytest

def calculate_discount(amount, discount_pct):
    if amount < 0 or discount_pct < 0 or discount_pct > 100:
        raise ValueError("Invalid pricing parameters.")
    return round(amount * (1 - discount_pct / 100), 2)

@pytest.mark.parametrize("amt, pct, expected", [
    (100, 10, 90.0),
    (299, 20, 239.2),
    (500, 0, 500.0)
])
def test_calculate_discount(amt, pct, expected):
    assert calculate_discount(amt, pct) == expected
```
''',
        'takeaways': 'Automated tests ensure non-breaking refactors; use pytest fixtures for clean setup and teardown.',
        'interview': 'What is mocking in unit tests and why is unittest.mock.patch used?',
    },
    {
        'order': 18,
        'title': 'Chapter 18: Logging, Debugging & Performance Profiling',
        'is_preview': False,
        'read_time_mins': 25,
        'summary': 'Python logging module, log levels, file handlers, formatters, Python Debugger (PDB), and cProfile benchmarking.',
        'content': '''# Chapter 18: Production Logging & Debugging

## 1. Production Logging Setup
```python
import logging

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s [%(levelname)s] %(name)s (%(filename)s:%(lineno)d): %(message)s',
    handlers=[
        logging.StreamHandler(),
        logging.FileHandler("app.log", encoding="utf-8")
    ]
)
logger = logging.getLogger("TECHSPIRE.Auth")
logger.info("User student@techspire.in logged in successfully.")
```
''',
        'takeaways': 'Never use print() for production error tracking; configure proper logging handlers and log levels.',
        'interview': 'What are the 5 standard Python logging levels in order of severity? (DEBUG, INFO, WARNING, ERROR, CRITICAL).',
    },
    {
        'order': 19,
        'title': 'Chapter 19: Python for Automation & Practical Scripting',
        'is_preview': False,
        'read_time_mins': 30,
        'summary': 'Automating filesystem cleanup, bulk file renaming, CSV/Excel data transformation, and scheduled job automation.',
        'content': '''# Chapter 19: Automation Scripting

## 1. Automatic File Organizer Script
```python
from pathlib import Path
import shutil

def organize_downloads(folder_path):
    folder = Path(folder_path)
    CATEGORIES = {
        'PDFs': ['.pdf'],
        'Images': ['.jpg', '.jpeg', '.png', '.svg'],
        'Code': ['.py', '.js', '.html', '.css', '.json'],
        'Archives': ['.zip', '.tar', '.gz']
    }
    for file in folder.iterdir():
        if file.is_file():
            for category, extensions in CATEGORIES.items():
                if file.suffix.lower() in extensions:
                    dest_dir = folder / category
                    dest_dir.mkdir(exist_ok=True)
                    shutil.move(str(file), str(dest_dir / file.name))
                    break
```
''',
        'takeaways': 'Automation scripts eliminate manual repetitive work; use shutil and pathlib for safe filesystem operations.',
        'interview': 'How can you run a Python automation script on a recurring schedule on Linux (cron) vs Windows (Task Scheduler)?',
    },
    {
        'order': 20,
        'title': 'Chapter 20: Professional Python Project Structure & Packaging',
        'is_preview': False,
        'read_time_mins': 25,
        'summary': 'Standard layout, pyproject.toml, src/ layout, semantic versioning, clean architecture, and CI/CD pipelines.',
        'content': '''# Chapter 20: Production Python Project Layout

## 1. Standard Production Directory Structure
```
techspire_app/
├── pyproject.toml
├── README.md
├── .gitignore
├── requirements.txt
├── src/
│   └── techspire_app/
│       ├── __init__.py
│       ├── core/
│       ├── models/
│       └── utils/
└── tests/
    ├── __init__.py
    └── test_core.py
```
''',
        'takeaways': 'Use pyproject.toml as the modern unified configuration standard for Python packages (PEP 518/621).',
        'interview': 'What is the difference between requirements.txt and pyproject.toml in modern Python development?',
    },
    {
        'order': 21,
        'title': 'Chapter 21: Real-World Capstone Projects Walkthrough',
        'is_preview': False,
        'read_time_mins': 45,
        'summary': 'Complete implementations: Multi-client Socket Chat, Student Management System, Expense Tracker, and REST API Client.',
        'content': '''# Chapter 21: Real-World Portfolio Projects

## Project 1: Command-Line Expense Tracker & Visualizer
```python
import json
from datetime import datetime

class ExpenseTracker:
    def __init__(self, filename="expenses.json"):
        self.filename = filename
        self.expenses = self._load()

    def add_expense(self, category, amount, description=""):
        self.expenses.append({
            "timestamp": datetime.now().isoformat(),
            "category": category,
            "amount": float(amount),
            "description": description
        })
        self._save()

    def _save(self):
        with open(self.filename, 'w') as f:
            json.dump(self.expenses, f, indent=2)

    def _load(self):
        try:
            with open(self.filename, 'r') as f: return json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            return []

    def total_by_category(self):
        totals = {}
        for exp in self.expenses:
            cat = exp['category']
            totals[cat] = totals.get(cat, 0.0) + exp['amount']
        return totals
```
''',
        'takeaways': 'Capstone projects demonstrate practical problem-solving skills to technical interviewers and hiring managers.',
        'interview': 'How do you design an application for modularity, unit testability, and error resilience?',
    },
    {
        'order': 22,
        'title': 'Chapter 22: Technical Interview Q&A Vault (50+ Questions & Answers)',
        'is_preview': False,
        'read_time_mins': 40,
        'summary': 'High-frequency Python interview questions: memory management, OOP, decorators, concurrency, data structures, and algorithms.',
        'content': '''# Chapter 22: High-Frequency Python Technical Interview Vault

## Top Core Interview Questions & Model Answers

### Q1: What is the difference between `is` and `==` in Python?
**Answer**: `==` checks for **equality of values** (calls `__eq__`), while `is` checks for **identity** (whether two variables reference the exact same memory address in heap, i.e., `id(a) == id(b)`).

### Q2: How does Python manage memory?
**Answer**: Python uses two primary mechanisms:
1. **Reference Counting**: Every object tracks how many references point to it. When the count drops to 0, memory is immediately deallocated.
2. **Cyclic Garbage Collector (Generational GC)**: Detects and cleans up reference cycles across three generations (Gen 0, 1, 2).

### Q3: What is a generator and why is it preferred over a list for large datasets?
**Answer**: A generator is an iterator created using `yield` or generator expressions. It computes items lazily on demand ($O(1)$ memory) instead of loading the entire collection into RAM ($O(N)$ memory).

### Q4: Explain `*args` and `**kwargs`.
**Answer**: `*args` allows a function to accept any number of positional arguments as a `tuple`. `**kwargs` allows accepting arbitrary keyword arguments as a `dict`.

### Q5: What is Monkey Patching in Python?
**Answer**: Dynamically modifying a class or module at runtime without changing the original source code.
''',
        'takeaways': 'Focus on memory mechanics, GIL, OOP design, and time-space complexity when answering technical interviewers.',
        'interview': 'Be prepared to write code on a whiteboard or online IDE during live technical screenings.',
    },
    {
        'order': 23,
        'title': 'Chapter 23: Complete Python Rapid Revision Cheat Sheets',
        'is_preview': False,
        'read_time_mins': 25,
        'summary': 'Concise syntax tables, regex tokens, OOP templates, file modes, socket methods, and time complexity charts.',
        'content': '''# Chapter 23: Python Rapid Revision Cheat Sheet

## 1. Quick Syntax Reference

| Concept | Syntax Example |
| :--- | :--- |
| **List Slicing** | `lst[start:stop:step]` (e.g. `lst[::-1]` reverses list) |
| **Dictionary Get** | `d.get('key', 'default_val')` |
| **Set Operations** | `a | b` (Union), `a & b` (Intersection), `a - b` (Difference) |
| **F-String Formatting**| `f"Price: ₹{price:,.2f}"` -> `Price: ₹1,299.00` |
| **Lambda Function** | `add = lambda x, y: x + y` |
| **Ternary Operator** | `val = "Adult" if age >= 18 else "Minor"` |
| **Unpacking** | `first, *middle, last = [1, 2, 3, 4, 5]` |

## 2. File Modes Cheat Sheet
- `'r'`: Read (Default, error if not found)
- `'w'`: Write (Truncates/overwrites file)
- `'a'`: Append (Writes to end of file)
- `'r+'`: Read + Write
- `'rb'` / `'wb'`: Binary read / write
''',
        'takeaways': 'Keep this chapter bookmarked on your phone or tablet for 10-minute revisions before exams or interviews.',
        'interview': 'Review this cheat sheet before entering your technical interview session.',
    }
]

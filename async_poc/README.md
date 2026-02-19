# POC: Python Async / Await

## Objective
Demonstrate Python's `async` / `await` for concurrent, non-blocking execution.

## Problem / Motivation
Without async, I/O-bound tasks block the program sequentially,
leading to inefficient execution.

## Approach
- `without_async_problem.py` shows blocking sequential tasks
- `basic_async_example.py` shows concurrent execution using async/await

## How to Run
1. Run `without_async_problem.py` to see sequential blocking
2. Run `basic_async_example.py` to see async concurrency

```bash
python without_async_problem.py
python basic_async_example.py

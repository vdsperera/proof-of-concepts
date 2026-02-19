# POC: Python `with` (Context Managers)

## Objective
Demonstrate how Python's `with` statement ensures safe resource management compared to manual handling.

## Problem Statement
Manually managing resources (files, locks, connections) can cause leaks if cleanup code is skipped due to exceptions.

## Demonstration
- `without_with_problem.py` shows the risk
- `basic_with_example.py` shows the safe approach
- `custom_context_manager.py` shows how `with` works internally

## Conclusion
Using `with` guarantees cleanup and improves reliability and readability.

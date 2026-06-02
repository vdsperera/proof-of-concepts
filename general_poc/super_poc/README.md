# Python super() and MRO Behavior POC

## Goal

This POC demonstrates how Python method resolution order (MRO) works and why `super()` is required to build a cooperative inheritance chain.

It compares:
- Direct attribute usage (broken inheritance behavior)
- Cooperative inheritance using `super()` (correct chaining behavior)

---

## Problem Statement

In class inheritance systems, multiple classes may override the same method.

If a subclass does NOT use `super()`, it can unintentionally bypass logic defined in intermediate parent classes.

This leads to:
- Silent skipping of behavior
- Broken mixins or extensions
- Hard-to-debug production issues in frameworks (e.g., Django admin)

---

## Example Scenario

We simulate a Django-like admin system:

- `BaseModelAdmin` → provides base readonly fields
- `ModelAdmin` → adds additional fields
- `SubModelAdmin` → adds final custom fields

We compare two approaches:
1. Broken approach (no super chaining)
2. Fixed approach (cooperative inheritance using super())

---

## Files in this POC

- `broken_example.py` → shows non-cooperative inheritance
- `fixed_example.py` → shows correct super() usage
- `mro_example.py` → shows execution order and MRO behavior

---

## Key Concept: MRO (Method Resolution Order)

Python resolves methods in a linear order using MRO:

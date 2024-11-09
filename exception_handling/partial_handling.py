"""
3. Handling Exceptions at Each Level (Partial Handling)


What It Is:
    Handling certain types of exceptions at intermediate levels,
    performing specific recovery actions, or logging them, but
    letting other exceptions continue to propagate.

How It’s Done:
    Use try-except blocks selectively. Catch only specific exceptions
    that you want to handle at that level, and re-raise others if necessary.

When to Use:
    When you have intermediate steps that can sometimes recover from
    errors (e.g., retrying a network request) but still want to escalate
    certain issues.
"""
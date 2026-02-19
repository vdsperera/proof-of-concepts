"""
Why Functional:
    Immutability: We are not modifying any of the original data;
    instead, we're creating new lists based on transformations.

    Declarative nature: The code expresses what needs to be done:
    filter odd numbers and then square them. The actual "how"
    (iteration and transformation) is handled by the built-in
    filter and map functions.

    Higher-Order Functions: The use of filter and map demonstrates
    functional programming’s power in processing data with higher-order
    functions (functions that take other functions as arguments).

    The functional approach is preferred here because the task
    focuses on data transformations and pure functions. Using
    loops would be less concise and would involve more mutable
    state, making it less elegant in a functional context.

"""

def is_odd(number):
    """_summary_

    Args:
        number (_type_): _description_

    Returns:
        _type_: _description_
    """
    return number % 2 != 0


def square(number):
    """_summary_

    Args:
        number (_type_): _description_

    Returns:
        _type_: _description_
    """
    return number * number


def main():
    """_summary_
    """
    numbers = [2, 4, 6, 7, 9]

    # Using filter and map for functional programming
    odd_numbers = filter(is_odd, numbers)
    squared_odds = map(square, odd_numbers)

    result = list(squared_odds)

    print(result)


if __name__ == "__main__":
    main()

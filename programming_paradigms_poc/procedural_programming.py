"""
Why Procedural:
    Modularity is key here: the program is organized into separate
    functions (calculate_sum and calculate_average) that handle
    specific tasks. This structure makes the code easier to maintain,
    test, and reuse.

    Reusability: Each function is self-contained and can be reused
    with different input data.

    Imperative programming would work here too, but using procedural
    programming allows us to organize the code into logical units
    that can be reused independently.

    Functional programming wouldn't be the best fit for this case,
    as there are no complex transformations or recursive operations
    that demand its strengths.

"""

def calculate_sum(numbers):
    """_summary_

    Args:
        numbers (_type_): _description_

    Returns:
        _type_: _description_
    """
    return sum(numbers)


def calculate_average(numbers):
    """_summary_

    Args:
        numbers (_type_): _description_

    Returns:
        _type_: _description_
    """
    return sum(numbers)/len(numbers)


def main():
    """_summary_
    """
    numbers = [20, 10, 50, 60, 80]
    total = calculate_sum(numbers)
    average = calculate_average(numbers)

    print(f"Total is {total} and average is {average}")


if __name__ == "__main__":
    main()

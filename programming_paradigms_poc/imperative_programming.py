"""
Why Imperative:
    * In this scenario, the task involves directly interacting with the user
    and modifying state (the total) based on input.

    * The imperative approach is appropriate because we explicitly control
    the flow of the program (with loops and conditionals) and change the state
    (total), which fits well with the need for step-by-step instructions.

    * Procedural or functional paradigms would not offer much advantage here,
    as this task is more about modifying the state in response to input rather
    than breaking it into reusable functions or avoiding mutable state.

"""

total = 0

while True:
    input_value = input("Enter a number or 'q' to quit: ")
    if input_value == 'q':
        break
    else:
        try:
            total += int(input_value)
        except Exception as e:
            print("Error: ", e)

print("The total is : ", total)

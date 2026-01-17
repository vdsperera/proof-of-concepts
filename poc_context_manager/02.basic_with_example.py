import os

with open("demo.txt", "w") as file:
    file.write("Hello, World!")
    os._exit(1)  # immediately terminate process, bypassing Python cleanup
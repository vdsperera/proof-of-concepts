import os

file = open("demo.txt", "w")
file.write("Hello, World!")
os._exit(1)  # immediately terminate process, bypassing Python cleanup
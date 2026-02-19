import time

def task(name, seconds):
    print(f"starting task {name}")
    time.sleep(seconds) # blocks the whole program
    print(f"finished task {name}")

def main():
    task("A", 2)
    task("B", 2)

if __name__ == "__main__":
    main()
    # starting task A
    # finished task A
    # starting task B
    # finished task B
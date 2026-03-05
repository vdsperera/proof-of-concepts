import threading
import time

def task(name):
    print(f"Task {name}: Starting")
    time.sleep(2) #simulate I/O wait
    print(f"Task {name}: Finished")

threads = []

for i in range(5):
    t = threading.Thread(target=task, args=(i, ))
    t.start()
    threads.append(t)

for t in threads:
    t.join()

print("Done")
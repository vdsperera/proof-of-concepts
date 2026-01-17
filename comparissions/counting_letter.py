import time
from collections import Counter

s = "abracadabraabracadabraabracadabraabracadabraabracadabraabracadabraabracadabraabracadabraabracadabraabracadabraabracadabraabracadabraabracadabraabracadabraabracadabraabracadabraabracadabra" * 10000  # make string bigger to notice time difference

# --- Method 1: Manual loop ---
start = time.time()
count1 = {}
for char in s:
    if char in count1:
        count1[char] += 1
    else:
        count1[char] = 1
end = time.time()
print("Manual loop:", end-start, "seconds")

# --- Method 2: dict.get shortcut ---
start = time.time()
count2 = {}
for char in s:
    count2[char] = count2.get(char, 0) + 1
end = time.time()
print("dict.get:", end-start, "seconds")

# --- Method 3: Counter ---
start = time.time()
count3 = Counter(s)
end = time.time()
print("Counter:", end-start, "seconds")

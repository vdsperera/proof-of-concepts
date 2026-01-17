import tkinter as tk
import random
import time
from collections import Counter

reactions = ['❤️', '😂', '🔥', '👍', '😮']
stream = [random.choice(reactions) for _ in range(300_0000)]

def fast_summary():
    start = time.time()
    counts = Counter(stream)
    label.config(
        text=f"Counter\nTime: {round(time.time()-start,3)}s"
    )

root = tk.Tk()
root.title("Live Reactions (Counter)")

label = tk.Label(root, text="Click summarize", font=("Arial", 16))
label.pack(pady=10)

tk.Button(root, text="Summarize Reactions", command=fast_summary).pack(pady=10)

root.mainloop()

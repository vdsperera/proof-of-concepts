import tkinter as tk

count = 0

def normal_click():
    global count
    count += 1
    label.config(text=f"Normal Count: {count}")

root = tk.Tk()
root.title("Normal Live Counter")

label = tk.Label(root, text="Normal Count: 0", font=("Arial", 20))
label.pack(pady=10)

tk.Button(root, text="CLICK FAST!", font=("Arial", 18), command=normal_click).pack(pady=20)

root.mainloop()

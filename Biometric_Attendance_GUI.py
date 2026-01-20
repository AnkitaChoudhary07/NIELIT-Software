import tkinter as tk
from tkinter import ttk, messagebox
import os

FILE_NAME = "attendance_data.txt"

candidates = {
    1: {"name": "Mr.Rajeev Aggarwal", "present": 0, "absent": 0},
    2: {"name": "Mr.Sanjeev Suri", "present": 0, "absent": 0},
    3: {"name": "Dr.Pratiyush Guleria", "present": 0, "absent": 0},
    4: {"name": "Ms.Meenakshi Verma", "present": 0, "absent": 0},
    5: {"name": "Mr.Gagandeep Singh", "present": 0, "absent": 0},
    6: {"name": "Mr.Patanjali Pandey", "present": 0, "absent": 0},
    7: {"name": "Mr.Dalip Kumar", "present": 0, "absent": 0},
    8: {"name": "Mr.Rakesh Joshi", "present": 0, "absent": 0},
    9: {"name": "Mr.Amar Thakur", "present": 0, "absent": 0},
}

# ---------------- FILE HANDLING ----------------
def save_data():
    with open(FILE_NAME, "w") as f:
        for cid, d in candidates.items():
            f.write(f"{cid},{d['name']},{d['present']},{d['absent']}\n")

def load_data():
    if os.path.exists(FILE_NAME):
        with open(FILE_NAME, "r") as f:
            for line in f:
                cid, name, p, a = line.strip().split(",")
                candidates[int(cid)] = {
                    "name": name,
                    "present": int(p),
                    "absent": int(a)
                }

# ---------------- LEAVE LOGIC ----------------
def calculate_leaves(absent):
    if absent <= 4:
        return absent, 0
    return 4, absent - 4

# ---------------- TABLE REFRESH ----------------
def refresh_table():
    for row in tree.get_children():
        tree.delete(row)

    for cid, d in candidates.items():
        cl, cr = calculate_leaves(d["absent"])
        tree.insert("", "end", values=(
            cid, d["name"], d["present"], d["absent"], cl, cr
        ))

# ---------------- MARK ATTENDANCE WINDOW ----------------
def mark_attendance():
    win = tk.Toplevel(root)
    win.title("Mark Attendance")
    win.geometry("300x350")

    entries = {}

    for cid, d in candidates.items():
        frame = tk.Frame(win)
        frame.pack(pady=3)

        tk.Label(frame, text=d["name"], width=10).pack(side="left")
        var = tk.StringVar(value="P")
        ttk.Combobox(frame, textvariable=var, values=["P", "A"], width=5).pack(side="left")
        entries[cid] = var

    def submit():
        for cid, var in entries.items():
            if var.get() == "P":
                candidates[cid]["present"] += 1
            else:
                candidates[cid]["absent"] += 1
        save_data()
        refresh_table()
        messagebox.showinfo("Success", "Attendance Saved")
        win.destroy()

    tk.Button(win, text="Submit", command=submit, bg="green", fg="white").pack(pady=10)

# ---------------- MAIN WINDOW ----------------
root = tk.Tk()
root.title("Biometric Attendance System")
root.geometry("650x400")
root.resizable(False, False)

load_data()

title = tk.Label(root, text="Biometric Attendance System", font=("Arial", 16, "bold"))
title.pack(pady=10)

columns = ("ID", "Name", "Working Days", "Leaves", "Casual Leave", "CR Leave")
tree = ttk.Treeview(root, columns=columns, show="headings")

for col in columns:
    tree.heading(col, text=col)
    tree.column(col, width=100, anchor="center")

tree.pack(pady=10)

btn_frame = tk.Frame(root)
btn_frame.pack(pady=10)

tk.Button(btn_frame, text="Mark Attendance", command=mark_attendance,
          bg="#1e90ff", fg="white", width=20).pack(side="left", padx=10)

tk.Button(btn_frame, text="Exit", command=root.quit,
          bg="red", fg="white", width=20).pack(side="left", padx=10)

refresh_table()
root.mainloop()

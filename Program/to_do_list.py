from email.policy import default
import os
import tkinter as tk
from tkinter import messagebox
from tkinter import ttk, filedialog
import sv_ttk


class ListGUI:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("To Do List - github.com/saleemtoure")
        sv_ttk.set_theme("dark")

        self.root.maxsize(370, 500)
        self.root.minsize(370, 500)

        self.label = ttk.Label(self.root, text="TO DO", font=("Arial", 19))
        self.label.pack(padx=10, pady=10)

        self.entrybox = ttk.Entry(self.root, font=("Arial", 16), width=20)
        self.entrybox.bind("<Return>", self.add_objective)
        self.entrybox.pack(padx=10, pady=10)

        self.treeView = ttk.Treeview(self.root, show="tree")
        self.treeView.pack(padx=10, pady=10, fill="both", expand=True)

        self.treeView.bind("<<TreeviewSelect>>", self.delete_objective)

        self.inn_btn = ttk.Button(text="Load list from txt file", command=self.load)
        self.inn_btn.pack()

        self.clear_btn = ttk.Button(text="Clear", command=self.clear)
        self.clear_btn.pack(padx=10, pady=10)

        # Open list from last time - START

        dir_path = os.path.realpath(
            os.path.join(os.getcwd(), os.path.dirname(__file__))
        )
        file_path = os.path.join(dir_path, "my-to-do-list.txt")

        if not os.path.exists(file_path):
            pass
        else:
            with open(file_path, "r") as f:
                for line in f:
                    clean_line = line.strip()
                    if clean_line:
                        self.treeView.insert("", "end", text=clean_line)

        self.autosave()
        # Open list from last time - END

        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)
        self.root.mainloop()

    def add_objective(self, event):
        if self.entrybox.get() != "":
            self.treeView.insert("", "end", text=self.entrybox.get())
            self.entrybox.delete(0, tk.END)

        self.autosave()

    def delete_objective(self, event):
        if self.treeView.selection() == ():
            pass
        else:
            if messagebox.askyesno(
                title="Quit?", message="Do you want to delete this task?"
            ):
                self.treeView.delete(self.treeView.selection()[0])

        self.autosave()

    def autosave(self):
        dir_path = os.path.realpath(
            os.path.join(os.getcwd(), os.path.dirname(__file__))
        )
        file_path = os.path.join(dir_path, "my-to-do-list.txt")

        with open(file_path, "w") as f:
            for task in self.treeView.get_children():
                if task != "":
                    taskText = self.treeView.item(task)["text"]
                    f.write(f"{taskText}\n")

    def load(self):
        file_path = filedialog.askopenfilename(filetypes=[("Text Files", "*.txt")])
        if file_path == "":
            pass
        else:
            f = open(file_path, "r")
            self.clear()
            for line in f:
                self.treeView.insert("", "end", text=line)
            f.close()

    def clear(self):
        for task in self.treeView.get_children():
            self.treeView.delete(task)

        self.autosave()

    def on_closing(self):
        if messagebox.askyesno(title="Quit?", message="Do you really want to quit?"):
            self.root.destroy()


ListGUI()

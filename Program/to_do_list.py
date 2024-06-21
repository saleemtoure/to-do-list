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

        self.out_btn = ttk.Button(text="Save as txt file", command=self.save)
        self.out_btn.pack(pady=2)

        self.inn_btn = ttk.Button(text="Load list from txt file", command=self.load)
        self.inn_btn.pack()

        self.clear_btn = ttk.Button(text="Clear", command=self.reset)
        self.clear_btn.pack(padx=10, pady=10)

        self.saved = False

        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)
        self.root.mainloop()

    def add_objective(self, event):
        self.treeView.insert("", "end", text=self.entrybox.get())
        self.entrybox.delete(0, tk.END)
        self.saved = False

    def delete_objective(self, event):
        if self.treeView.selection() == ():
            pass
        else:
            if messagebox.askyesno(
                title="Quit?", message="Do you want to delete this task?"
            ):
                self.treeView.delete(self.treeView.selection()[0])
        self.saved = False

    def save(self):
        desktop_file_path = os.path.join(os.path.expanduser("~"), "Desktop")

        file_path = filedialog.asksaveasfilename(
            initialfile="my-to-do-list",
            initialdir=desktop_file_path,
            defaultextension=".txt",
            filetypes=[("Text Files", "*.txt")],
        )

        if not file_path:
            pass
        else:
            # print(file_path)
            with open(file_path, "w") as f:
                for task in self.treeView.get_children():
                    f.write(f"{self.treeView.item(task)['text']}\n")

            self.saved = True

    def load(self):
        file_path = filedialog.askopenfilename(filetypes=[("Text Files", "*.txt")])
        if file_path == "":
            pass
        else:
            f = open(file_path, "r")
            self.reset()
            for line in f:
                self.treeView.insert("", "end", text=line)
            f.close()
        self.saved = True

    def reset(self):
        for task in self.treeView.get_children():
            self.treeView.delete(task)
        self.saved = False

    def on_closing(self):
        if messagebox.askyesno(title="Quit?", message="Do you really want to quit?"):
            if len(self.treeView.get_children()) != 0 and self.saved == False:
                self.save()

            self.root.destroy()


ListGUI()

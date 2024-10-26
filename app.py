import tkinter as tk
from tkinter import filedialog, messagebox
import subprocess

class CodeEditor:
    def __init__(self, root):
        self.root = root
        self.root.title("Python Code Editor")
        self.root.geometry("800x600")

        # Code Area
        self.code_area = tk.Text(self.root)
        self.code_area.pack(fill="both", expand=True)

        # Menu Bar
        self.menu_bar = tk.Menu(self.root)
        self.root.config(menu=self.menu_bar)

        # File Menu
        self.file_menu = tk.Menu(self.menu_bar, tearoff=0)
        self.file_menu.add_command(label="New", command=self.new_file)
        self.file_menu.add_command(label="Open", command=self.open_file)
        self.file_menu.add_command(label="Save", command=self.save_file)
        self.file_menu.add_separator()
        self.file_menu.add_command(label="Exit", command=self.root.quit)
        self.menu_bar.add_cascade(label="File", menu=self.file_menu)

        # Run Button
        self.run_button = tk.Button(self.root, text="Run", command=self.run_code)
        self.run_button.pack()

        # Output Area
        self.output_area = tk.Text(self.root)
        self.output_area.pack(fill="x")

    def new_file(self):
        self.code_area.delete(1.0, "end")

    def open_file(self):
        file_path = filedialog.askopenfilename(title="Select Python File")
        if file_path:
            with open(file_path, "r") as file:
                self.code_area.delete(1.0, "end")
                self.code_area.insert("end", file.read())

    def save_file(self):
        file_path = filedialog.asksaveasfilename(title="Save Python File")
        if file_path:
            with open(file_path, "w") as file:
                file.write(self.code_area.get(1.0, "end"))

    def run_code(self):
        code = self.code_area.get(1.0, "end")
        try:
            output = subprocess.check_output(["python", "-c", code], stderr=subprocess.STDOUT)
            self.output_area.delete(1.0, "end")
            self.output_area.insert("end", output.decode())
        except subprocess.CalledProcessError as e:
            self.output_area.delete(1.0, "end")
            self.output_area.insert("end", f"Error: {e.output.decode()}")

if __name__ == "__main__":
    root = tk.Tk()
    code_editor = CodeEditor(root)
    root.mainloop()

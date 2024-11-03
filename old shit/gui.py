import tkinter as tk
from subprocess import Popen

def run_main_script():
    process = Popen(['run_main.bat'], shell=True)

root = tk.Tk()
root.title("GUI for main.py")

run_button = tk.Button(root, text="Run main.py", command=run_main_script)
run_button.pack(pady=20)

root.mainloop()

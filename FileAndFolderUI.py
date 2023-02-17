import tkinter as tk
from tkinter import filedialog
import os
import re

# Function to delete comments from a Java file
def delete_comments(file_path):
    with open(file_path, 'r') as f:
        content = f.read()
    content = re.sub(r'//.*', '', content) # Delete single-line comments
    content = re.sub(r'/\*[\s\S]*?\*/', '', content) # Delete multi-line comments
    with open(file_path, 'w') as f:
        f.write(content)

# Create a tkinter window with two buttons
root = tk.Tk()

def select_file():
    file_path = filedialog.askopenfilename(initialdir=os.getcwd(), title="Select a Java file", filetypes=(("Java files", "*.java"), ("All files", "*.*")), multiple=False)
    if os.path.isfile(file_path):
        delete_comments(file_path)
    elif file_path:
        print("Invalid selection: please select a single .java file.")
    
def select_folder():
    folder_path = filedialog.askdirectory(initialdir=os.getcwd(), title="Select a folder containing Java files")
    if os.path.isdir(folder_path):
        for root, dirs, files in os.walk(folder_path):
            for file in files:
                if file.endswith('.java'):
                    file_path = os.path.join(root, file)
                    delete_comments(file_path)
    elif folder_path:
        print("Invalid selection: please select a folder containing .java files.")
    
file_button = tk.Button(root, text="Select a single Java file", command=select_file)
folder_button = tk.Button(root, text="Select a folder containing Java files", command=select_folder)
file_button.pack()
folder_button.pack()

root.mainloop()

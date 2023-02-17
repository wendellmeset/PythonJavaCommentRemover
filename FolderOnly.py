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

# Open a dialog to select a folder
root = tk.Tk()
root.withdraw()
folder_path = filedialog.askdirectory()

# Traverse the directory and delete comments from all .java files
for root, dirs, files in os.walk(folder_path):
    for file in files:
        if file.endswith('.java'):
            file_path = os.path.join(root, file)
            delete_comments(file_path)

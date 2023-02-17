import tkinter as tk
from tkinter import filedialog
from tkinter import ttk 
import time
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

# Function to show a loading screen
def show_loading_screen():
    loading_window = tk.Toplevel(root)
    loading_window.geometry("400x100")
    loading_window.title("Removing comments...")
    
    progress_label = tk.Label(loading_window, text="0%")
    progress_label.pack(pady=10)
    
    progress_bar = ttk.Progressbar(loading_window, orient=tk.HORIZONTAL, length=300, mode='determinate')
    progress_bar.pack(pady=10)
    
    estimated_time_label = tk.Label(loading_window, text="Estimated time remaining: Calculating...")
    estimated_time_label.pack(pady=10)
    
    return (loading_window, progress_label, progress_bar, estimated_time_label)

# Function to update the loading screen
def update_loading_screen(progress, total, start_time, progress_label, progress_bar, estimated_time_label):
    percentage = int(progress / total * 100)
    progress_label.config(text=str(percentage) + "%")
    progress_bar['value'] = percentage
    
    current_time = time.time()
    elapsed_time = current_time - start_time
    remaining_time = elapsed_time * (total - progress) / progress
    estimated_time_label.config(text="Estimated time remaining: " + str(int(remaining_time)) + " seconds")
    
# Function to hide the loading screen
def hide_loading_screen(loading_window):
    loading_window.withdraw()

# Function to show a success popup
def show_success_popup():
    success_window = tk.Toplevel(root)
    success_window.geometry("300x100")
    success_window.title("Success")
    
    success_label = tk.Label(success_window, text="Finished Removing Your Comments!!")
    success_label.pack(pady=20)
    
    ok_button = tk.Button(success_window, text="OK", command=lambda: success_window.destroy())
    ok_button.pack(pady=10)

# Function to show an error popup
def show_error_popup(error_message):
    error_window = tk.Toplevel(root)
    error_window.geometry("600x400")
    error_window.title("Error")
    
    error_label = tk.Label(error_window, text="An error occurred while removing comments:\n\n" + error_message)
    error_label.pack(pady=20)
    
    def copy_to_clipboard():
        root.clipboard_clear()
        root.clipboard_append(error_message)
    
    copy_button = tk.Button(error_window, text="Copy", command=copy_to_clipboard)
    copy_button.pack(pady=20)
    
    ok_button = tk.Button(error_window, text="OK", command=lambda: error_window.destroy())
    ok_button.pack(pady=20)

# Create a tkinter window with two buttons
root = tk.Tk()

root.geometry("400x150")
root.title("Remove Comments")

def select_file():
    file_path = filedialog.askopenfilename(initialdir=os.getcwd(), title="Select a Java file", filetypes=(("Java files", "*.java"), ("All files", "*.*")), multiple=False)
    if os.path.isfile(file_path):
        # Show loading screen
        loading_window, progress_label, progress_bar, estimated_time_label = show_loading_screen()
        start_time = time.time()
        
        # Delete comments from file
        try:
            delete_comments(file_path)
        except Exception as e:
            # Show error popup and hide loading screen
            hide_loading_screen(loading_window)
            show_error_popup(str(e))
            return
        
        # Hide loading screen and show success popup
        hide_loading_screen(loading_window)
        show_success_popup()

def select_folder():
    folder_path = filedialog.askdirectory(initialdir=os.getcwd(), title="Select a folder")
    if os.path.isdir(folder_path):
        # Show loading screen
        loading_window, progress_label, progress_bar, estimated_time_label = show_loading_screen()
        start_time = time.time()
        
        # Delete comments from all Java files in folder and subdirectories
        total_files = 0
        for root, dirs, files in os.walk(folder_path):
            for file in files:
                if file.endswith(".java"):
                    total_files += 1
        progress = 0
        
        for root, dirs, files in os.walk(folder_path):
            for file in files:
                if file.endswith(".java"):
                    file_path = os.path.join(root, file)
                    try:
                        delete_comments(file_path)
                    except Exception as e:
                        # Show error popup and hide loading screen
                        hide_loading_screen(loading_window)
                        show_error_popup(str(e))
                        return
                    progress += 1
                    update_loading_screen(progress, total_files, start_time, progress_label, progress_bar, estimated_time_label)
        
        # Hide loading screen and show success popup
        hide_loading_screen(loading_window)
        show_success_popup()

select_file_button = tk.Button(root, text="Select Java File", command=select_file)
select_file_button.pack(pady=10)

select_folder_button = tk.Button(root, text="Select Folder", command=select_folder)
select_folder_button.pack(pady=10)

root.mainloop()

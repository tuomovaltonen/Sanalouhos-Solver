import tkinter as tk
from tkinter import  filedialog, messagebox
from solve_gui import open_grid_window
from utilities import read_from_file
from play_gui import open_play_window
from solvers import get_random_grid, solve
import random

def go_back_to_start(window):
    window.destroy()
    open_start_window()

# The starting window
def open_start_window():
    global start_window
    start_window = tk.Tk()
    start_window.title("Sanalouhos")
    start_window.geometry("300x200")

    # Add a Start button to open the grid window
    start_button = tk.Button(start_window, text="Create or Solve", font=("Arial", 16), command=lambda: open_settings_window(False))
    start_button.pack(expand=True)

    # Add a Start button to open the grid window
    play_button = tk.Button(start_window, text="Play from file", font=("Arial", 16), command=open_read_file_window)
    play_button.pack(expand=True)

    # Add a Start button to open the grid window
    playran_button = tk.Button(start_window, text="Play Random", font=("Arial", 16),command=lambda: open_settings_window(True))
    playran_button.pack(expand=True)

    start_window.mainloop()

# Window for file submitting
def open_read_file_window():
    # Destroy the start window
    start_window.destroy()

    # Create the new window
    read_file_window = tk.Tk()
    read_file_window.title("Read File")

    # Text input field for file path
    file_path_var = tk.StringVar()
    file_entry = tk.Entry(read_file_window, textvariable=file_path_var, width=50)
    file_entry.pack(pady=10)

    # File selection button
    def browse_file():
        file_path = filedialog.askopenfilename()
        file_path_var.set(file_path)

    browse_button = tk.Button(read_file_window, text="Browse", command=browse_file)
    browse_button.pack(pady=5)

    # Submit button callback
    def submit_file():
        file_path = file_path_var.get()
        if not file_path:
            messagebox.showwarning("Warning", "Please enter or select a file.")
            return

        try:
            # Use parse_file function to read file content
            solution, letters, language = read_from_file(file_path)
            try:
                solutions = solve(letters,language, 1)
                if len(solutions) == 0:
                    raise ValueError("Seems like the file is unsolvable.\n Better to not even try :)")
                # Open the play window with parsed content
                open_play_window(language, letters,read_file_window, False, solution)
            except ValueError as e:
                messagebox.showerror("no solutions", str(e))
        except Exception as e:
            messagebox.showerror("Error", f"Failed to open the file: {str(e)}")

    # Submit and Back buttons
    submit_button = tk.Button(read_file_window, text="Submit", command=submit_file)
    submit_button.pack(pady=5)

    back_button = tk.Button(read_file_window, text="Back", command=lambda: go_back_to_start(read_file_window))
    back_button.pack(pady=5)

    read_file_window.mainloop()


def open_settings_window(is_rand_play):
    # Close start window
    start_window.destroy()
    # Create the settings window
    global settings 
    settings = tk.Tk()
    settings.title("Custom your Sanalouhos")
    settings.geometry("300x300")
    settings.minsize(50, 50)
 

    # Label and Entry for Number 1
    label1 = tk.Label(settings, text="Number of columns (2-10):")
    label1.pack()

    num1 = tk.Entry(settings)
    num1.pack()
    num1.insert(0, "5")

    # Label and Entry for Number 2
    label2 = tk.Label(settings, text="Number of rows (2-10):")
    label2.pack()

    num2 = tk.Entry(settings)
    num2.pack()
    num2.insert(0, "6")

    # Language selection with radio buttons
    language_var = tk.StringVar(value="finnish")
    radio_finnish = tk.Radiobutton(settings, text="Finnish", variable=language_var, value="finnish")
    radio_finnish.pack()
    radio_english = tk.Radiobutton(settings, text="English", variable=language_var, value="english")
    radio_english.pack()

    
    if(is_rand_play):
        # Label and Entry for Number 1
        label3 = tk.Label(settings, text="Set seed:")
        label3.pack()
        global num3
        num3 = tk.Entry(settings)
        num3.pack()
        seed = random.randint(0,10384018375134)
        num3.insert(0, str(seed))


    # Submit button
    submit_button = tk.Button(settings, text="Submit", command= lambda: settings_submit_action(language_var, num1, num2, is_rand_play))
    submit_button.pack()

    settings.mainloop()

def settings_submit_action(language_var, num1, num2, is_rand_play):
    try:
        # Retrieve and validate entries
        cols = int(num1.get())
        rows = int(num2.get())
        
        if not (2 <= cols <= 10) or not (2 <= rows <= 10):
            raise ValueError("Both numbers must be between 3 and 20.")

        # Get the selected language
        selected_language = language_var.get()
        
        # Open next window
        if is_rand_play:
            global num3
            letters = get_random_grid(selected_language, cols, rows, int(num3.get()))
            open_play_window(selected_language, letters, settings, False)
        else:
            open_grid_window(settings, rows, cols, selected_language)
    except ValueError as e:
        messagebox.showerror("Input Error", str(e))

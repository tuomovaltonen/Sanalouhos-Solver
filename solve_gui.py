import tkinter as tk
import time
from tkinter import  filedialog, messagebox
from solvers import solve, get_words_from_coordinates
from utilities import color_scale, sort_solutions

def check_is_solvable_on_save(letters, language, window):
    solution = solve(letters, language,1)
    if len(solution) == 0:
        messagebox.showerror("No solutions found", "No solutions found")
        return
    else:
        from play_gui import open_play_window
        open_play_window(language, letters, window, True )

        
def open_grid_window( previous_window, rows, cols,language, letters=None):
    global solutions, words

    previous_window.destroy()
    # initialize grid entries
    global grid_entries
    grid_entries = []
    # Close the settings window
    

    # Create the main grid window
    global root
    root = tk.Tk()
    root.title("Write your Sanalouhos!")
    root.geometry("600x600")
    root.minsize(300, 300)

    create_grid(root, rows, cols, letters)

    
    # Add a Back button to return to the start window
    from start_and_set_gui import go_back_to_start
    back_button = tk.Button(root, text="Back to start", font=("Arial", 14), command= lambda: go_back_to_start(root))
    back_button.grid(row=rows, column=0, columnspan=cols//2, pady=10, sticky="nsew")

    # Add a Save button to write the grid entries to a file
    save_button = tk.Button(root, text="Save to file", font=("Arial", 14), command= lambda: check_is_solvable_on_save(find_grid_letters(), language, root))
    save_button.grid(row=rows, column=cols//2, columnspan=cols - cols//2, pady=10, sticky="nsew")

    solve_button = tk.Button(root, text="Solve", font=("Arial", 14), command= lambda: open_solution_window(True,False, root, find_grid_letters(), rows, cols,language,1))
    solve_button.grid(row=rows + 1, column=0, columnspan=cols, pady=10, sticky="nsew")

    # Start the Tkinter event loop for the grid window
    root.mainloop()

def find_grid_letters():
    letters = []
    for row in grid_entries:
        row_letters = []
        for entry in row:
            row_letters.append(entry.get())
        letters.append(row_letters)
    return letters

def save_grid_to_file(solution, language):
    global grid_entries
    data = []
    for row in grid_entries:
        row_data = [entry.get() for entry in row]
        data.append(row_data)

    # Write the data to a file
    with open("grid_entries.txt", "w") as file:
        for row_data in data:
            file.write(",".join(row_data) + "\n")

    print("Grid entries saved to grid_entries.txt")

def move_focus(direction, current_row, current_col, rows, cols):
    """Move focus based on the specified direction"""
    if direction == "right" and current_col < cols - 1:
        grid_entries[current_row][current_col + 1].focus_set()
    elif direction == "left" and current_col > 0:
        grid_entries[current_row][current_col - 1].focus_set()
    elif direction == "up" and current_row > 0:
        grid_entries[current_row - 1][current_col].focus_set()
    elif direction == "down" and current_row < rows - 1:
        grid_entries[current_row + 1][current_col].focus_set()

def on_key_press(event, row, col, rows, cols):

    """Handle character input and auto-move to the next square"""
    if event.keysym in ["Left", "Right", "Up", "Down"]:
        # Move based on arrow keys
        directions = {"Left": "left", "Right": "right", "Up": "up", "Down": "down"}
        move_focus(directions[event.keysym], row, col, rows, cols)
        return "break"  # Prevent further handling of the key press
    elif event.keysym == "BackSpace":
        # Move to the previous square and clear it
        grid_entries[row][col].delete(0, tk.END)  # Clear current cell
        if col > 0 or row > 0:  # Ensure there is a previous cell to move to
            prev_col = col - 1 if col > 0 else cols - 1
            prev_row = row if col > 0 else row - 1
            grid_entries[prev_row][prev_col].focus_set()
            grid_entries[prev_row][prev_col].delete(0, tk.END)
        return "break"
    elif len(event.char) == 1 and event.char.isalpha():
        # Input a letter and move to the next square
        grid_entries[row][col].delete(0, tk.END)  # Clear current cell
        grid_entries[row][col].insert(0, event.char.upper())  # Insert uppercase letter
        if col < cols - 1:
            grid_entries[row][col + 1].focus_set()
        elif row < rows - 1:
            grid_entries[row + 1][0].focus_set()
        return "break"

def create_grid(window, rows, cols, letters=None):
    global grid_entries
    grid_entries = []  # Reset grid entries list if recreating the grid

    for i in range(rows):
        row_entries = []
        for j in range(cols):
            entry = tk.Entry(window, font=("Arial", 30), justify="center", borderwidth=1, relief="solid")
            entry.grid(row=i, column=j, padx=2, pady=2, sticky="nsew")
            entry.bind("<Key>", lambda e, r=i, c=j: on_key_press(e, r, c, rows, cols))  # Bind key event with row and col
            
            # Initialize the entry with the corresponding letter if letters array is provided
            if letters and i < len(letters) and j < len(letters[i]):
                entry.insert(0, letters[i][j])

            row_entries.append(entry)
        grid_entries.append(row_entries)

    # Configure grid to make rows and columns resizable
    for i in range(rows):
        window.grid_rowconfigure(i, weight=1)  # Make row expandable
    for j in range(cols):
        window.grid_columnconfigure(j, weight=1)  # Make column expandable

def open_solution_window(is_create_mode,is_save_solution, previous_window, letters,rows,cols,language, num_sol,intented_solution = None, time_string = None):
    #Find Solution
    global solutions
    if num_sol == 1 and intented_solution != None:
        solutions = [intented_solution]
    else:
        # Normilize the count
        # A bit clumsy but works
        if num_sol != -1 and intented_solution != None:
            num_sol -= 1
        solutions = solve(letters,language, num_sol)
        solutions = sort_solutions(solutions)
        
        if intented_solution != None :
            solutions.insert(0, intented_solution)
        # Add intented solution as first if it is available
        # The program depicts one solution two much in the solutions

    try:
        if len(solutions) == 0:
            raise ValueError("No solutions found!")
        
         #sort solution
        
        global words
        words = get_words_from_coordinates(solutions, letters)
        # Destroy previous window
        previous_window.destroy()

       
        global number_of_solutions
        number_of_solutions = len(solutions)

        global solutions_index
        solutions_index = 0

        #create a solution window
        global solution_window
        solution_window = tk.Tk()
        if(time_string != None):
            solution_window.title(time_string)
        else:
            solution_window.title("Solutions")

        solution_window.geometry("600x600")

        display_solution_grid(solution_window, letters,rows,cols)

        #highlight the first solutions
        highlight_solution(solutions[0])
        
        # Add a Back button to return to the start window
        left_button = tk.Button(solution_window, text="Previous", font=("Arial", 14), command=lambda: show_previous_solution(cols))
        left_button.grid(row=rows, column=0, pady=10, sticky="nsew")

        # Add a counter label to display the current index and total solutions
        global counter_label
        counter_label = tk.Label(solution_window, text=f"{solutions_index + 1 } / {number_of_solutions}", font=("Arial", 14))
        counter_label.grid(row=rows, column= cols // 2, pady=10, sticky="nsew")

        # Add a Next button to proceed to the next solution
        right_button = tk.Button(solution_window, text="Next", font=("Arial", 14), command=lambda: show_next_solution(cols))
        right_button.grid(row=rows, column= cols - 1, pady=10, sticky="nsew")

        if is_create_mode and not is_save_solution:
            back_button = tk.Button(solution_window, text="Back", font=("Arial", 14), command=lambda: open_grid_window(solution_window, rows, cols, language, letters))
            back_button.grid(row=rows + 1, column=0, columnspan=cols, pady=10, sticky="nsew")
        elif not is_create_mode and not is_save_solution: 
            from start_and_set_gui import go_back_to_start
            back_button = tk.Button(solution_window, text="Back to start", font=("Arial", 14), command=lambda: go_back_to_start(solution_window))
            back_button.grid(row=rows + 1, column=0, columnspan=cols, pady=10, sticky="nsew")
        else: # Save solution mode
            back_button = tk.Button(solution_window, text="Back", font=("Arial", 14), command=lambda: open_grid_window(solution_window, rows, cols, language, letters))
            back_button.grid(row=rows + 1, column=0, pady=10, sticky="nsew")

            save_button = tk.Button(solution_window, text="Save to file", font=("Arial", 14), command=lambda: save_grid_to_file(solutions[solutions_index], language))
            save_button.grid(row=rows + 1, column= cols - 1, pady=10, sticky="nsew")


         # Create and place the entry field
        entry = tk.Entry(solution_window, width=5)
        entry.grid(row=rows + 2, column=1, pady=10)

        # more solutions function
        # Create and place the "More Solutions" button
        btn_more_solutions = tk.Button(solution_window, text="More Solutions", command= lambda: on_more_solutions_click(is_create_mode,is_save_solution,solution_window, letters,rows,cols,language,entry,intented_solution, time_string))
        btn_more_solutions.grid(row=rows + 2, column=0, pady=10)

       

        # Create and place the label
        label = tk.Label(solution_window, text= "(-1 for all)")
        label.grid(row=rows + 2, column=2, pady=10)

         # Display words
        global word_labels
        word_labels = []
        display_words(solution_window, words[solutions_index], cols)

        solution_window.mainloop()

    except ValueError as e:
        messagebox.showerror("No solutions found", str(e))

def on_more_solutions_click(is_create_mode,is_save_solution, previous_window, letters,rows,cols,language,entry,intented_solution, time_string):
    try:
        value = int(entry.get())
        if value < -1:
            raise ValueError("Value must be -1 or greater.")
        open_solution_window(is_create_mode,is_save_solution, previous_window, letters,rows,cols,language, value, intented_solution, time_string)  # Call the foo function with the input value
    except ValueError:
        messagebox.showerror("Invalid Input", "Input a maximum number of solutions to be found (-1 for all)")

def update_counter():
    counter_label.config(text=f"{solutions_index + 1} / {number_of_solutions}")

def highlight_solution(pair_arrays):
     # Reset all label backgrounds first
    for row in grid_labels:
        for label in row:
            label.config(bg=label.master.cget("bg")) 
    count = 0
    for a in pair_arrays:
        # Highlight the cells specified in the coordinate pairs
        for x, y in a:
            grid_labels[x][y].config(bg=color_scale(count))  # Choose a color like yellow for highlighting
        count = count + 1

def show_previous_solution(cols):
    global solutions_index
    if solutions_index > 0:
        solutions_index -= 1
        highlight_solution(solutions[solutions_index])
    update_counter()
    display_words(solution_window, words[solutions_index],cols)

def show_next_solution(cols):
    global solutions_index
    if solutions_index < len(solutions) - 1:
        solutions_index += 1
        highlight_solution(solutions[solutions_index])
    update_counter()
    display_words(solution_window, words[solutions_index],cols)

def display_words(window, words_list, cols):
    global word_labels
    # Clear any existing labels
    for label in word_labels:
        label.destroy()
    
    # Add new labels for each word
    word_labels = []
    for i, word in enumerate(words_list):
        color = color_scale(i)
        label = tk.Label(window, text=word, font=("Arial", 14), fg=color)
        label.grid(row=i, column=cols + 1, padx=10, pady=5, sticky="w")
        word_labels.append(label)

def display_solution_grid(window, letters, rows, cols):
    global grid_labels
    grid_labels = []  # Clear any existing labels

    for i in range(rows):
        row_labels = []
        for j in range(cols):
            label = tk.Label(window, text=letters[i][j], font=("Arial", 30), borderwidth=1,justify="center",relief="solid", width=2, height=1, fg="black")
            label.grid(row=i, column=j, padx=2, pady=2, sticky="nsew")
            row_labels.append(label)
        grid_labels.append(row_labels)

    # Make grid resizable
    for i in range(rows):
        window.grid_rowconfigure(i, weight=1)
    for j in range(cols):
        window.grid_columnconfigure(j, weight=1, uniform="col")

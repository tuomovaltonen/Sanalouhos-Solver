import tkinter as tk
from tkinter import  filedialog, messagebox
from solve_gui import open_solution_window, open_grid_window
from utilities import color_scale, write_to_file, find_path
from solvers import is_valid_word, get_all_words
import time
import random

def update_timer():
    global elapsed_time, close_timer
    # Format elapsed time as HH:MM:SS
    time_str = time.strftime("%H:%M:%S", time.gmtime(elapsed_time))
    timer_label.config(text=time_str)
    elapsed_time += 1
    play_window.after(1000, update_timer)  # Update every 1 second

def open_play_window(language, letters1, previous_window, choose_solution, intented_solution = None):
    all_words_set = set(get_all_words(language))
    previous_window.destroy()  # Close the current window
    global letters
    letters = letters1
    global play_window, word_label, timer_label
    play_window = tk.Tk()
    if not choose_solution:
        play_window.title("Play Window")
    else:
        play_window.title("Choose your solution")

    play_window.geometry("600x600")

    rows = len(letters)
    cols = len(letters[0])

    if(choose_solution):
        messagebox.showinfo("Notification", "Choose the solution you intented\n It will be presented first when the game is solved")
        

    # Initialize the global time variable
    if(not choose_solution):
        global elapsed_time
        elapsed_time = 0
        
        # Timer label
        timer_label = tk.Label(play_window, text="00:00:00", font=("Arial", 16))
        timer_label.grid(row=0, column=cols-1, columnspan=cols, pady=5)

        # Start updating the timer
        update_timer()

    


    #variables
    global word_index, color_index
    word_index = 0  # Tracks the color to use for the current word
    color_index = 0
    global selected_cells
    selected_cells = [[]]

    # Word display label
    word_label = tk.Label(play_window, text="", font=("Arial", 20))
    word_label.grid(row=0, column=0, columnspan=len(letters[0]), pady=10)

    # Create the grid of cells
    for i in range(rows):
        for j in range(cols):
            label = tk.Label(play_window, text=letters[i][j], font=("Arial", 30), borderwidth=1,justify="center",relief="solid", width=2, height=1, fg="white")
            label.grid(row=i+1, column=j, padx=2, pady=2, sticky="nsew")
            label.bind("<Button-1>", lambda e, r=i+1, c=j+1: cell_clicked(e, r, c))

    # Make grid resizable
    for i in range(rows+1):
        play_window.grid_rowconfigure(i, weight=1)
    for j in range(cols):
        play_window.grid_columnconfigure(j, weight=1)

    # "Connect" button to validate word
    connect_button = tk.Button(play_window, text="Connect", font=("Arial", 14), command=lambda: validate_word(rows,cols, all_words_set, language,choose_solution, intented_solution))
    connect_button.grid(row=rows + 2, column=0, columnspan=cols, pady=10)

    if not choose_solution:
        give_up_button = tk.Button(play_window, text="Give up", font=("Arial", 14), command=lambda: give_up(letters, rows, cols ,language, intented_solution))
        give_up_button.grid(row=rows + 4, column=cols - 1, pady=10, sticky="e")


    #back to grid if choose solution
    if choose_solution:
        back_button = tk.Button(play_window, text="Back", font=("Arial", 14), command=lambda: open_grid_window(play_window, rows, cols, language, letters))
        back_button.grid(row=rows + 4, column=0, pady=10)
    
    
    play_window.mainloop()

# Function to handle the "Give Up" button
def give_up(letters, rows, cols, language, intented_solution):
    # Ask the user if they are sure
    result = messagebox.askyesno("Confirmation", "Are you sure you want to give up?")
    if result:
        open_solution_window(False, False, play_window, letters, rows, cols, language,1, intented_solution, "You gave UP!!!")

def successor_cell(previous_cell, current_cell):
    x1, y1 = previous_cell
    x2, y2 = current_cell
    # Check if the current cell is one of the 8 possible neighbors
    return abs(x1 - x2) <= 1 and abs(y1 - y2) <= 1 and (x1, y1) != (x2, y2)

def cell_clicked(event, row, col):
    global word_index, color_index

    # Adjust the indices since grid indices start from 1 in display but 0 in list
    row -= 1
    col -= 1

    # If immidietly previous cell unmark it
    if len(selected_cells[word_index]) > 0 and (row, col) == selected_cells[word_index][-1]:
        reset_one_cell(row,col)
        del selected_cells[word_index][-1]
        update_word_display()
        return

    # Ignore if already in the current word
    if (row, col) in selected_cells[word_index]:
        return

    # Reset cells if previous word
    for i in range(word_index):
        if (row, col) in selected_cells[i]:
            reset_cells(i)
            del selected_cells[i]
            word_index -= 1
            return
        
     # Ignore if already 10 selected
    if len(selected_cells[word_index]) >= 10:
        return
    
    #ignore if not immidiate successor
    if len(selected_cells[word_index]) > 0 and not successor_cell(selected_cells[word_index][-1], (row,col)):
        return
    

    # Color the cell with current color
    cell = event.widget
    cell.config(bg=color_scale(color_index))
    cell.config(fg="black")

    # Add letter to word display and track cell
    selected_cells[word_index].append((row, col))
    update_word_display()

def update_word_display():
    # Check if there are any selected cells for the current word_index
    if word_index < len(selected_cells) and selected_cells[word_index]:
        word = ''.join(letters[row][col] for row, col in selected_cells[word_index])
    else:
        word = ""  # If no selected cells, display empty string
    word_label.config(text=word)

def reset_one_cell(i,j):
    cell = play_window.grid_slaves(row=i+1, column=j)[0]
    cell.config(bg=cell.master.cget("bg"))
    cell.config(fg="white")

def reset_cells(index):
    global word_index
    # Reset all cells in back to their original color
    for (row, col) in selected_cells[index]:
        # Adjust indices to match grid display rows and columns
        cell = play_window.grid_slaves(row=row+1, column=col)[0]
        cell.config(bg=cell.master.cget("bg"))
        cell.config(fg="white")
    
def validate_word(rows, cols, all_words_set, language, is_choose_solution, intented_solution):
    global word_index, color_index

    while len(selected_cells) <= word_index:
        selected_cells.append([])

    # Get the current word
    word = ''.join(letters[row][col].lower() for row, col in selected_cells[word_index])

    if is_valid_word(word, all_words_set):
        # Move to the next color for the new word
        word_index += 1
        color_index = (color_index + 1)

        selected_cells.append([])
        update_word_display()  # Clear word display for next word
        #check if all letters are validated
        if len([item for sublist in selected_cells for item in sublist]) == rows*cols:
            if(is_choose_solution):
                path = find_path()
                random_key = random.randint(1, 100) 
                write_to_file(path, language,letters,random_key, selected_cells)
                messagebox.showinfo("Notification", "File saved in: " + path)
                from start_and_set_gui import go_back_to_start
                go_back_to_start(play_window)
            else:
                time_string = time.strftime("%H:%M:%S", time.gmtime(elapsed_time))
                messagebox.showinfo("Congrats!","YEAH! You did it!\nYour time was: " + time_string + "\nPress Ok to continue loading the solutions")
                open_solution_window(False, False, play_window, letters, rows, cols, language,1, intented_solution, time_string )
    else:
        # Reset if condition is not met
        reset_cells(word_index)
        selected_cells[word_index] = []
        update_word_display()
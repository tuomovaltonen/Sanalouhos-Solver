# Sanalouhos-Solver
Solver, random game constructor and ability to write your own Sanalouhos with graphical user interface. Sanalouhos is a word game created by Helsingin Sanomat. Works also for Strands by New York times.

## Installation
Tkinter is needed for the gui. It is often already installed with python. More information in https://docs.python.org/3/library/tkinter.html.

## Usage

Running the script main.py will start the program. After that the GUI is quite self explanatory. 

The games created can be saved in .txt files. By default they are saved in the "Louhokset" folder. There is one example game provided in the folder.

It is not difficult to construct a Sanalouhos with so many solution that it will be difficult to handle for the program if all solutions are requested. Hence be a bit carefull when solving for all solutions. The solver is generally fast for finding all solutions. For example, there should be no such problems in the random games.

For random games, users can provide a custom seed. This ensures that the same game is generated every time, which is particularly useful for competitive play with friends.

## Structure

The files that has "gui" in their name contains the code for the gui. The solver funtions are in "solvers.py" file and can be utilized without the gui as well. ChatGPT has been used for writing parts of the program. 

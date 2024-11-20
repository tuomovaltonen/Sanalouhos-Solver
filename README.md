# Sanalouhos-Solver
Solver, random game constructor and ability to write your own Sanalouhos with graphical user interface. Sanalouhos is a word game created by Helsingin Sanomat. Works also for Strands by New York times.

# Notes
It seems that some windows systems the default window backround is white making the letters difficult to spot whe playing. This can be changed by switching all the fg="white" to fg="black".

## Installation
Tkinter is needed for the gui. Numpy for random number generation. It is often already installed with python. More information in https://docs.python.org/3/library/tkinter.html.

## Usage

Running the script main.py will start the program. After that the GUI is quite self explanatory. 

The games created can be saved in .txt files. By default, they are saved in the "Louhokset" folder. There is one example game provided in the folder.

For random games, users can provide a custom seed. This ensures that the same game is generated every time, which is particularly useful for competitive play with friends. Generating a large random game can take few seconds.

The random games are always solvable and the program does not allow to upload or download a game without a working solution. The solutions are XOR decrypted in the game files so that they are not immidietly seen if the file is opened.

## Dictionaries

The applicable words has to be of length between 3 and 10. (This can be changed, if wanted, by altering the parameters when reading a file, cell_click action in the game and the maximum length filtering in the cover_the_grid function.)

The dictionary for Finnish is from https://www.kotus.fi/aineistot/sana-aineistot/nykysuomen_sanalista and it seems include more words that the one used by HS. The dictionary for English is from https://github.com/dwyl/english-words.


## Solver 

The solver is based on simple recursive depth-first-search.

The files that has "gui" in their name contains the code for the gui. The solver funtions are in "solvers.py" file and can be utilized without the gui as well. ChatGPT has been used for writing parts of the program. 

In random games and when reading from the file the solver presents the first solution to be the one that is availeble from the construction and does not call the solver method. Only if more than 1 solutions is requested solver is called. The solution available in the construction can appear twice since the solver also finds it. Be a bit carefull when solving for all solutions in large grids. The solver is generally fast for finding all solutions. For example, there should be no such problems in the random games with default size.

The solver considers the words to be different only if there exist a coordinate where they differ. For example, if there is a word "ovi" the solver consider the word to be the same as "voi" they share each coordinate. On the other hand, solutions are considered to be different even if they consist of the same words but chosen on different coordinates.

The solutions are presented in an order where the first solution is the one availeble by construction if it exist and the other solutions sorted so that the solutions with longest words are presented first.
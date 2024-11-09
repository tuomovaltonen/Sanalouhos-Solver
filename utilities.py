import os
import tkinter as tk

pastel_colors = [
    "#FFB6C1",  # Light Pink
    "#FFDAB9",  # Peach Puff
    "#FFFFE0",  # Light Yellow
    "#98FB98",  # Pale Green
    "#E0FFFF",  # Light Cyan
    "#E6E6FA",  # Lavender
    "#FFE4E1",  # Misty Rose
    "#87CEFA",  # Light Sky Blue
    "#D8BFD8",  # Thistle
    "#F0FFF0",  # Honeydew
    "#FFFACD",  # Lemon Chiffon
    "#F5FFFA",  # Mint Cream
    "#F0F8FF",  # Alice Blue
    "#FFF5EE",  # Seashell
    "#FFF8DC"   # Cornsilk
]

def color_scale(i):
    return pastel_colors[i % len(pastel_colors)]


def write_to_file(file_path, language, letters, key, solution):
    # Format the language and letters array
    language_text = language
    letters_text = "\n".join(",".join(row) for row in letters)
    key_text = str(key)

    # Format the solution as nested arrays of pairs: e.g., [[(a,b), (c,d)], [(e,f)]]
    # Each array is separated by a blank line
    solution_text = "\n\n".join(
        "\n".join(f"{a},{b}" for a, b in sublist) for sublist in solution
    )
    
    # XOR encrypt the solution
    solution_bytes = solution_text.encode()
    xor_key = int(key)  # Convert key to an integer for XOR operation
    encrypted_bytes = bytes([b ^ xor_key for b in solution_bytes])
    
    # Combine all parts and write to file
    with open(file_path, "wb") as file:
        file.write((language_text + "\n").encode())
        file.write((letters_text + "\n").encode())
        file.write((key_text + "\n").encode())
        file.write(encrypted_bytes)  # Write encrypted solution as bytes

def read_from_file(file_path):
    with open(file_path, "rb") as file:
        lines = file.read().splitlines()
        
    # Parse language from the first line
    language = lines[0].decode()

    # Parse letters until the key line is found
    letters = []
    key_line_index = None
    for i, line in enumerate(lines[1:], start=1):
        try:
            int(line.decode())  # If this line is the key, it should convert to an integer
            key_line_index = i
            break
        except ValueError:
            # If not an integer, treat it as part of the letters grid
            letters.append(line.decode().split(","))

    if key_line_index is None:
        raise ValueError("Invalid file format: No key found in the file.")
    
    # Parse the key
    key = int(lines[key_line_index].decode())

    # Decrypt the solution
    encrypted_solution = b"\n".join(lines[key_line_index + 1:])  # Join remaining lines as bytes
    decrypted_bytes = bytes([b ^ key for b in encrypted_solution])
    decrypted_solution_text = decrypted_bytes.decode()

    # Parse solution back to array of arrays of pairs of integers
    try:
        # Split by double newlines to separate sub-arrays, then parse each line within
        solution = [
            [list(map(int, pair.split(","))) for pair in sublist.splitlines()]
            for sublist in decrypted_solution_text.split("\n\n")
        ]
    except ValueError:
        raise ValueError("Invalid file format: Decrypted solution format is incorrect.")
    

    from solvers import is_solution
    if not is_solution(solution, letters, language):
        raise ValueError("Solution does not seem to solve the Louhos")
    
    return solution, letters, language

def find_path():
    # Ensure the directory exists
    directory = "Louhokset"
    os.makedirs(directory, exist_ok=True)
    
    # Iterate to find the smallest integer i for which the file does not exist
    i = 1
    while True:
        file_path = os.path.join(directory, f"Sanalouhos{i}.txt")
        if not os.path.exists(file_path):
            return file_path
        i += 1

def sort_solutions(solutions):
    # Sort solutions based on the lengths of arrays within each element
    solutions.sort(key=lambda x: sorted([len(arr) for arr in x], reverse=True), reverse=True)
    return solutions





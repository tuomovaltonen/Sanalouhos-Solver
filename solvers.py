import random

def load_words_from_file(filename, max_length):
    with open(filename, 'r') as file:
        words = [line.strip() for line in file if len(line.strip()) >= 3 and len(line.strip()) <= max_length]
    return words


def find_words_from_index(letters, si, sj, all_words):
    # Define answers list to hold all found word coordinate paths
    answers = []
    
    rows = len(letters)
    cols = len(letters[0])
    # Convert all_words to a set for quick lookup
    all_words_set = set(all_words)
    
    # Helper function for DFS
    def dfs(i, j, path, current_word, current_word_list):
        # Add the current coordinate to path
        path.append((i, j))
        # Add the current letter to the current word
        current_word += letters[i][j]
        
        # Filter current_word_list to only words that start with current_word
        current_word_list = [word for word in current_word_list if word.startswith(current_word)]
        
        # If current_word is a complete word, add the current path to answers
        if current_word in all_words_set:
            answers.append(list(path))  # Copy path to avoid mutation later
        
        # If current_word_list is empty or no successors, backtrack
        if not current_word_list:
            path.pop()
            return
        
        # Explore successors
        for ni, nj in successors(i, j, rows, cols):
            # Recurse
            if (ni, nj) not in path:
                dfs(ni, nj, path, current_word, current_word_list)
        
        # Backtrack by removing the last added coordinate
        path.pop()
    
    # Start DFS from the initial coordinate (si, sj)
    dfs(si, sj, [], "", all_words)
    
    return answers

def filter_unique_sets(array_of_pairs):
    unique_sets = []
    seen_sets = set()
    
    for pairs in array_of_pairs:
        # Convert each list of pairs to a frozenset of tuples for comparison
        set_of_pairs = frozenset(map(tuple, pairs))
        
        # Add only if the frozenset is not in seen_sets
        if set_of_pairs not in seen_sets:
            unique_sets.append(pairs)
            seen_sets.add(set_of_pairs)
    
    return unique_sets

def get_words_from_coordinates(answers, letters):
    words = []
    for solution in answers:
        sol_words = []
        for path in solution:
            # Reconstruct the word using the coordinates in the path
            word = ''.join(letters[i][j] for i, j in path)
            sol_words.append(word)
        words.append(sol_words)
    return words

def is_solution(solution, letters, language):
    all_words = get_all_words(language)
    rows = len(letters)
    cols = len(letters[0])
    total_length = sum(len(inner_list) for inner_list in solution)
    if(total_length != rows*cols):
        return False
    for path in solution:
        if (len(path) > 0):
            # Reconstruct the word using the coordinates in the path
            word = ''.join(letters[i][j] for i, j in path)
            if not is_valid_word(word, all_words):
                return False
    return True
    

def cover_the_grid(chains, rows, cols, number_of_answer):
    covered_cells = [[False for _ in range(cols)] for _ in range(rows)]
    answers = []
    global current_num
    current_num = 0

    def dfs(covered_cells, current_chains, suitable_chains):
        global current_num
        if number_of_answer > current_num or number_of_answer == -1:
            current_cell= (-1,-1)
            #find next cell to cover
            for i in range(rows):
                for j in range(cols):
                    if not covered_cells[i][j]:
                        current_cell = (i,j)
            # if not found we are done
            if current_cell == (-1,-1):
                answers.append(current_chains)
                current_num += 1
                return

            covering_chains = [chain for chain in suitable_chains if current_cell in chain]
            total_length = sum(len(chain) for chain in current_chains)
            for c in covering_chains:
                max_length = rows*cols - total_length - len(c)
                suitable_for_c = [chain for chain in suitable_chains if (len(chain) == max_length or len(chain) <= max_length - 3 ) and (not any(pair in chain for pair in c))]
                for cell in c:
                    covered_cells[cell[0]][cell[1]] = True
                dfs(covered_cells, current_chains + [c], suitable_for_c)
                for cell in c:
                    covered_cells[cell[0]][cell[1]] = False
    
    dfs(covered_cells, [], chains)
    return answers


            
def get_all_words(language):
    if language == "finnish":
        return load_words_from_file("Dictionaries/all_finnish_words.txt", 10)
    elif language == "english":
        return ["dog", "cat", "rememberance", "cinderella"]
    else:
         return []
#if min sols -1 solve all
def solve(letters, language, min_sols):
    all_words = get_all_words(language)
    rows = len(letters)
    cols = len(letters[0])
    letters = [[letter.lower() for letter in row] for row in letters]

    chains = []
    for i in range(rows):
        for j in range(cols):
            chains += find_words_from_index(letters, i, j, all_words)
    unique_chains = filter_unique_sets(chains)
    unique_chains.sort(key=len, reverse=True)
    coordinates = cover_the_grid(unique_chains, rows, cols, min_sols)
    
    return coordinates



def is_valid_word(word, all_words_set):
    return word.lower() in all_words_set

def successors(i, j, rows, cols):
    # Define possible moves in 8 directions (including diagonals)
    directions = [(-1, -1), (-1, 0), (-1, 1),
                  (0, -1),          (0, 1),
                  (1, -1), (1, 0), (1, 1)]
    
    # Initialize list to hold valid successors
    valid_successors = []
    
    # Loop over each direction
    for di, dj in directions:
        ni, nj = i + di, j + dj  # New coordinates
        
        # Check if the new coordinates are within grid boundaries
        if 0 <= ni < rows and 0 <= nj < cols:
            valid_successors.append((ni, nj))
    
    return valid_successors

def count_neighbors(cell, not_covered_cells, rows, cols):
    x, y = cell
    # Define all potential neighbors, including diagonals
    potential_neigbours = successors(x, y, rows, cols) 
    
    # Filter valid neighbors that are within grid bounds and in not_covered_cells
    valid_neighbors = [
        (nx, ny) for nx, ny in potential_neigbours
        if (nx, ny) in not_covered_cells
    ]
    
    return len(valid_neighbors)

# -------------- Random grid functions ---------------

def weighted_random_choice(lst):
    n = len(lst)
    # Create weights that prefer the start
    weights = [1 / (i + 1) for i in range(n)]
    # Normalize weights to sum to 1
    total_weight = sum(weights)
    normalized_weights = [w / total_weight for w in weights]
    # Use random.choices to select with these weights
    return random.choices(lst, weights=normalized_weights, k=1)[0]

def get_rand_partition(cols, rows):
    ans = []
    sum = 0
    while(sum < rows*cols):
        rand_num = random.randint(3,10)
        if rows * cols - sum - rand_num < 3:
            rand_num = rows * cols - sum 
        if(rand_num > 10):
            continue
        ans.append(rand_num)
        sum += rand_num
    return ans

def rand_coordinates(cols,rows):
    partitions = get_rand_partition(cols, rows)
    partitions.sort(reverse=True)
    count = 0
    while(True):
        not_covered_cells = [(x, y) for x in range(rows) for y in range(cols)]  
        found = True
        ans = []
        for i in partitions:
            current_cell = random.choice(not_covered_cells)
            not_covered_cells.remove(current_cell)
            cells = [current_cell]
            for j in range(i-1):
                candidates = list(set(successors(current_cell[0], current_cell[1], rows, cols)).intersection(set(not_covered_cells)))
                candidates.sort(key= lambda cell: count_neighbors(cell, not_covered_cells, rows, cols))
                if(len(candidates) == 0):
                    found = False
                    break
                current_cell = weighted_random_choice(candidates)
                cells.append(current_cell)
                not_covered_cells.remove(current_cell)

            if(not found):
                break
            ans.append(cells)
        if(found):
            break
    return ans

def rand_letters(cords, language, cols, rows):
    all_words = get_all_words(language)
    words = []
    for i in cords:
        words.append(random.choice([s for s in all_words if len(s) == len(i)]))
    
    letters = [["" for _ in range(cols)] for _ in range(rows)]

    chain_index = 0
    for chain in cords:
        letter_index = 0
        for cell in chain:
            letters[cell[0]][cell[1]] = words[chain_index][letter_index].upper()
            letter_index +=1
        chain_index +=1
    return letters


def get_random_grid(selected_language, cols, rows, given_seed):
    random.seed(given_seed)
    coord = rand_coordinates(cols, rows)
    return rand_letters(coord, selected_language, cols, rows)




assignments = []
from collections import Counter

def cross(a, b):
    "Cross product of elements in A and elements in B."
    return [s+t for s in a for t in b]

rows = 'ABCDEFGHI'
cols = '123456789'
boxes = cross(rows, cols)
row_units = [cross(r, cols) for r in rows]
column_units = [cross(rows, c) for c in cols]
square_units = [cross(rs, cs) for rs in ('ABC','DEF','GHI') for cs in ('123','456','789')]
diagonal_units = [[r+c for r,c in zip(rows,cols)], [r+c for r,c in zip(rows,cols[::-1])]]

diagunitlist = row_units + column_units + square_units + diagonal_units
diagunits = dict((s, [u for u in diagunitlist if s in u]) for s in boxes)
diagpeers = dict((s, set(sum(diagunits[s],[]))-set([s])) for s in boxes)

standardunitlist = row_units + column_units + square_units
standardunits = dict((s, [u for u in standardunitlist if s in u]) for s in boxes)
standardpeers = dict((s, set(sum(standardunits[s],[]))-set([s])) for s in boxes)

def assign_value(values, box, value):
    """
    Please use this function to update your values dictionary!
    Assigns a value to a given box. If it updates the board record it.
    """
    values[box] = value
    if len(value) == 1:
        assignments.append(values.copy())
    return values

def naked_twins(values):
    unitlist = standardunitlist
    for unit in unitlist:
        twins = Counter([values[peerkey] for peerkey in unit])
        for twinkey, twinvalue in twins.items():
            if len(twinkey) == twinvalue and twinvalue > 1:
                #print(twinkey)
                for peer in unit:
                    if values[peer] != twinkey:
                        #print("killing "+str(twinkey)+" in "+peer)
                        for n in twinkey:
                            values[peer] = values[peer].replace(n,'')
    return values

def make_number(value):
    if value == '.':
        return cols
    return value

def grid_values(grid):
    characters = list(grid)
    return dict((boxes[b],make_number(a)) for (a,b) in zip(characters,range(len(characters))))

def display(values):
    width = 1+max(len(values[s]) for s in boxes)
    line = '+'.join(['-'*(width*3)]*3)
    for r in rows:
        print(''.join(values[r+c].center(width)+('|' if c in '36' else '')
                      for c in cols))
        if r in 'CF': print(line)
    return

def eliminate(values,diag):
    peers = standardpeers
    if diag:
        peers = diagpeers
    for key, value in values.items():
        if len(value) == 1:
            for peer in peers[key]:
                values[peer] = values[peer].replace(value,'')
    return values

def only_choice(values,diag):
    unitlist = standardunitlist
    if diag:
        unitlist = diagunitlist
    for unit in unitlist:
        for digit in cols:
            dplaces = [box for box in unit if digit in values[box]]
            if len(dplaces) == 1:
                values[dplaces[0]] = digit
    return values

def reduce_puzzle(values,diag):
    solved_values = [box for box in values.keys() if len(values[box]) == 1]
    stalled = False
    while not stalled:
        # Check how many boxes have a determined value
        solved_values_before = len([box for box in values.keys() if len(values[box]) == 1])

        # Your code here: Use the Eliminate Strategy
        values = eliminate(values,diag)

        # Your code here: Use the Only Choice Strategy
        values = only_choice(values,diag)

        # Check how many boxes have a determined value, to compare
        solved_values_after = len([box for box in values.keys() if len(values[box]) == 1])
        # If no new values were added, stop the loop.
        stalled = solved_values_before == solved_values_after
        # Sanity check, return False if there is a box with zero available values:
        if len([box for box in values.keys() if len(values[box]) == 0]):
            return False

    return values

def solve(grid):
    result, board = search(grid,True)
    return board


def search(values,diag):
    "Using depth-first search and propagation, create a search tree and solve the sudoku."
    # First, reduce the puzzle using the previous function
    values = reduce_puzzle(values,diag)

    if values is False:
        return False, None

    # Chose one of the unfilled square s with the fewest possibilities
    if all(len(val) == 1 for val in values.values()):
        return True, values
    
    minIndex = 0
    minValue = 99
    for s in boxes:
        if len(values[s]) > 1:
            if len(values[s]) < minValue:
                minIndex = s
                minValue = len(values[s])
                
    possibilities = values[minIndex]
    for possibility in list(possibilities):
        newvalues = values.copy()
        newvalues[minIndex] = possibility
        result, board = search(newvalues,diag)
        if result:
            return result, board

    print("couldn't find")
    display(results)
    
    return False, None

#diag_sudoku_grid = '2.............62....1....7...6..8...3...9...7...6..4...4....8....52.............3'
#parsed_grid = grid_values(diag_sudoku_grid)
#display(parsed_grid)
#print(solve(parsed_grid))

try:
    from visualize import visualize_assignments
    visualize_assignments(assignments)
except:
    print('We could not visualize your board due to a pygame issue. Not a problem! It is not a requirement.')



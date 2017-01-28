assignments = []

def cross(a, b):
  "Cross product of elements in A and elements in B."
  return [s + t for s in a for t in b]

def crosslist(l1, l2):
  return [ (e1, e2) for e1 in l1 for e2 in l2 ]

digits = '123456789'
rows = 'ABCDEFGHI'
cols = digits
boxes = cross(rows, cols)
row_units = [cross(r, cols) for r in rows]
column_units = [cross(rows, c) for c in cols]
square_units = [cross(r, c) for r in ('ABC', 'DEF', 'GHI') for c in ('123', '456', '789')]
diag_units = [ [ f+s for (f, s) in zip(rows, cols) ], [ f+s for (f, s) in zip(rows, cols[::-1]) ] ]
unitlist = row_units + column_units + square_units + diag_units

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
  """Eliminate values using the naked twins strategy.
  Args:
      values(dict): a dictionary of the form {'box_name': '123456789', ...}

  Returns:
      the values dictionary with the naked twins eliminated from peers.
  """
  for u in unitlist:
    for b1, b2 in crosslist(u, u):
      if b1 != b2 and len(values[b1]) == 2 and values[b1] == values[b2]:
        for b in u:
          if b != b1 and b != b2:
            values[b] = values[b].replace(values[b1][0], '')
            values[b] = values[b].replace(values[b1][1], '')
  return values

def grid_values(grid):
  """
  Convert grid into a dict of {square: char} with '123456789' for empties.
  Args:
      grid(string) - A grid in string form.
  Returns:
      A grid in dictionary form
          Keys: The boxes, e.g., 'A1'
          Values: The value in each box, e.g., '8'. If the box has no value, then the value will be '123456789'.
  """
  chars = []
  for c in grid:
    if c in digits:
      chars.append(c)
    else:
      chars.append(digits)
  assert(len(chars) == 81)
  return dict(zip(boxes, chars))

def display(values):
  """
  Display the values as a 2-D grid.
  Args:
      values(dict): The sudoku in dictionary form
  """
  width = 1+max(len(values[s]) for s in boxes)
  line = '+'.join(['-'*(width*3)]*3)
  for r in rows:
    print(''.join(values[r+c].center(width)+('|' if c in '36' else '')
      for c in cols))
    if r in 'CF': print(line)
  return

def eliminate(values):
  newvalues = { k: v for k, v in values.items() }
  for b in boxes:
    if len(values[b]) == 1:
      ridx = ord(b[0]) - ord('A')
      cidx = ord(b[1]) - ord('1')
      for r in row_units[ridx]:
        if b != r:
          newvalues[r] = newvalues[r].replace(values[b], '')
      for c in column_units[cidx]:
        if b != c:
          newvalues[c] = newvalues[c].replace(values[b], '')
      for s in square_units[(ridx // 3) * 3 + cidx // 3]:
        if b != s:
          newvalues[s] = newvalues[s].replace(values[b], '')
      if b in diag_units[0]:
        for d in diag_units[0]:
          if b != d:
            newvalues[d] = newvalues[d].replace(values[b], '')
      if b in diag_units[1]:
        for d in diag_units[1]:
          if b != d:
            newvalues[d] = newvalues[d].replace(values[b], '')
  return newvalues

def check_unit(values, unit):
  digits  ='123456789'
  d = { k : [] for k in digits } # dictionary from digit (1-9) to box
  for b in unit:
    for c in values[b]:
      d[c].append(b)
  for k, v in d.items():
    if len(v) == 1:
      values[v[0]] = k

def only_choice(values):
  for u in unitlist:
    check_unit(values, u)
  return values

def reduce_puzzle(values):
  stalled = False
  while not stalled:
    solved_before = len([b for b in values.keys() if len(values[b]) == 1])
    values = eliminate(values)
    values = only_choice(values)
    values = naked_twins(values)
    solved_after = len([b for b in values.keys() if len(values[b]) == 1])
    stalled = solved_before == solved_after
    if len([b for b in values.keys() if len(values[b]) == 0]):
      return False
  return values

def solved(values):
  return len([b for b in values.keys() if len(values[b]) == 1]) == 81

def search(values):
  values = reduce_puzzle(values)
  if values == False:
    return False
  if solved(values):
    return values
  minlen, b = min((len(values[b]), b) for b in values.keys() if len(values[b]) > 1)
  for d in values[b]:
    copy = { k: v for k, v in values.items() }
    copy[b] = d
    copy = search(copy)
    if copy:
      return copy

def solve(grid):
  """
  Find the solution to a Sudoku grid.
  Args:
      grid(string): a string representing a sudoku grid.
          Example: '2.............62....1....7...6..8...3...9...7...6..4...4....8....52.............3'
  Returns:
      The dictionary representation of the final sudoku grid. False if no solution exists.
  """
  puzzle = grid_values(grid)
  puzzle = search(puzzle)
  for box, value in puzzle.items():
    assign_value(puzzle, box, value)
  assert(len(assignments) == 81)
  return puzzle

if __name__ == '__main__':
  diag_sudoku_grid = '2.............62....1....7...6..8...3...9...7...6..4...4....8....52.............3'
  display(solve(diag_sudoku_grid))

  try:
    from visualize import visualize_assignments
    visualize_assignments(assignments)
  except:
    print('We could not visualize your board due to a pygame issue. Not a problem! It is not a requirement.')

import curses
from random import choice

# Shapes and rotations
shapes = [
    [[1, 1, 1], [0, 1, 0]],  # T shape
    [[1, 1], [1, 1]],        # Square shape
    [[1, 1, 1, 1]],          # Line shape
    [[0, 1, 1], [1, 1, 0]],  # Z shape
    [[1, 1, 0], [0, 1, 1]]   # S shape
]

# Initialize colors
def init_colors():
    curses.start_color()
    # Define bright color pairs
    curses.init_pair(1, curses.COLOR_WHITE, curses.COLOR_BLACK)   # White
    curses.init_pair(2, curses.COLOR_YELLOW, curses.COLOR_BLACK)  # Yellow
    curses.init_pair(3, curses.COLOR_CYAN, curses.COLOR_BLACK)    # Cyan
    curses.init_pair(4, curses.COLOR_MAGENTA, curses.COLOR_BLACK) # Magenta
    curses.init_pair(5, curses.COLOR_BLUE, curses.COLOR_BLACK)    # Bright Blue
    curses.init_pair(6, curses.COLOR_GREEN, curses.COLOR_BLACK)   # Bright Green

# Choose random bright color pair ID
def random_color_id():
    return choice(range(1, 7))  # ID 1-6 sesuai pasangan warna terang

# Initialize screen
def init_screen():
    screen = curses.initscr()
    curses.curs_set(0)
    sh, sw = screen.getmaxyx()
    win = curses.newwin(sh, sw, 0, 0)
    win.keypad(1)
    win.timeout(300)  
    return win

# Check if a move is valid
def valid_move(grid, shape, offset):
    x, y = offset
    for i, row in enumerate(shape):
        for j, cell in enumerate(row):
            if cell and (
                x + i >= len(grid) or
                y + j >= len(grid[0]) or
                y + j < 0 or
                grid[x + i][y + j]
            ):
                return False
    return True

# Add shape to grid
def add_to_grid(grid, shape, offset):
    x, y = offset
    for i, row in enumerate(shape):
        for j, cell in enumerate(row):
            if cell:
                grid[x + i][y + j] = cell

# Clear full lines
def clear_lines(grid):
    new_grid = [row for row in grid if any(cell == 0 for cell in row)]
    lines_cleared = len(grid) - len(new_grid)
    for _ in range(lines_cleared):
        new_grid.insert(0, [0 for _ in grid[0]])
    return new_grid, lines_cleared

# Draw grid on screen
def draw_grid(win, grid, current_shape, shape_pos, color_map):
    for i, row in enumerate(grid):
        for j, cell in enumerate(row):
            if cell:
                color = color_map.get((i, j), 1)  # Default white
                win.addch(i, j * 2, "#", curses.color_pair(color))
            else:
                win.addch(i, j * 2, ".")

    # Draw the current shape
    for i, row in enumerate(current_shape):
        for j, cell in enumerate(row):
            if cell:
                try:
                    color = color_map.get((shape_pos[0] + i, shape_pos[1] + j), 1)
                    win.addch(shape_pos[0] + i, (shape_pos[1] + j) * 2, "#", curses.color_pair(color))
                except curses.error:
                    pass

# Rotate shape
def rotate_shape(shape):
    rows, cols = len(shape), len(shape[0])
    new_shape = [[0] * rows for _ in range(cols)]
    for i in range(rows):
        for j in range(cols):
            new_shape[j][rows - 1 - i] = shape[i][j]
    return new_shape

# Main
def tetris():
    win = init_screen()
    init_colors()
    sh, sw = win.getmaxyx()
    grid_width = min(sw // 2, 10)
    grid_height = sh - 1
    grid = [[0 for _ in range(grid_width)] for _ in range(grid_height)]
    color_map = {}

    current_shape = choice(shapes)
    current_color = random_color_id()
    shape_pos = [0, max(0, grid_width // 2 - len(current_shape[0]) // 2)]
    score = 0

    key = None
    while True:
        win.clear()
        draw_grid(win, grid, current_shape, shape_pos, color_map)

        # Display score
        max_x = win.getmaxyx()[1]
        if 2 * grid_width + 12 < max_x:
            win.addstr(0, 2 * grid_width + 2, f"Score: {score}")
        else:
            win.addstr(0, 0, f"Score: {score}")

        # Player input
        next_key = win.getch()
        key = next_key if next_key != -1 else None
        new_pos = list(shape_pos)

        if key == curses.KEY_DOWN:
            new_pos[0] += 1
        elif key == curses.KEY_LEFT:
            new_pos[1] -= 1
        elif key == curses.KEY_RIGHT:
            new_pos[1] += 1
        elif key == curses.KEY_UP:
            rotated_shape = rotate_shape(current_shape)
            if valid_move(grid, rotated_shape, shape_pos):
                current_shape = rotated_shape

        if key is None:
            new_pos[0] += 1

        if valid_move(grid, current_shape, new_pos):
            shape_pos = new_pos
        else:
            if key is None or key == curses.KEY_DOWN:
                add_to_grid(grid, current_shape, shape_pos)
                for i, row in enumerate(current_shape):
                    for j, cell in enumerate(row):
                        if cell:
                            color_map[(shape_pos[0] + i, shape_pos[1] + j)] = current_color
                score += 10
                grid, cleared = clear_lines(grid)
                score += cleared * 10
                current_shape = choice(shapes)
                current_color = random_color_id()
                shape_pos = [0, max(0, grid_width // 2 - len(current_shape[0]) // 2)]
                if not valid_move(grid, current_shape, shape_pos):
                    break

    curses.endwin()
    print(f"Game Over! Your score: {score}")

if __name__ == "__main__":
    tetris()

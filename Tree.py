import numpy as np
import tkinter as tk


# Define the heuristic function
def heuristic(board, player):
    rows, cols = board.shape
    score = 0

    # Check horizontal lines
    for row in range(rows):
        for col in range(cols - 3):
            window = board[row, col:col + 4]
            score += evaluate_window(window, player)

    # Check vertical lines
    for row in range(rows - 3):
        for col in range(cols):
            window = board[row:row + 4, col]
            score += evaluate_window(window, player)

    # Check positively sloped diagonals
    for row in range(rows - 3):
        for col in range(cols - 3):
            window = [board[row + i, col + i] for i in range(4)]
            score += evaluate_window(window, player)

    # Check negatively sloped diagonals
    for row in range(3, rows):
        for col in range(cols - 3):
            window = [board[row - i, col + i] for i in range(4)]
            score += evaluate_window(window, player)

    return score


# Helper function to evaluate a window of 4 cells
def evaluate_window(window, player):
    score = 0
    opponent = 1 if player == 2 else 2

    if np.count_nonzero(window == player) == 4:
        score += 100
    elif np.count_nonzero(window == player) == 3 and np.count_nonzero(window == 0) == 1:
        score += 5
    elif np.count_nonzero(window == player) == 2 and np.count_nonzero(window == 0) == 2:
        score += 2

    if np.count_nonzero(window == opponent) == 3 and np.count_nonzero(window == 0) == 1:
        score -= 4

    return score


# Class to represent a node in the game tree
class Node:
    def init(self, state, board, player, depth=0):
        self.state = state
        self.board = board
        self.player = player
        self.children = []
        self.depth = depth

    def str(self):
        return str(self.state)


# Function to generate the game tree up to a certain depth
def generate_game_tree(node, depth, max_depth):
    if depth >= max_depth:
        return

    rows, cols = node.board.shape
    for col in range(cols):
        for row in range(rows - 1, -1, -1):
            if node.board[row][col] == 0:
                new_board = node.board.copy()
                new_board[row][col] = node.player
                child_node = Node(f"Player {node.player} move at ({row}, {col})", new_board, 3 - node.player, depth + 1)
                node.children.append(child_node)
                generate_game_tree(child_node, depth + 1, max_depth)
                break


# Function to draw the game tree using tkinter Canvas with colors
def draw_game_tree(canvas, node, x=960, y=60, dx=200, dy=150):
    color = "blue" if node.player == 1 else "green"
    canvas.create_text(x, y, text=str(node), tags="node", fill=color, font=("Helvetica", 12, "bold"))

    for i, child in enumerate(node.children):
        child_x = x + (i - len(node.children) / 2) * dx
        child_y = y + dy
        canvas.create_line(x, y + 10, child_x, child_y - 10, fill="gray")
        draw_game_tree(canvas, child, child_x, child_y, dx / max(1, len(node.children) - 1))


# GUI class to display the game tree
class GameTreeGUI:
    def init(self, root_node):
        self.root_node = root_node

        self.root = tk.Tk()
        self.root.title("Game Tree")

        self.canvas = tk.Canvas(self.root, width=1920, height=1080, bg="white")
        self.canvas.pack(side=tk.TOP, fill=tk.BOTH, expand=True)

        self.draw_tree()

        tk.Button(self.root, text="Quit", command=self.root.quit).pack(side=tk.BOTTOM)

    def draw_tree(self):
        draw_game_tree(self.canvas, self.root_node)


# Example usage
if __name__ == "main":
    # Initialize an empty board (6x7)
    board = np.zeros((6, 7), dtype=int)

    # Create the root node of the game tree
    root_node = Node("Root", board, player=1)

    # Generate the game tree up to a certain depth (e.g., depth=3)
    generate_game_tree(root_node, depth=0, max_depth=3)

    print("\nGame Tree:")

    # Draw the game tree using GUI
    gui = GameTreeGUI(root_node)
    gui.root.mainloop()
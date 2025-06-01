
import pygame   #library Used for visualization and creating a graphical interface.
import heapq    #Provides a priority queue for algorithms like A* and Greedy Best-First Search.
from collections import deque  #A double-ended queue used for efficient BFS.
import time #Included for potential delays, but not directly used in this code.

# Directions for moving in the grid: Right, Left, Down, Up
DIRECTIONS = [(0, 1), (0, -1), (1, 0), (-1, 0)]

# Colors for visualization
WHITE = (255, 255, 255)  # Grid color
BLACK = (0, 0, 0)        # Unused, but can be for the background
GREEN = (0, 255, 0)      # Final point color and path color
RED = (255, 0, 0)        # Obstacle color
BLUE = (0, 0, 255)       # (Unused, but can be used for visualizing path)
GREY = (169, 169, 169)   # Searching (current cell being explored)

# Grid parameters
CELL_SIZE = 50 #Appear as a 50x50 square.
MARGIN = 2 #Have a 2-pixel gap between it and adjacent cells.

# BFS Algorithm
def bfs(grid, start, goal, draw, clock): #A Pygame clock object for controlling the speed of visualization.
    rows, cols = len(grid), len(grid[0])  #Get the dimensions of the grid.
    queue = deque([(*start, [])]) # A deque (double-ended queue) to store cells to be explored.
    visited = set() #A set to track visited cells, ensuring the algorithm does not revisit them.
    visited.add(start) #The starting cell is immediately marked as visited.

    path = [] #A list to store the sequence of cells from the start to the goal. It gets updated as the algorithm explores the grid.

    while queue: # This loop continues until there are no cells left to explore in the queue.
        r, c, current_path = queue.popleft() # Removes the first element from the queue (FIFO behavior).( ""r = row and c = coloumn"")
        draw((r, c), GREY)  # Highlight current cell being explored
        path = current_path + [(r, c)]  #Updates the path by appending the current cell (r, c) to current_path.
        
        # Wait for space bar press to continue to next step
        waiting_for_input = True    #The visualization pauses at each step until the user presses the Spacebar.
        while waiting_for_input:
            for event in pygame.event.get():  # This allows step-by-step inspection of the algorithm's process.
                if event.type == pygame.QUIT: #If the user closes the Pygame window (pygame.QUIT), the program exits.
                    pygame.quit()
                if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                    waiting_for_input = False

        if (r, c) == goal:  #If the current cell (r, c) matches the goal cell, the algorithm returns the path as the solution.
            return path

        for dr, dc in DIRECTIONS:  # A list of possible moves (right, left, down, up).
            nr, nc = r + dr, c + dc  # Calculate the neighbor’s row and column: nr = r + dr, nc = c + dc.
            if 0 <= nr < rows and 0 <= nc < cols and grid[nr][nc] == 0 and (nr, nc) not in visited:
                # 0 <= nr < rows and 0 <= nc < cols: Ensures the neighbor is within grid boundaries.
                #grid[nr][nc] == 0: Ensures the neighbor is a free cell (not an obstacle).
                #(nr, nc) not in visited: Ensures the neighbor has not been visited before.
                visited.add((nr, nc)) #Add (nr, nc) to the visited set.
                queue.append((nr, nc, path)) #Append (nr, nc, path) to the queue.

    return None #If the queue becomes empty without finding the goal, return None to indicate that no path exists.

# DFS Algorithm
def dfs(grid, start, goal, draw, clock):
    rows, cols = len(grid), len(grid[0])  #Get the dimensions of the grid.
    stack = [(start, [])] #A stack (list) to store cells to be explored. It starts with the start position and an empty path.
    visited = set()  
    visited.add(start)  

    path = []  #A list to store the sequence of cells from the start to the goal. It gets updated as the algorithm explores the grid.

    while stack:  #This loop continues until there are no cells left to explore in the stack.
        (r, c), current_path = stack.pop()  #Removes the last element from the stack (LIFO behavior).
        draw((r, c), GREY)  # Highlight current cell being explored
        path = current_path + [(r, c)]
        
        # Wait for space bar press to continue to next step
        waiting_for_input = True
        while waiting_for_input:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                    waiting_for_input = False

        if (r, c) == goal:
            return path

        for dr, dc in DIRECTIONS: 
            nr, nc = r + dr, c + dc
            if 0 <= nr < rows and 0 <= nc < cols and grid[nr][nc] == 0 and (nr, nc) not in visited:
                visited.add((nr, nc))
                stack.append(((nr, nc), path))

    return None

# Greedy Best-First Search (GBFS) Algorithm
def gbfs(grid, start, goal, draw, clock):
    rows, cols = len(grid), len(grid[0])
    open_list = [(0, start, [])]  # A priority queue (using a min-heap) that stores cells to explore, initialized with
    #   0: The heuristic value for the start node (distance to goal).
    #   start: The starting cell (row, column).
    #   []: An empty path (no steps taken yet).
    visited = set()  #visited: A set to keep track of visited cells to avoid revisiting them.
    visited.add(start)

    def heuristic(a, b):  #Purpose: To estimate the "cost" (distance) from the current cell a to the goal cell b.
        return abs(a[0] - b[0]) + abs(a[1] - b[1])  # Manhattan Distance
    # This heuristic is suitable for grid-based movement without diagonal moves.
    # Formula: ∣𝑥1−𝑥2∣+∣𝑦1−𝑦2∣.

    path = []

    while open_list: #The algorithm continues as long as there are cells in the open_list to explore.
        _, (r, c), current_path = heapq.heappop(open_list) #heapq.heappop(open_list): Removes and retrieves the cell with the smallest heuristic value (highest priority) from the priority queue
        #   _: The heuristic value (not used further in this step).
        draw((r, c), GREY)  # Highlight current cell being explored
        path = current_path + [(r, c)]
        
        # Wait for space bar press to continue to next step
        waiting_for_input = True
        while waiting_for_input:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                    waiting_for_input = False

        if (r, c) == goal:
            return path

        for dr, dc in DIRECTIONS:
            nr, nc = r + dr, c + dc
            if 0 <= nr < rows and 0 <= nc < cols and grid[nr][nc] == 0 and (nr, nc) not in visited:
                visited.add((nr, nc))
                heapq.heappush(open_list, (heuristic((nr, nc), goal), (nr, nc), path))
                #Calculate the heuristic value: heuristic((nr, nc), goal).
                #Append the neighbor to the open_list using heapq.heappush()

    return None  #If the open_list becomes empty without finding the goal, return None to indicate that no path exists.
# A* Algorithm
def a_star(grid, start, goal, draw, clock):
    rows, cols = len(grid), len(grid[0])
    open_list = [(0, 0, start, [])]  # f, g, node, path
    visited = set()
    visited.add(start)

    def heuristic(a, b):
        return abs(a[0] - b[0]) + abs(a[1] - b[1])  # Manhattan Distance

    path = []

    while open_list:
        _, g, (r, c), current_path = heapq.heappop(open_list)
        draw((r, c), GREY)  # Highlight current cell being explored
        path = current_path + [(r, c)]
        
        # Wait for space bar press to continue to next step
        waiting_for_input = True
        while waiting_for_input:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                    waiting_for_input = False

        if (r, c) == goal:
            return path

        for dr, dc in DIRECTIONS:
            nr, nc = r + dr, c + dc
            if 0 <= nr < rows and 0 <= nc < cols and grid[nr][nc] == 0 and (nr, nc) not in visited:
                visited.add((nr, nc))
                heapq.heappush(open_list, (g + 1 + heuristic((nr, nc), goal), g + 1, (nr, nc), path)) #g+1: Actual cost to the neighbor
                #heuristic((nr,nc),goal): Estimated cost from the neighbor to the goal.

#A* evaluates the total cost 𝑓 = 𝑔 + ℎ, where:g: Cost from start to current cell.h: Estimated cost from current cell to goal.
    return None

# UCS Algorithm
def ucs(grid, start, goal, draw, clock):
    rows, cols = len(grid), len(grid[0])
    open_list = [(0, start, [])]  # cost, node, path
    visited = set()
    visited.add(start)

    path = []

    while open_list:
        cost, (r, c), current_path = heapq.heappop(open_list)  #Removes and retrieves the cell with the lowest cost from the open_list.
        draw((r, c), GREY)  # Highlight current cell being explored
        path = current_path + [(r, c)]
        
        # Wait for space bar press to continue to next step
        waiting_for_input = True
        while waiting_for_input:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                    waiting_for_input = False

        if (r, c) == goal:
            return path

        for dr, dc in DIRECTIONS:
            nr, nc = r + dr, c + dc
            if 0 <= nr < rows and 0 <= nc < cols and grid[nr][nc] == 0 and (nr, nc) not in visited:
                visited.add((nr, nc))
                heapq.heappush(open_list, (cost + 1, (nr, nc), path)) #Calculate the new cost to the neighbor: newcost = current cost+1.

    return None

# Beam Search Algorithm
def beam_search(grid, start, goal, draw, clock, beam_width=3):
    #beam_width : Limits the number of candidate paths explored at each step.
    rows, cols = len(grid), len(grid[0])
    open_list = [(0, start, [])]
    visited = set()
    visited.add(start)

    path = []

    while open_list: #The loop runs until there are no nodes left to explore in the open_list.
        #The lambda function is a short, inline function that takes a single argument (x).
        #x represents each element in the open_list.
        #x[0] accesses the first element of the tuple (i.e., the heuristic_value).
        #The sorted function uses this heuristic_value to sort the list in ascending order (smallest heuristic values come first).
        open_list = sorted(open_list, key=lambda x: x[0])[:beam_width]  # Select top `beam_width` nodes
        #Sorts the open_list by heuristic value (x[0]).
        #Selects the top beam_width nodes for the next level of exploration.
        next_open_list = [] #next_open_list: A temporary list to hold the next level of nodes to explore.

        for _, (r, c), current_path in open_list: #Loops through the selected nodes (open_list).
            draw((r, c), GREY)  # Highlight current cell being explored
            path = current_path + [(r, c)]
            
            # Wait for space bar press to continue to next step
            waiting_for_input = True
            while waiting_for_input:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit()
                    if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                        waiting_for_input = False

            if (r, c) == goal:
                return path

            for dr, dc in DIRECTIONS:
                nr, nc = r + dr, c + dc
                if 0 <= nr < rows and 0 <= nc < cols and grid[nr][nc] == 0 and (nr, nc) not in visited:
                    visited.add((nr, nc))
                    next_open_list.append((abs(nr - goal[0]) + abs(nc - goal[1]), (nr, nc), path))
                    # Compute the heuristic: abs(nr - goal[0]) + abs(nc - goal[1]) (Manhattan Distance).
                    # Append the neighbor to next_open_list with the new heuristic and updated path.

        open_list = next_open_list # Replace the current open_list with next_open_list for the next iteration.

    return None

# Function to visualize the grid
def visualize(grid, start, goal, algorithm):
    pygame.init() #Initializes all Pygame modules required for graphics, event handling, and more.
    rows, cols = len(grid), len(grid[0])
    width, height = cols * CELL_SIZE, rows * CELL_SIZE #Calculate the total screen size based on cell dimensions and grid size
    screen = pygame.display.set_mode((width, height)) #pygame.display.set_mode: Creates a Pygame window with the calculated dimensions.
    pygame.display.set_caption("Grid-Based Robot Navigation") #pygame.display.set_caption: Sets the window title to "Grid-Based Robot Navigation."

    clock = pygame.time.Clock()  # Control visualization speed
    #clock: A Pygame object used to control the frame rate or speed of visualization.

    def draw_cell(pos, color): #Takes a grid position (pos) and a color to draw a rectangle on the grid.
        r, c = pos #pos: A tuple (r, c) representing the row and column of the cell to be drawn.
        pygame.draw.rect(  
            screen,
            color,  #
            [(MARGIN + CELL_SIZE) * c + MARGIN  , (MARGIN + CELL_SIZE) * r  + MARGIN, CELL_SIZE, CELL_SIZE  ]
        )
        # pygame.draw.rect: Draws a rectangle on the screen
        # (MARGIN + CELL_SIZE) * c + MARGIN  'X-coordinate' 
        # (MARGIN + CELL_SIZE) * r ' Y-coordinate'
        # MARGIN, CELL_SIZE, CELL_SIZE 'Width and height of the rectangle'
        
        
        pygame.display.flip()  #pygame.display.flip(): Updates the Pygame window to reflect the new cell color immediately.

    def draw_grid():
        for row in range(rows):
            for col in range(cols):
                color = WHITE if grid[row][col] == 0 else RED  # Obstacles are red ,Free cells (value 0 in the grid) are colored WHITE.
                draw_cell((row, col), color)
        draw_cell(start, GREEN)  # Start position in green
        draw_cell(goal, GREEN)  # Goal position in green

    # Draw initial grid
    draw_grid()  #This line calls the draw_grid function to draw the grid before the algorithm begins.
    
    # Run the chosen algorithm
    path = algorithm(grid, start, goal, draw_cell, clock) #Runs the selected pathfinding algorithm to find the shortest path (or any path) from start to goal.

    # Draw the final path
    if path:
        for r, c in path: #Iterates through each cell (r, c) in the path.
            draw_cell((r, c), GREEN)  # Path is green
            clock.tick(60) #Adds a small delay (clock.tick(60)) between drawing each cell to make the visualization smooth and understandable.
    else:
        print("No path found.")

    # Keep the window open until closed by the user
    running = True
    while running: #Starts a while loop that continuously checks for events.
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
    pygame.quit() # the user closes the window (pygame.QUIT), the loop ends, and Pygame is terminated using pygame.quit().

# Function to get user input for the grid and algorithm
def get_user_input():
    print("Welcome to Grid-Based Robot Navigation!") #Displays a greeting message to introduce the program.

    # Input grid size , Asks the user for the number of rows and columns in the grid
    rows = int(input("Enter the number of rows: "))
    cols = int(input("Enter the number of columns: "))

    # Initialize grid with all free cells (0)
    grid = [[0 for _ in range(cols)] for _ in range(rows)] #Creates a 2D grid initialized with 0 (indicating free cells).

    # Input number of obstacles
    num_obstacles = int(input("Enter the number of obstacles: "))
    print("Enter the positions of obstacles (row and column, space-separated):")
    for _ in range(num_obstacles): #Iterates num_obstacles times to input obstacle positions (r, c):
        r, c = map(int, input("Obstacle: ").split())
         # .split() is used to:Take the user input as a single string.Break it into separate components (like row and column) by splitting at spaces.
        if 0 <= r < rows and 0 <= c < cols: #The obstacle must be within the grid boundaries (0 <= r < rows and 0 <= c < cols).
            grid[r][c] = 1 # the place with obstacle will be marke as 1 
        else:
            print("Invalid position, skipping!") #If the user enters a position outside the grid, it skips that input.

    # Input start and goal positions, Asks the user to input the start and goal positions as tuples (row, column).
    print("Enter the start position (row and column, space-separated):")
    start = tuple(map(int, input("Start: ").split()))
    # .split() is used to:Take the user input as a single string.Break it into separate components (like row and column) by splitting at spaces.
    print("Enter the goal position (row and column, space-separated):")
    goal = tuple(map(int, input("Goal: ").split()))
    # .split() is used to:Take the user input as a single string.Break it into separate components (like row and column) by splitting at spaces.

    # Validate inputs
    if not (0 <= start[0] < rows and 0 <= start[1] < cols) or grid[start[0]][start[1]] == 1: #Cannot be an obstacle (grid[start[0]][start[1]] == 1).
        raise ValueError("Invalid start position!")
    if not (0 <= goal[0] < rows and 0 <= goal[1] < cols) or grid[goal[0]][goal[1]] == 1:
        raise ValueError("Invalid goal position!")

    # Choose algorithm ,Displays a menu of algorithm options
    print("Choose the algorithm to use:")
    print("1. BFS (Breadth-First Search)")
    print("2. DFS (Depth-First Search)")
    print("3. GBFS (Greedy Best-First Search)")
    print("4. A* (A Star)")
    print("5. UCS (Uniform Cost Search)")
    print("6. Beam Search")

    choice = int(input("Enter the number corresponding to the algorithm: "))

    algorithms = {
        1: bfs,
        2: dfs,
        3: gbfs,
        4: a_star,
        5: ucs,
        6: beam_search
    }

    if choice not in algorithms:
        raise ValueError("Invalid algorithm choice!")

    return grid, start, goal, algorithms[choice] #Returns the configured grid, start position, goal position, and the selected algorithm function.

# Main function
if __name__ == "__main__":
    try:
        grid, start, goal, algorithm = get_user_input() #takes the input from the user 
        print(f"Visualizing {algorithm.__name__.replace('_', ' ').title()} step by step...") # takes the algorithm name such as bfs,dfs
        #algorithm.__name__: Retrieves the name of the function (e.g., "bfs" or "a_star").
        # replace('_', ' '): Replaces underscores in the name with spaces for readability.
        # title(): Capitalizes the first letter of each word (e.g., "Bfs" becomes "Bfs", "a_star" becomes "A Star").
        visualize(grid, start, goal, algorithm)
        #Calls the visualize() function to:
             # Render the grid and animate the chosen algorithm's step-by-step process of finding a path from the start to the goal.
    except Exception as e:
        print(f"Error: {e}")
        #If any error occurs (e.g., invalid user input, a crash during execution), the except block catches it.
        #Prints the error message to the user instead of crashing.

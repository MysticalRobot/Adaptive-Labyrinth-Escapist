import pygame
from graph import Graph
from dstar import DStar

# initialize a graph (and generate a maze)
G = Graph(n=10, allow_diagonal_movement=False)
facing_right = True

# load the images
amongus_left = pygame.image.load("amongus_left.png")
amongus_right = pygame.image.load("amongus_right.png")
vent = pygame.image.load("vent.png")

random_ahh_number_chosen_after_trial_and_error = 575
# as n increases, the vertex size decreases
vertex_size = int(random_ahh_number_chosen_after_trial_and_error  * (1 / G.old_n)) 
# as n increases, the edge size increases
edge_size = vertex_size // int(random_ahh_number_chosen_after_trial_and_error  * (1 / G.old_n)) if G.old_n > 60 else 10

# scale the images to draw appropriately
amongus_left = pygame.transform.scale(amongus_left, (vertex_size, vertex_size))
amongus_right = pygame.transform.scale(amongus_right, (vertex_size, vertex_size))
vent = pygame.transform.scale(vent, (vertex_size, vertex_size))

# initialize pygame
pygame.init()
dimension = (G.old_n * vertex_size + (G.old_n - 1) * edge_size) + G.old_n * 2
screen = pygame.display.set_mode((dimension, dimension))
clock = pygame.time.Clock()
running = True

# draws the maze
def draw_maze() -> None:
    screen.fill('grey') # draw the background
    row_offset = 0
    for row in range(G.n):
        col_offset = 0
        for col in range(G.n):
            curr = G.maze[row][col]
            if curr == G.ENDPOINT: 
                # draw the goal (vent) before the start (amongus) to account for overlap
                if (row, col) == G.goal:
                    screen.blit(vent, (G.goal[1] + col_offset, G.goal[0] + row_offset))
                if (row, col) == G.start:
                    amongus = amongus_right if facing_right else amongus_left
                    screen.blit(amongus, (G.start[1] + col_offset, G.start[0] + row_offset))
            # draw og walls black, and newly added walls red, and removed walls green
            elif curr != G.EMPTY_OR_EDGE:
                if curr == G.NO_EDGE:
                    color = 'black'
                elif curr == G.REMOVED_EDGE:
                    color = 'red'
                else:
                    color = 'green'
                width = edge_size if col & 1 else vertex_size
                height = edge_size if row & 1 else vertex_size
                pygame.draw.rect(screen, color, pygame.Rect(col + col_offset, row + row_offset, width, height))
            col_offset += edge_size if col & 1 else vertex_size
        row_offset += edge_size if row & 1 else vertex_size
    pygame.display.update() # update the screen

while running:
    for event in pygame.event.get():
        # stop when user has x'd out the window
        if event.type == pygame.QUIT: 
            running = False
        # add or remove some edges when requested by user
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_a:
                G.AddEdges()
            if event.key == pygame.K_d:
                G.RemoveEdges()
    draw_maze()
    clock.tick(60) # cap at 60 fps
pygame.quit()
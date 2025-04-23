import pygame
from graph import Graph
from dstar import DStar

# initialize a graph (and generate a maze)
G = Graph(10)
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
            block = G.maze[row][col]
            # draw the lack of an edge as a wall
            if block == 1:
                width = edge_size if col & 1 else vertex_size
                height = edge_size if row & 1 else vertex_size
                pygame.draw.rect(screen, 'black', pygame.Rect(col + col_offset, row + row_offset, width, height))
            elif block == 2: 
              # draw the goal (vent) before the start (amongus) to account for overlap
              if (row, col) == G.goal:
                  screen.blit(vent, (G.goal[1] + col_offset, G.goal[0] + row_offset))
              if (row, col) == G.start:
                  amongus = amongus_right if facing_right else amongus_left
                  screen.blit(amongus, (G.start[1] + col_offset, G.start[0] + row_offset))
            col_offset += edge_size if col & 1 else vertex_size
        row_offset += edge_size if row & 1 else vertex_size
    pygame.display.update() # update the screen

while running:
    # stop when user has x'd out the window
    for event in pygame.event.get():
        if event.type == pygame.QUIT: 
            running = False

    # TODO add key handling stuff here (for randomly removing or adding walls)
    keys = pygame.key.get_pressed()      
    '''
    if keys[pygame.K_a]:  
    if keys[pygame.K_d]:
    '''
  
    draw_maze() # draw the maze and update the screen
    clock.tick(60) # cap fps at 60

pygame.quit()
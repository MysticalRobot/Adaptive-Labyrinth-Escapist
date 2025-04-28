import pygame, sys, gif_pygame
from graph import Graph
from dstar import DStar
from bfs import BFS
from lpastar import LifelongPlanningAStar

# initialize a graph (and generate a maze)
G = Graph(n=10, allow_diagonal_movement=True)

# load the images and gif
win = pygame.display.set_mode((512, 512))
amongus_left = pygame.image.load("amongus_left.png")
amongus_right = pygame.image.load("amongus_right.png")
vent = pygame.image.load("vent.png")
venting = gif_pygame.load("amongus_venting.gif")

random_ahh_number_chosen_after_trial_and_error = 575
# as n increases, the vertex size decreases
vertex_size = int(random_ahh_number_chosen_after_trial_and_error  * (1 / G.old_n)) 
# as n increases, the edge size increases
edge_size = vertex_size // int(random_ahh_number_chosen_after_trial_and_error  * (1 / G.old_n)) if G.old_n > 60 else 10

# scale the images to draw appropriately
amongus_left = pygame.transform.scale(amongus_left, (vertex_size, vertex_size))
amongus_right = pygame.transform.scale(amongus_right, (vertex_size, vertex_size))
vent = pygame.transform.scale(vent, (vertex_size, vertex_size))
venting = gif_pygame.transform.scale(venting, (vertex_size, vertex_size))

# decide on algorithm
algorithm_name = 'dstar'
if algorithm_name == 'dstar':
    algorithm = DStar(G)
elif algorithm_name == 'lpastar':
    algorithm = LifelongPlanningAStar(G)
elif algorithm_name == 'bfs':
    algorithm = BFS(G)
# TODO handle additional algorithms here
else:
    'zehahahaha mugiwara'
algorithm.ComputeShortestPath() 

# initialize pygame
pygame.init()
dimension = (G.old_n * vertex_size + (G.old_n - 1) * edge_size) + G.old_n * 2
screen = pygame.display.set_mode((dimension, dimension))
clock = pygame.time.Clock()
facing_right = True
moves_are_allowed = True
running = True

# returns the color of the edge
def get_edge_color(edge : int) -> str:
    if edge == G.NO_EDGE:
        return 'black'
    elif edge == G.REMOVED_EDGE:
        return 'red'
    elif edge == G.NEW_EDGE: 
        return 'green'
    # this case generally isn't used
    else:
        return 'grey'

# draws the maze
def draw_maze() -> None:
    screen.fill('grey') # draw the background
    row_offset = 0
    for row in range(G.n):
        is_horizontal_wall = G.IsHorizontalWall(row)
        col_offset = 0
        for col in range(G.n):
            is_vertical_wall = G.IsVerticalWall(col)
            curr = G.maze[row][col]
            if curr == G.ENDPOINT: 
                if (moves_are_allowed):
                    # draw the goal (vent) before the start (amongus) to account for overlap
                    if (row, col) == G.goal:
                        screen.blit(vent, (G.goal[1] + col_offset, G.goal[0] + row_offset))
                    if (row, col) == G.start:
                        amongus = amongus_right if facing_right else amongus_left
                        screen.blit(amongus, (G.start[1] + col_offset, G.start[0] + row_offset))
                else:
                    if venting is not None:
                        venting.render(screen, (128-venting.get_width()*0.5, 256-venting.get_height()*0.5))
                        venting.render(screen, (G.goal[1] + col_offset, G.goal[0] + row_offset))
            # draw og walls black, newly added walls red, and removed walls green
            elif curr != G.EMPTY_OR_EDGE:
                width = edge_size if is_vertical_wall else vertex_size
                height = edge_size if is_horizontal_wall else vertex_size
                pygame.draw.rect(screen, get_edge_color(curr), pygame.Rect(col + col_offset, row + row_offset, width, height))
            col_offset += edge_size if is_vertical_wall else vertex_size
        row_offset += edge_size if is_horizontal_wall else vertex_size
    pygame.display.update() # update the screen

while running:
    for event in pygame.event.get():
        # stop when user has x'd out the window
        if event.type == pygame.QUIT: 
            running = False
        if event.type == pygame.KEYDOWN and moves_are_allowed:
            # add edges and recompute path
            if event.key == pygame.K_a:
                algorithm.AdaptToChanges(G.AddEdges())
            # remove edges and recompute path
            if event.key == pygame.K_d:
                algorithm.AdaptToChanges(G.RemoveEdges())
            # move amongus
            if event.key == pygame.K_w:
                new_start = algorithm.PickSuccessor()
                # change orientation of amongus based on move
                if new_start[1] < G.start[1]:
                    facing_right = False
                elif new_start[1] > G.start[1]:
                    facing_right = True
                G.MoveStart(new_start)
                if G.start == G.goal:
                    moves_are_allowed = False

    draw_maze()
    clock.tick(60) # cap at 60 fps

pygame.quit()
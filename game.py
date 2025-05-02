import pygame
import time
from init_algorithm import initialize_algorithm

# generate maze and initialize algorithm
_, algorithm = initialize_algorithm(algorithm_name='dstar', n=10, allow_diagonal_movement=True)
algorithm.ComputeShortestPath() 

random_ahh_number_chosen_after_trial_and_error = 575
# as n increases, the vertex size decreases
vertex_size = int(random_ahh_number_chosen_after_trial_and_error  * (1 / algorithm.G.old_n)) 
# as n increases, the edge size increases
edge_size = vertex_size // int(random_ahh_number_chosen_after_trial_and_error  * (1 / algorithm.G.old_n)) if algorithm.G.old_n > 60 else 10

# load and scale all the images
amongus = pygame.transform.scale(pygame.image.load("assets/amongus.png"), (vertex_size * 0.8, vertex_size * 0.7))
vent = pygame.transform.scale(pygame.image.load("assets/vent.png"), (vertex_size * 0.8, vertex_size * 0.5))
venting_frames = [pygame.transform.scale(pygame.image.load(f'assets/venting_frame{i}.png'), (vertex_size, vertex_size)) for i in range(1, 6)]

# initialize mixer for music
pygame.mixer.init()
background_music = pygame.mixer.Sound('assets/amongus_drip_song.mp3')
background_music.set_volume(0.5)
background_music.play(loops=-1)

venting_sound = pygame.mixer.Sound('assets/venting_sound.mp3')
venting_sound.set_volume(4)

# initialize pygame
pygame.init()
dimension = (algorithm.G.old_n * vertex_size + (algorithm.G.old_n - 1) * edge_size) + algorithm.G.old_n * 2
screen = pygame.display.set_mode((dimension, dimension))
clock = pygame.time.Clock()
facing_right = True
time_since_end_of_game = None
frame_time_length = 150000000
running = True

# returns the color of the edge
def get_edge_color(edge : int) -> str:
    if edge == algorithm.G.NO_EDGE:
        return 'black'
    elif edge == algorithm.G.REMOVED_EDGE:
        return 'red'
    elif edge == algorithm.G.NEW_EDGE: 
        return 'green'
    # this case generally isn't used
    else:
        return 'grey'

# draws the maze
def draw_maze() -> None:
    screen.fill('grey') # draw the background
    row_offset = 0
    for row in range(algorithm.G.n):
        is_horizontal_wall = algorithm.G.IsHorizontalWall(row)
        col_offset = 0
        for col in range(algorithm.G.n):
            is_vertical_wall = algorithm.G.IsVerticalWall(col)
            curr = algorithm.G.maze[row][col]
            x, y = col + col_offset, row + row_offset
            if curr == algorithm.G.ENDPOINT: 
                if time_since_end_of_game is None:
                    # draw the goal (vent) before the start (amongus) to account for overlap
                    if (row, col) == algorithm.G.goal:
                        screen.blit(vent, (x + vertex_size * 0.1, y + vertex_size * 0.5))
                    if (row, col) == algorithm.G.start:
                        screen.blit(amongus, (x + vertex_size * 0.1, y + vertex_size * 0.025))
                else:
                    current_time = time.time_ns()
                    if current_time < time_since_end_of_game + frame_time_length * 5:
                        screen.blit(venting_frames[0], (x, y))
                    # second frame occurs three times in original gif
                    elif current_time < time_since_end_of_game + frame_time_length * 8:
                        screen.blit(venting_frames[1], (x, y))
                    elif current_time < time_since_end_of_game + frame_time_length * 9:
                        screen.blit(venting_frames[2], (x, y))
                    elif current_time < time_since_end_of_game + frame_time_length * 10:
                        screen.blit(venting_frames[3], (x, y))
                    else:
                        screen.blit(venting_frames[4], (x, y))
            # draw og walls black, newly added walls red, and removed walls green
            elif curr != algorithm.G.EMPTY_OR_EDGE:
                width = edge_size if is_vertical_wall else vertex_size
                height = edge_size if is_horizontal_wall else vertex_size
                pygame.draw.rect(screen, get_edge_color(curr), pygame.Rect(x, y, width, height))
            col_offset += edge_size if is_vertical_wall else vertex_size
        row_offset += edge_size if is_horizontal_wall else vertex_size
    pygame.display.update() # update the screen

while running:
    for event in pygame.event.get():
        # stop when user has x'd out the window
        if event.type == pygame.QUIT: 
            running = False
        if event.type == pygame.KEYDOWN and time_since_end_of_game is None:
            # add edges and recompute path
            if event.key == pygame.K_a:
                algorithm.AdaptToChanges(algorithm.G.AddEdges())
            # remove edges and recompute path
            if event.key == pygame.K_d:
                algorithm.AdaptToChanges(algorithm.G.RemoveEdges())
            # move amongus
            if event.key == pygame.K_w:
                new_start = algorithm.PickSuccessor()
                if new_start is None:
                    new_start = algorithm.G.start
                # change orientation of amongus based on move
                if new_start[1] < algorithm.G.start[1] and facing_right:
                    facing_right = False
                    amongus = pygame.transform.flip(amongus, True, False)
                elif new_start[1] > algorithm.G.start[1] and not facing_right:
                    facing_right = True
                    amongus = pygame.transform.flip(amongus, True, False)
                algorithm.G.MoveStart(new_start)
                if algorithm.G.start == algorithm.G.goal:
                    venting_sound.play()
                    time_since_end_of_game = time.time_ns()
                    # flip all the venting frames based on the final orientation
                    if not facing_right:
                        venting_frames = [pygame.transform.flip(frame, True, False) for frame in venting_frames]
    draw_maze()
    clock.tick(60) # cap at 60 fps

pygame.quit()

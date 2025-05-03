import pygame
import time
from typing import Tuple
from graph import Graph
from algorithms import algorithms

# TODO change algorithm name here
algorithm_name = 'd* lite'

# generate maze and initialize algorithm
maze_to_recreate = 'previous_maze.txt' # replace with 'previous_maze.txt' to use the last maze
G = Graph(n=10, allow_diagonal_movement=True, maze_to_recreate=maze_to_recreate)
with open('previous_maze.txt', 'w') as f:
    f.write(G.GetRecreationInfo())
algorithm = algorithms[algorithm_name](G)
algorithm.ComputePath() 

random_ahh_number_chosen_after_trial_and_error = 600
# as n increases, the vertex size decreases
vertex_size = int(random_ahh_number_chosen_after_trial_and_error  * (1 / G.old_n)) 
# as n increases, the edge size increases
edge_size = vertex_size // int(random_ahh_number_chosen_after_trial_and_error  * (1 / G.old_n)) if G.old_n > 60 else 10

# load and scale all the images
amongus = pygame.transform.scale(pygame.image.load("assets/amongus.png"), (vertex_size * 0.8, vertex_size * 0.7))
vent = pygame.transform.scale(pygame.image.load("assets/vent.png"), (vertex_size * 0.8, vertex_size * 0.5))
venting_frames = [pygame.transform.scale(pygame.image.load(f'assets/venting_frame{i}.png'), (vertex_size, vertex_size)) for i in range(1, 6)]

# initialize music
pygame.mixer.init()
background_music = pygame.mixer.Sound('assets/amongus_drip_song.mp3')
background_music.set_volume(0.5)
background_music.play(loops=-1)
venting_sound = pygame.mixer.Sound('assets/venting_sound.mp3')
venting_sound.set_volume(4)

# initialize font
pygame.font.init()
vertex_label_font = pygame.font.SysFont(name='helvetica', size=vertex_size // 4)
algorithm_name_font = pygame.font.SysFont(name='helvetica', size=20) 
header_detail_font = pygame.font.SysFont(name='helvetica', size=15) 

# initialize pygame
pygame.init()
maze_dimension = (G.old_n * vertex_size + (G.old_n - 1) * edge_size)
header_height = 110
# create the screen, which is comprised of a header and the maze
screen = pygame.display.set_mode((maze_dimension + 2 * edge_size, maze_dimension + 3 * edge_size + header_height)) 
header = pygame.surface.Surface((screen.get_width(), header_height))
header_x_offset = edge_size
header_y_offset = edge_size
maze = pygame.surface.Surface((maze_dimension, maze_dimension))
maze_x_offset = edge_size
maze_y_offset = edge_size * 2 + header_height
clock = pygame.time.Clock()
facing_right = True
time_since_end_of_game = None
frame_time_length = 150000000
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

# returns the edge located at pos on the maze
def get_edge_at_pos(pos : Tuple[int, int]) -> Tuple[int, int]:
    # subtract the maze's offset from the postion on the display
    pos_x, pos_y = pos[0] - maze_x_offset, pos[1] - maze_y_offset
    y_offset = 0
    for y in range(G.n):
        height = edge_size if G.IsHorizontalWall(y) else vertex_size
        x_offset = 0
        for x in range(G.n):
            width = edge_size if G.IsVerticalWall(x) else vertex_size
            if pos_y > y_offset and pos_y < (y_offset + height) and pos_x > x_offset and pos_x < (x_offset + width):
                if G.IsEdge((y, x)) and not (G.IsDiagonalEdge((y, x)) and not G.allow_diagonal_movement):
                    return (y, x)
                else:
                    return (-1, -1)
            x_offset += width
        y_offset += height
    # edge does not exist at pos (i.e. vertex exists at pos)
    return (-1, -1)

# draws the maze
def draw_maze() -> None:
    maze.fill('grey') # draw the background
    y_offset = 0
    for y in range(G.n):
        height = edge_size if G.IsHorizontalWall(y) else vertex_size
        x_offset = 0
        for x in range(G.n):
            width = edge_size if G.IsVerticalWall(x) else vertex_size
            curr = G.maze[y][x]
            if curr == G.ENDPOINT: 
                if time_since_end_of_game is None:
                    # draw the goal (vent) before the start (amongus) to account for overlap
                    if (y, x) == G.goal:
                        maze.blit(vent, (x_offset + vertex_size * 0.1, y_offset + vertex_size * 0.5))
                    elif (y, x) == G.start:
                        maze.blit(amongus, (x_offset + vertex_size * 0.1, y_offset + vertex_size * 0.025))
                # draw the venting animation based on time elapsed since end of game
                else:
                    current_time = time.time_ns()
                    if current_time < time_since_end_of_game + frame_time_length * 5:
                        maze.blit(venting_frames[0], (x_offset, y_offset))
                    # second frame occurs three times in original gif
                    elif current_time < time_since_end_of_game + frame_time_length * 8:
                        maze.blit(venting_frames[1], (x_offset, y_offset))
                    elif current_time < time_since_end_of_game + frame_time_length * 9:
                        maze.blit(venting_frames[2], (x_offset, y_offset))
                    elif current_time < time_since_end_of_game + frame_time_length * 10:
                        maze.blit(venting_frames[3], (x_offset, y_offset))
                    else:
                        maze.blit(venting_frames[4], (x_offset, y_offset))
            # draw og walls black, newly added walls red, and removed walls green
            elif curr != G.EMPTY_OR_EDGE:
                pygame.draw.rect(maze, get_edge_color(curr), pygame.Rect(x_offset, y_offset, width, height))
            # draw rhs and g values in the center of vertices for d* lite
            elif not G.IsEdge((y, x)) and algorithm_name == 'd* lite':
                vertex_data = vertex_label_font.render(f'{algorithm.rhs[(y, x)]}:{algorithm.g[(y, x)]}', True, 'black')
                maze.blit(vertex_data, (x_offset + (vertex_size - vertex_data.get_width()) // 2, y_offset + (vertex_size - vertex_label_font.get_height()) // 2))
            x_offset += width
        y_offset += height
    screen.blit(maze, (maze_x_offset, maze_y_offset))
    
def draw_screen() -> None:
    # draw the maze
    draw_maze()
    
    # draw the each line of the header separately
    header.fill('black')
    text_x_offset = edge_size
    text_y_offset = edge_size
    line_spacing = 10
    
    text = algorithm_name_font.render(f'algorithm: {algorithm_name}', True, 'white')
    header.blit(text, (text_x_offset, text_y_offset))
    text_y_offset += algorithm_name_font.get_height() + line_spacing

    text = header_detail_font.render("controls: press 'a'/'d' to randomly add/delete edges, 'w' to move towards the goal,", True, 'white')
    header.blit(text, (text_x_offset, text_y_offset))
    text_y_offset += header_detail_font.get_height() + line_spacing

    text = header_detail_font.render('and right click on edges to manually add or remove them', True, 'white')
    header.blit(text, (text_x_offset + header_detail_font.render('controls: ', True, 'white').get_width(), text_y_offset))
    text_y_offset += header_detail_font.get_height() + line_spacing

    # TODO add notes about algorithm visualizations here
    if algorithm_name == 'd* lite':
        text = header_detail_font.render('note: every vertex s is labeled with its rhs and g values in the form rhs(s):g(s)', True, 'white')
        header.blit(text, (text_x_offset, text_y_offset))

    screen.blit(header, (header_x_offset, header_y_offset))

    # update the screen
    pygame.display.update() 

while running:
    for event in pygame.event.get():
        # stop when user has x'd out the window
        if event.type == pygame.QUIT: 
            running = False
        # the sussy baka imposter has reached the goal vertex
        elif time_since_end_of_game is not None:
            continue
        # flip the state of the edge under the cursor when the mouse is clicked and recompute path
        elif event.type == pygame.MOUSEBUTTONDOWN: 
            y, x = get_edge_at_pos(pygame.mouse.get_pos())
            if (y, x) != (-1, -1):
                if G.maze[y][x] == G.EMPTY_OR_EDGE or G.maze[y][x] == G.NEW_EDGE:
                    prev_value = G.maze[y][x]
                    G.maze[y][x] = G.REMOVED_EDGE
                    # revert the removal if it eliminates the path from the start to the goal
                    if not G.PathExists():
                        G.maze[y][x] = prev_value
                        # TODO maybe replace with GUI notification
                        print('Error: cannot remove edge without eliminating the path from the start vertex to goal vertex')
                        continue
                else:
                    G.maze[y][x] = G.NEW_EDGE
                algorithm.AdaptToChanges([(y, x)])
        elif event.type == pygame.KEYDOWN:
            # add edges and recompute path
            if event.key == pygame.K_a:
                algorithm.AdaptToChanges(G.AddEdges())
            # remove edges and recompute path
            if event.key == pygame.K_d:
                algorithm.AdaptToChanges(G.RemoveEdges())
            # move amongus
            if event.key == pygame.K_w:
                new_start = algorithm.PickSuccessor()
                if new_start is None:
                    new_start = G.start
                # change orientation of amongus based on move
                if new_start[1] < G.start[1] and facing_right:
                    facing_right = False
                    amongus = pygame.transform.flip(amongus, True, False)
                elif new_start[1] > G.start[1] and not facing_right:
                    facing_right = True
                    amongus = pygame.transform.flip(amongus, True, False)
                G.MoveStart(new_start)
                if G.start == G.goal:
                    venting_sound.play()
                    time_since_end_of_game = time.time_ns()
                    # flip all the venting frames based on the final orientation
                    if not facing_right:
                        venting_frames = [pygame.transform.flip(frame, True, False) for frame in venting_frames]
    draw_screen()
    clock.tick(60) # cap at 60 fps

pygame.quit()

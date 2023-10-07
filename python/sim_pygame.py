import pygame
import sys
import math

# Constants for colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
LINE_COLOR = (0, 0, 0)
SELECTED_COLOR = (255, 0, 0)  # Red for selected nodes
CONNECTED_COLOR_X = (255, 0, 0)  # Red for connections made by player X
CONNECTED_COLOR_O = (0, 0, 255)  # Blue for connections made by player O
TEXT_COLOR = (0, 0, 0)

# Constants for the game board
SCREEN_WIDTH = 400
SCREEN_HEIGHT = 400
GRID_SIZE = 6
GRID_SPACING = SCREEN_WIDTH // GRID_SIZE

# Calculate node positions in a circle
circle_radius = SCREEN_WIDTH // 3
node_positions = [
    (int(SCREEN_WIDTH // 2 + circle_radius * math.cos(2 * math.pi * i / GRID_SIZE)),
     int(SCREEN_HEIGHT // 2 + circle_radius * math.sin(2 * math.pi * i / GRID_SIZE)))
    for i in range(GRID_SIZE)
]

#pygame.init()
pygame.init()
pygame.font.init()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Sim Game")

# Initialize the game board
board = [[' ' for _ in range(GRID_SIZE)] for _ in range(GRID_SIZE)]
players = ['X', 'O']
current_player = 0

# Keep track of connections for each player
connections_x = set()
connections_o = set()

# Initialize selected_node
selected_node = None

# Function to draw the game board
def draw_board():
    screen.fill(WHITE)

    for i in range(GRID_SIZE):
        for j in range(GRID_SIZE):
            pygame.draw.circle(screen, LINE_COLOR, node_positions[i], 5)
            if i < GRID_SIZE - 1:
                pygame.draw.line(screen, LINE_COLOR, node_positions[i], node_positions[j], 2)

    for i in range(GRID_SIZE):
        for j in range(GRID_SIZE):
            if board[i][j] == 'X':
                pygame.draw.circle(screen, BLACK, node_positions[i], 10)
            elif board[i][j] == 'O':
                pygame.draw.circle(screen, BLACK, node_positions[i], 10)

    for connection in connections_x:
        pygame.draw.line(screen, CONNECTED_COLOR_X, node_positions[connection[0]], node_positions[connection[1]], 4)
    
    for connection in connections_o:
        pygame.draw.line(screen, CONNECTED_COLOR_O, node_positions[connection[0]], node_positions[connection[1]], 4)

    if connecting and selected_node is not None:
        pygame.draw.circle(screen, SELECTED_COLOR, node_positions[selected_node], 12)
        for i, node_position in enumerate(node_positions):
            if selected_node != i and board[selected_node][i] == ' ':
                pygame.draw.line(screen, CONNECTED_COLOR_X if current_player == 0 else CONNECTED_COLOR_O, node_positions[selected_node], node_position, 4)

    # Display game state and current player's turn
    font = pygame.font.Font(None, 36)
    text = font.render(f"Player {players[current_player]}'s turn", True, TEXT_COLOR)
    text_rect = text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT - 30))
    screen.blit(text, text_rect)

# Function to check for a triangle
def check_for_triangle(player):
    for i in range(GRID_SIZE):
        for j in range(i + 1, GRID_SIZE):
            if board[i][j] == player:
                for k in range(j + 1, GRID_SIZE):
                    if board[i][k] == player and board[j][k] == player:
                        return True
    return False

# Main game loop
running = True
connecting = False
selected_node = None

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            x, y = pygame.mouse.get_pos()
            for i, (node_x, node_y) in enumerate(node_positions):
                distance = math.sqrt((x - node_x) ** 2 + (y - node_y) ** 2)
                if distance < 12:  # Increase the radius for highlighting
                    if not connecting:
                        if board[i][i] == ' ':
                            connecting = True
                            selected_node = i
                    else:
                        if selected_node != i and board[selected_node][i] == ' ':
                            board[selected_node][i] = players[current_player]
                            board[i][selected_node] = players[current_player]
                            connecting = False
                            selected_node = None
                            
                            # Update the connections
                            if current_player == 0:
                                connections_x.add((selected_node, i))
                                connections_x.add((i, selected_node))
                            else:
                                connections_o.add((selected_node, i))
                                connections_o.add((i, selected_node))
                            
                            draw_board()
                            pygame.display.update()

                            if check_for_triangle(players[current_player]):
                                # Display the losing player
                                font = pygame.font.Font(None, 48)
                                text = font.render(f"Player {players[current_player]} loses!", True, TEXT_COLOR)
                                text_rect = text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
                                screen.blit(text, text_rect)
                                pygame.display.update()
                                pygame.time.delay(2000)  # Delay for 2 seconds
                                pygame.quit()
                                sys.exit()

                            current_player = (current_player + 1) % 2

    draw_board()
    pygame.display.update()

pygame.quit()
sys.exit()

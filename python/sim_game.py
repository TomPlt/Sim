def print_board(board):
    for row in board:
        print(" ".join(row))

def check_for_triangle(board, player):
    for i in range(6):
        for j in range(i + 1, 6):
            if board[i][j] == player:
                for k in range(j + 1, 6):
                    if board[i][k] == player and board[j][k] == player:
                        return True
    return False

def main():
    board = [[' ' for _ in range(6)] for _ in range(6)]
    players = ['X', 'O']
    current_player = 0

    print("Welcome to the game of Sim!")
    print_board(board)

    while True:
        print(f"Player {players[current_player]}'s turn")
        edge_input = input("Enter the nodes you want to connect (e.g., '0 1'): ")
        edge_nodes = [int(node) for node in edge_input.split()]

        if len(edge_nodes) != 2 or edge_nodes[0] == edge_nodes[1] or edge_nodes[0] < 0 or edge_nodes[0] >= 6 or edge_nodes[1] < 0 or edge_nodes[1] >= 6:
            print("Invalid input. Please enter two different node numbers between 0 and 5.")
        elif board[edge_nodes[0]][edge_nodes[1]] != ' ':
            print("That edge is already colored. Try again.")
        else:
            board[edge_nodes[0]][edge_nodes[1]] = players[current_player]
            board[edge_nodes[1]][edge_nodes[0]] = players[current_player]
            print_board(board)

            if check_for_triangle(board, players[current_player]):
                print(f"Player {players[current_player]} loses!")
                break

            current_player = (current_player + 1) % 2

if __name__ == "__main__":
    main()

import random
import numpy as np
from sim_game import print_board, check_for_triangle
import pickle
from tqdm import tqdm


class QLearningAgent:
    def __init__(self, learning_rate=0.1, discount_factor=0.9, exploration_rate=1.0, exploration_decay=0.995):
        self.q_table = {}
        self.learning_rate = learning_rate
        self.discount_factor = discount_factor
        self.exploration_rate = exploration_rate
        self.exploration_decay = exploration_decay
    
    def get_state_representation(self, board):
        return "".join(["".join(row) for row in board])
    
    def get_valid_actions(self, board):
        return [(i, j) for i in range(6) for j in range(i + 1, 6) if board[i][j] == ' ']

    def choose_action(self, board):
        state = self.get_state_representation(board)
        if random.uniform(0, 1) < self.exploration_rate:
            return random.choice(self.get_valid_actions(board))
        q_values = {action: self.q_table.get((state, action), 0) for action in self.get_valid_actions(board)}
        max_q_value = max(q_values.values())
        return random.choice([action for action, q_value in q_values.items() if q_value == max_q_value])
    
    def learn(self, old_board, action, reward, new_board):
        old_state = self.get_state_representation(old_board)
        new_state = self.get_state_representation(new_board)
        old_q_value = self.q_table.get((old_state, action), 0)
        max_new_q_value = max([self.q_table.get((new_state, new_action), 0) for new_action in self.get_valid_actions(new_board)], default=0)
        self.q_table[(old_state, action)] = old_q_value + self.learning_rate * (reward + self.discount_factor * max_new_q_value - old_q_value)
        self.exploration_rate *= self.exploration_decay

    def save(self, filename="Sim\q_agent.pkl.pkl"):
        with open(filename, 'wb') as file:
            pickle.dump({
                'q_table': self.q_table,
                'learning_rate': self.learning_rate,
                'discount_factor': self.discount_factor,
                'exploration_rate': self.exploration_rate,
                'exploration_decay': self.exploration_decay
            }, file)
    def load(self, filename="q_agent.pkl"):
        with open(filename, 'rb') as file:
            data = pickle.load(file)
            self.q_table = data['q_table']
            self.learning_rate = data['learning_rate']
            self.discount_factor = data['discount_factor']
            self.exploration_rate = data['exploration_rate']
            self.exploration_decay = data['exploration_decay']

class RandomAgent:
    def get_valid_actions(self, board):
        return [(i, j) for i in range(6) for j in range(i + 1, 6) if board[i][j] == ' ']

    def choose_action(self, board):
        return random.choice(self.get_valid_actions(board))

def train_agent(num_episodes=1_000_000):
    q_agent = QLearningAgent()
    random_agent = RandomAgent()

    ai_wins = 0
    ai_losses = 0
    win_percentages = []

    for episode in range(num_episodes):
        board = [[' ' for _ in range(6)] for _ in range(6)]
        players = ['X', 'O']
        current_player = 0

        while True:
            prev_board = [row.copy() for row in board]

            # Agent's turn
            if current_player == 0:
                edge_nodes = q_agent.choose_action(board)
                board[edge_nodes[0]][edge_nodes[1]] = players[current_player]
                board[edge_nodes[1]][edge_nodes[0]] = players[current_player]
            # Random opponent's turn
            else:
                edge_nodes = random_agent.choose_action(board)
                board[edge_nodes[0]][edge_nodes[1]] = players[current_player]
                board[edge_nodes[1]][edge_nodes[0]] = players[current_player]

            # Check for game end condition
            if check_for_triangle(board, players[current_player]):
                if current_player == 0:
                    ai_losses += 1
                else:
                    ai_wins += 1
                reward = -1 if current_player == 0 else 1
                q_agent.learn(prev_board, edge_nodes, reward, board)
                break

            # If the AI made a move, update Q-values before switching player
            if current_player == 0:
                reward = 0  # No winner yet
                q_agent.learn(prev_board, edge_nodes, reward, board)

            # Switch player
            current_player = (current_player + 1) % 2

        # Print statistics every 1000 episodes
        if episode % 1000 == 0 and episode > 0:
            win_percentage = ai_wins / 1000
            win_percentages.append(win_percentage)
            ai_wins = 0  # Reset wins count after each 1000 episodes
            ai_losses = 0  # Reset losses count as well
            print(f"Episode {episode}, AI Win Percentage: {win_percentage:.2%}")
        
        # Decaying exploration rate
        q_agent.exploration_rate = max(0.05, q_agent.exploration_rate * q_agent.exploration_decay)
    
    # Saving the agent
    q_agent.save()
    return win_percentages


def test_agent(agent: QLearningAgent, num_games=10000):
    random_agent = RandomAgent()
    ai_wins = 0
    ai_losses = 0

    for game in tqdm(range(num_games)):
        board = [[' ' for _ in range(6)] for _ in range(6)]
        players = ['X', 'O']
        current_player = 0

        while True:
            # Agent's turn
            if current_player == 0:
                edge_nodes = agent.choose_action(board)
                board[edge_nodes[0]][edge_nodes[1]] = players[current_player]
                board[edge_nodes[1]][edge_nodes[0]] = players[current_player]
            # Random opponent's turn
            else:
                edge_nodes = random_agent.choose_action(board)
                board[edge_nodes[0]][edge_nodes[1]] = players[current_player]
                board[edge_nodes[1]][edge_nodes[0]] = players[current_player]

            # Check for game end condition
            if check_for_triangle(board, players[current_player]):
                if current_player == 0:
                    ai_losses += 1
                else:
                    ai_wins += 1
                break

            # Switch player
            current_player = (current_player + 1) % 2

    win_percentage = ai_wins / num_games
    print(f"AI win percentage over {num_games} games: {win_percentage:.2%}")
    return win_percentage

def main():
    # num_episodes = 1_000_000
    # win_percentages = train_agent(num_episodes)
    trained_agent = QLearningAgent()
    trained_agent.load()  # Load trained Q-table
    train_agent()
    win_rate = test_agent(trained_agent, num_games=10_000)
    print(f"AI win rate after training: {win_rate:.2%}")

if __name__ == "__main__":
    main()
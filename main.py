import csv
import math

def read_players(filename):
    try:
        with open(filename, 'r') as file:
            reader = csv.reader(file)
            players = {row[0]: float(row[1]) for row in reader if len(row) >= 2}
    except FileNotFoundError:
        players = {}
    return players

def write_players(filename, players):
    with open(filename, 'w', newline='') as file:
        writer = csv.writer(file)
        for player, elo in players.items():
            elo_formatted = "{:.1f}".format(elo)  # Format Elo rating with one decimal place
            writer.writerow([player, elo_formatted])

def calculate_elo(winner_elo, loser_elo):
    expected_winner = 1 / (1 + 10 ** ((loser_elo - winner_elo) / 400))
    expected_loser = 1 / (1 + 10 ** ((winner_elo - loser_elo) / 400))

    k_factor = 32  # You can adjust the k_factor based on the desired sensitivity of Elo changes.

    winner_elo_new = winner_elo + k_factor * (1 - expected_winner)
    loser_elo_new = loser_elo + k_factor * (0 - expected_loser)

    return winner_elo_new, loser_elo_new

def main():
    filename = 'foosball_ratings.csv'

    # Read existing player ratings or create an empty dictionary
    players = read_players(filename)

    # Get user input for match details
    player1 = input("Enter the first name and the last initial of the first player: ")
    player2 = input("Enter the first name and the last initial of the second player: ")
    winner = input("Enter the first name and the last initial of the winner: ")

    # Check if players have existing ratings, create default if not
    if player1 not in players:
        players[player1] = 1200
    if player2 not in players:
        players[player2] = 1200

    # Get current player ratings
    player1_elo = players[player1]
    player2_elo = players[player2]

    # Update player ratings based on the match outcome
    if winner == player1 or winner == player2:
        winner_elo_new, loser_elo_new = calculate_elo(player1_elo, player2_elo) if winner == player1 else calculate_elo(player2_elo, player1_elo)
        
        # Update player ratings in the dictionary
        players[player1] = winner_elo_new if winner == player1 else loser_elo_new
        players[player2] = winner_elo_new if winner == player2 else loser_elo_new

        # Write updated player ratings to the file
        write_players(filename, players)

        # Display updated ratings
        #print(f"\nUpdated Ratings:\n{player1}: {players[player1]}\n{player2}: {players[player2]}")
        print(f"\nUpdated Ratings:\n{player1}: {players[player1]:.1f}\n{player2}: {players[player2]:.1f}")

    else:
        print("Invalid winner name. No changes made.")

if __name__ == "__main__":
    main()

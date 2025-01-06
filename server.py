import socket
import threading

# Game logic for Rock, Paper, Scissors
def determine_winner(choice1, choice2):
    if choice1 == choice2:
        return "Draw"
    elif (choice1 == "Rock" and choice2 == "Scissors") or \
         (choice1 == "Paper" and choice2 == "Rock") or \
         (choice1 == "Scissors" and choice2 == "Paper"):
        return "Player 1 Wins"
    else:
        return "Player 2 Wins"

# Function to handle each client
def handle_client(client_socket, player, choices, results, lock):
    while True:
        try:
            # Receive the client's choice
            choice = client_socket.recv(1024).decode()
            with lock:
                choices[player] = choice

            # Wait until both players have made a choice
            while None in choices:
                pass

            with lock:
                # Compute result and notify both clients
                if results[player] is None:
                    result = determine_winner(choices[0], choices[1])
                    results[0], results[1] = result, result
                    other_player = 1 - player
                    client_socket.send(
                        f"Your choice: {choices[player]}\nOpponent's choice: {choices[other_player]}\nResult: {results[player]}".encode()
                    )
        except:
            print(f"Player {player + 1} disconnected.")
            break

# Main server function
def main():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind(("0.0.0.0", 5555))
    server.listen(2)
    print("Server started. Waiting for players to connect...")

    choices = [None, None]  # Store choices of player 1 and player 2
    results = [None, None]  # Store results for player 1 and player 2
    lock = threading.Lock()  # Ensure thread safety

    players = []
    for i in range(2):
        client_socket, addr = server.accept()
        print(f"Player {i + 1} connected from {addr}.")
        players.append(client_socket)
        threading.Thread(target=handle_client, args=(client_socket, i, choices, results, lock)).start()

if __name__ == "__main__":
    main()

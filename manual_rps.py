import random


choices = ["Rock", "Paper", "Scissors"]

def get_computer_choice() -> str:
    return random.choice(["rock", "paper", "scissors"])

def get_user_choice() -> str:
    while True:
        choice = str(input("Enter 'Rock', 'Paper', or 'Scissors': ")).lower()
        if choice in ("rock", "paper", "scissors"):
            return choice

def get_winner(computer_choice: str, user_choice: str) -> str:
    print(computer_choice)
    u_w = "User wins"
    c_w = "Computer_wins"
    if computer_choice == user_choice:
        return "Tie"
    elif computer_choice == "rock":
        if user_choice == "paper":
            return u_w
        else:
            return c_w
    elif computer_choice == "paper":
        if user_choice == "scissors":
            return u_w
        else:
            return c_w
    else:
        if user_choice == "rock":
            return u_w
        else:
            return c_w

print(get_winner(get_computer_choice(),get_user_choice()))